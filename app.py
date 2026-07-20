"""
app.py — Flask backend for option chain frontend.
Run: python app.py
"""
import os
import sys
from datetime import date, datetime

import pytz
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

OPTION_DB = os.getenv("OPTION_DB", "data/option_chain.db")
IST       = pytz.timezone("Asia/Kolkata")

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

_STRIKE_GAP = {"NIFTY50": 50, "BANKNIFTY": 100, "MIDCAPNIFTY": 25, "FINNIFTY": 50, "SENSEX": 100}
_DISPLAY_NAME = {
    "NIFTY50":     "NIFTY 50",
    "BANKNIFTY":   "BANK NIFTY",
    "FINNIFTY":    "FIN NIFTY",
    "MIDCAPNIFTY": "MIDCAP NIFTY",
    "SENSEX":      "SENSEX",
}


def _fmt(v):
    if v is None or (isinstance(v, float) and __import__('math').isnan(v)):
        return None
    return round(float(v), 2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/expiries")
def api_expiries():
    symbol = request.args.get("symbol", "NIFTY50")
    try:
        from src.option_chain.nse_scraper import get_expiry_dates
        today    = datetime.now(IST).date()
        expiries = [
            e for e in get_expiry_dates(symbol)
            if datetime.strptime(e, "%d-%b-%Y").date() >= today
        ]
        return jsonify(expiries[:4])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/option-chain")
def api_option_chain():
    symbol = request.args.get("symbol", "NIFTY50")
    expiry = request.args.get("expiry", "")

    from src.option_chain.nse_scraper import fetch_option_chain, get_expiry_dates, get_spot
    from src.database import insert_option_data

    spot = get_spot(symbol) or 0.0

    if not expiry:
        expiries = get_expiry_dates(symbol)
        expiry   = expiries[0] if expiries else ""

    try:
        df = fetch_option_chain(symbol, expiry, spot)
    except Exception as e:
        return jsonify({"error": f"Option chain fetch failed: {e}"}), 502

    if df.empty:
        return jsonify({"error": "No option chain data available"}), 404

    try:
        insert_option_data(OPTION_DB, symbol, df, spot)
    except Exception:
        pass

    gap = _STRIKE_GAP.get(symbol, 50)
    atm = round(spot / gap) * gap if spot else 0

    chain = {}
    for _, r in df.iterrows():
        s = float(r["strike"])
        if s not in chain:
            chain[s] = {"strike": s, "CE": {}, "PE": {}}
        otype = str(r["option_type"]).upper()
        chain[s][otype] = {
            "oi":     _fmt(r.get("oi")),
            "oiChg":  _fmt(r.get("oi_chg")),
            "volume": _fmt(r.get("volume")),
            "iv":     _fmt(r.get("iv")),
            "ltp":    _fmt(r.get("ltp")),
            "open":   _fmt(r.get("open")),
            "high":   _fmt(r.get("high")),
            "low":    _fmt(r.get("low")),
            "close":  _fmt(r.get("close")),
            "delta":  _fmt(r.get("delta")),
            "gamma":  _fmt(r.get("gamma")),
            "theta":  _fmt(r.get("theta")),
            "vega":   _fmt(r.get("vega")),
            "rho":    _fmt(r.get("rho")),
        }

    rows = sorted(chain.values(), key=lambda x: x["strike"])
    return jsonify({
        "spot":   spot,
        "atm":    atm,
        "rows":   rows,
        "symbol": _DISPLAY_NAME.get(symbol, symbol),
        "expiry": expiry,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
