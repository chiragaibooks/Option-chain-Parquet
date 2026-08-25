"""greeks.py — Black-Scholes option Greeks (single source of truth).

All functions follow the standard Black-Scholes model:
  - spot  : underlying price (S)
  - strike: option strike (K)
  - tte   : time to expiry in *years* (e.g. 7/365)
  - r     : risk-free rate as decimal (e.g. 0.065)
  - iv    : implied volatility as decimal (e.g. 0.18)

Conventions:
  - delta : CE ∈ (0, 1)  |  PE ∈ (-1, 0)
  - gamma : same for CE and PE
  - theta : per *calendar day* (divide BS theta by 365)
  - vega  : per 1% change in IV (divide BS vega by 100)
  - rho   : per 1% change in interest rate (divide BS rho by 100)
"""
import logging
import math
from typing import Literal, Optional

from scipy.stats import norm

logger = logging.getLogger(__name__)


def _d1_d2(spot: float, strike: float, tte: float, r: float, iv: float):
    if tte <= 0 or iv <= 0:
        raise ValueError(f"tte and iv must be positive, got tte={tte} iv={iv}")
    d1 = (math.log(spot / strike) + (r + 0.5 * iv ** 2) * tte) / (iv * math.sqrt(tte))
    return d1, d1 - iv * math.sqrt(tte)


def delta(
    spot: float, strike: float, tte: float, r: float, iv: float,
    option_type: Literal["CE", "PE"] = "CE",
) -> float:
    """Delta: CE ∈ (0,1), PE ∈ (-1,0)."""
    d1, _ = _d1_d2(spot, strike, tte, r, iv)
    return norm.cdf(d1) if option_type == "CE" else norm.cdf(d1) - 1


def gamma(spot: float, strike: float, tte: float, r: float, iv: float) -> float:
    """Gamma — identical for CE and PE."""
    d1, _ = _d1_d2(spot, strike, tte, r, iv)
    return norm.pdf(d1) / (spot * iv * math.sqrt(tte))


def theta(
    spot: float, strike: float, tte: float, r: float, iv: float,
    option_type: Literal["CE", "PE"] = "CE",
) -> float:
    """Theta per calendar day (negative for long options)."""
    d1, d2 = _d1_d2(spot, strike, tte, r, iv)
    pdf_d1  = norm.pdf(d1)
    t_decay = -(spot * pdf_d1 * iv) / (2 * math.sqrt(tte))
    disc    = r * strike * math.exp(-r * tte)
    if option_type == "CE":
        return (t_decay - disc * norm.cdf(d2)) / 365
    return (t_decay + disc * norm.cdf(-d2)) / 365


def vega(spot: float, strike: float, tte: float, r: float, iv: float) -> float:
    """Vega per 1% change in IV."""
    d1, _ = _d1_d2(spot, strike, tte, r, iv)
    return spot * norm.pdf(d1) * math.sqrt(tte) / 100


def rho(
    spot: float, strike: float, tte: float, r: float, iv: float,
    option_type: Literal["CE", "PE"] = "CE",
) -> float:
    """Rho per 1% change in interest rate."""
    _, d2 = _d1_d2(spot, strike, tte, r, iv)
    factor = strike * tte * math.exp(-r * tte) / 100
    return factor * norm.cdf(d2) if option_type == "CE" else -factor * norm.cdf(-d2)


def compute_greeks(
    spot: float,
    strike: float,
    tte: float,
    r: float,
    iv: float,
    option_type: Literal["CE", "PE"] = "CE",
) -> dict:
    """
    Compute all five BS Greeks. Returns a dict with keys:
    delta, gamma, theta, vega, rho — all rounded to 6 sig-figs.
    Returns None for each key on any calculation failure.

    Parameters
    ----------
    spot        : underlying price
    strike      : option strike
    tte         : time to expiry in years (e.g. 7/365)
    r           : annualised risk-free rate as decimal (e.g. 0.065)
    iv          : annualised implied volatility as decimal (e.g. 0.18)
    option_type : "CE" or "PE"
    """
    null = {k: None for k in ("delta", "gamma", "theta", "vega", "rho")}
    if not (spot > 0 and strike > 0 and tte > 0 and iv > 0):
        return null
    try:
        return {
            "delta": round(delta(spot, strike, tte, r, iv, option_type), 4),
            "gamma": round(gamma(spot, strike, tte, r, iv),              6),
            "theta": round(theta(spot, strike, tte, r, iv, option_type), 4),
            "vega":  round(vega (spot, strike, tte, r, iv),              4),
            "rho":   round(rho  (spot, strike, tte, r, iv, option_type), 4),
        }
    except Exception:
        logger.exception("compute_greeks failed: spot=%s strike=%s type=%s", spot, strike, option_type)
        return null
