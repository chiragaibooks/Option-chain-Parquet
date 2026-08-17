<!-- auto-updated: 17 Aug 2026 09:31:59 IST -->

# 📋 NIFTY50 Option Chain — Last 10 Snapshots

**Updated:** 17 Aug 2026 09:31:59 IST

---

<script>
function applyFilters() {
  var expiry = document.getElementById('f-expiry').value;
  var type   = document.getElementById('f-type').value;
  var sMin   = parseFloat(document.getElementById('f-strike-min').value) || -Infinity;
  var sMax   = parseFloat(document.getElementById('f-strike-max').value) || Infinity;
  var lMin   = parseFloat(document.getElementById('f-ltp-min').value)    || -Infinity;
  var lMax   = parseFloat(document.getElementById('f-ltp-max').value)    || Infinity;
  document.querySelectorAll('table tr[data-expiry]').forEach(function(row) {
    var eMatch = !expiry || row.dataset.expiry === expiry;
    var tMatch = !type   || row.dataset.type   === type;
    var strike = parseFloat(row.dataset.strike);
    var ltp    = parseFloat(row.dataset.ltp);
    var sMatch = strike >= sMin && strike <= sMax;
    var lMatch = ltp    >= lMin && ltp    <= lMax;
    row.style.display = (eMatch && tMatch && sMatch && lMatch) ? '' : 'none';
  });
}
function resetFilters() {
  ['f-expiry','f-type','f-strike-min','f-strike-max','f-ltp-min','f-ltp-max'].forEach(function(id){
    document.getElementById(id).value='';
  });
  applyFilters();
}
</script>

<details open>
<summary><b>🔍 Column Filters</b></summary>

<table>
<tr>
  <th>Expiry</th>
  <th>Strike Min</th><th>Strike Max</th>
  <th>Type</th>
  <th>LTP Min</th><th>LTP Max</th>
  <th></th>
</tr>
<tr>
  <td><select id='f-expiry' onchange='applyFilters()'><option value=''>All</option><option value="01-Sep-2026">01-Sep-2026</option><option value="08-Sep-2026">08-Sep-2026</option><option value="18-Aug-2026">18-Aug-2026</option><option value="25-Aug-2026">25-Aug-2026</option></select></td>
  <td><input id='f-strike-min' type='number' placeholder='e.g. 24000' oninput='applyFilters()' style='width:90px'></td>
  <td><input id='f-strike-max' type='number' placeholder='e.g. 25000' oninput='applyFilters()' style='width:90px'></td>
  <td><select id='f-type' onchange='applyFilters()'><option value=''>All</option><option>CE</option><option>PE</option></select></td>
  <td><input id='f-ltp-min' type='number' placeholder='e.g. 10' oninput='applyFilters()' style='width:80px'></td>
  <td><input id='f-ltp-max' type='number' placeholder='e.g. 500' oninput='applyFilters()' style='width:80px'></td>
  <td><button onclick='resetFilters()'>Reset</button></td>
</tr>
</table>

</details>

## 🕐 17 Aug 2026 09:31 IST

<table>
<tr><th>Timestamp</th><th>Expiry</th><th>Strike</th><th>Type</th><th>LTP</th></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='21200' data-ltp='1.15'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>21200</td><td>PE</td><td>1.15</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='21300' data-ltp='1.25'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>21300</td><td>PE</td><td>1.25</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='21350' data-ltp='1.2'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>21350</td><td>PE</td><td>1.20</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='21400' data-ltp='1.3'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>21400</td><td>PE</td><td>1.30</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='21450' data-ltp='1.2'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>21450</td><td>PE</td><td>1.20</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='21500' data-ltp='2854.3'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>21500</td><td>CE</td><td>2,854.30</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='21500' data-ltp='1.45'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>21500</td><td>PE</td><td>1.45</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='21600' data-ltp='1.55'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>21600</td><td>PE</td><td>1.55</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='21650' data-ltp='1.45'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>21650</td><td>PE</td><td>1.45</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='21700' data-ltp='1.5'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>21700</td><td>PE</td><td>1.50</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='21900' data-ltp='1.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>21900</td><td>PE</td><td>1.65</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='22000' data-ltp='2341.95'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22000</td><td>CE</td><td>2,341.95</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='22000' data-ltp='3.85'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>22000</td><td>PE</td><td>3.85</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22000' data-ltp='0.3'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22000</td><td>PE</td><td>0.30</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22000' data-ltp='1.85'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22000</td><td>PE</td><td>1.85</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22050' data-ltp='0.3'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22050</td><td>PE</td><td>0.30</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='22100' data-ltp='3.7'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>22100</td><td>PE</td><td>3.70</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22100' data-ltp='0.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22100</td><td>PE</td><td>0.35</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22100' data-ltp='2.0'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22100</td><td>PE</td><td>2.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22150' data-ltp='0.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22150</td><td>PE</td><td>0.35</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='22200' data-ltp='3.55'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>22200</td><td>PE</td><td>3.55</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22200' data-ltp='0.3'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22200</td><td>PE</td><td>0.30</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22200' data-ltp='2.05'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22200</td><td>PE</td><td>2.05</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='22250' data-ltp='3.45'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>22250</td><td>PE</td><td>3.45</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22250' data-ltp='0.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22250</td><td>PE</td><td>0.35</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='22300' data-ltp='4.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>22300</td><td>PE</td><td>4.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22300' data-ltp='0.45'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22300</td><td>PE</td><td>0.45</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22300' data-ltp='2.15'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22300</td><td>PE</td><td>2.15</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22350' data-ltp='0.5'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22350</td><td>PE</td><td>0.50</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22400' data-ltp='0.45'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22400</td><td>PE</td><td>0.45</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22400' data-ltp='2.3'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22400</td><td>PE</td><td>2.30</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22450' data-ltp='0.5'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22450</td><td>PE</td><td>0.50</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='22500' data-ltp='1847.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22500</td><td>CE</td><td>1,847.65</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='22500' data-ltp='4.5'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>22500</td><td>PE</td><td>4.50</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22500' data-ltp='0.55'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22500</td><td>PE</td><td>0.55</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22500' data-ltp='2.45'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22500</td><td>PE</td><td>2.45</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22550' data-ltp='0.6'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22550</td><td>PE</td><td>0.60</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22550' data-ltp='2.55'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22550</td><td>PE</td><td>2.55</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='22600' data-ltp='1777.0'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22600</td><td>CE</td><td>1,777.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22600' data-ltp='0.55'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22600</td><td>PE</td><td>0.55</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22600' data-ltp='2.45'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22600</td><td>PE</td><td>2.45</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22650' data-ltp='0.6'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22650</td><td>PE</td><td>0.60</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22650' data-ltp='2.45'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22650</td><td>PE</td><td>2.45</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='22700' data-ltp='4.8'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>22700</td><td>PE</td><td>4.80</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22700' data-ltp='0.6'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22700</td><td>PE</td><td>0.60</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22700' data-ltp='2.7'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22700</td><td>PE</td><td>2.70</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22750' data-ltp='0.6'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22750</td><td>PE</td><td>0.60</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='22800' data-ltp='5.45'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>22800</td><td>PE</td><td>5.45</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22800' data-ltp='0.65'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22800</td><td>PE</td><td>0.65</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22800' data-ltp='2.75'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22800</td><td>PE</td><td>2.75</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='22850' data-ltp='5.9'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>22850</td><td>PE</td><td>5.90</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22850' data-ltp='0.7'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22850</td><td>PE</td><td>0.70</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22850' data-ltp='2.85'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22850</td><td>PE</td><td>2.85</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='22900' data-ltp='6.25'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>22900</td><td>PE</td><td>6.25</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='22900' data-ltp='11.8'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>22900</td><td>PE</td><td>11.80</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22900' data-ltp='0.75'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22900</td><td>PE</td><td>0.75</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22900' data-ltp='3.05'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22900</td><td>PE</td><td>3.05</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='22950' data-ltp='0.8'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>22950</td><td>PE</td><td>0.80</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='22950' data-ltp='3.2'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>22950</td><td>PE</td><td>3.20</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='23000' data-ltp='1342.9'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23000</td><td>CE</td><td>1,342.90</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23000' data-ltp='6.8'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23000</td><td>PE</td><td>6.80</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='23000' data-ltp='12.5'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>23000</td><td>PE</td><td>12.50</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23000' data-ltp='0.75'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23000</td><td>PE</td><td>0.75</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23000' data-ltp='3.25'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23000</td><td>PE</td><td>3.25</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23050' data-ltp='6.9'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23050</td><td>PE</td><td>6.90</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='23050' data-ltp='14.15'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>23050</td><td>PE</td><td>14.15</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23050' data-ltp='0.85'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23050</td><td>PE</td><td>0.85</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23050' data-ltp='3.35'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23050</td><td>PE</td><td>3.35</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23100' data-ltp='7.3'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23100</td><td>PE</td><td>7.30</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='23100' data-ltp='14.6'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>23100</td><td>PE</td><td>14.60</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23100' data-ltp='0.85'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23100</td><td>PE</td><td>0.85</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23100' data-ltp='3.45'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23100</td><td>PE</td><td>3.45</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23150' data-ltp='7.85'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23150</td><td>PE</td><td>7.85</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='23150' data-ltp='16.0'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>23150</td><td>PE</td><td>16.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23150' data-ltp='0.9'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23150</td><td>PE</td><td>0.90</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23150' data-ltp='3.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23150</td><td>PE</td><td>3.65</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='23200' data-ltp='1230.0'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>23200</td><td>CE</td><td>1,230.00</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23200' data-ltp='8.5'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23200</td><td>PE</td><td>8.50</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23200' data-ltp='0.9'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23200</td><td>PE</td><td>0.90</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23200' data-ltp='3.8'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23200</td><td>PE</td><td>3.80</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23250' data-ltp='9.3'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23250</td><td>PE</td><td>9.30</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23250' data-ltp='0.95'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23250</td><td>PE</td><td>0.95</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23250' data-ltp='4.0'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23250</td><td>PE</td><td>4.00</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='23300' data-ltp='1080.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23300</td><td>CE</td><td>1,080.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='23300' data-ltp='1000.0'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23300</td><td>CE</td><td>1,000.00</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='23300' data-ltp='1040.75'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23300</td><td>CE</td><td>1,040.75</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23300' data-ltp='10.25'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23300</td><td>PE</td><td>10.25</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23300' data-ltp='1.05'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23300</td><td>PE</td><td>1.05</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23300' data-ltp='4.25'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23300</td><td>PE</td><td>4.25</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='23350' data-ltp='24.1'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>23350</td><td>PE</td><td>24.10</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23350' data-ltp='1.0'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23350</td><td>PE</td><td>1.00</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23350' data-ltp='4.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23350</td><td>PE</td><td>4.65</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23400' data-ltp='12.7'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23400</td><td>PE</td><td>12.70</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23400' data-ltp='1.1'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23400</td><td>PE</td><td>1.10</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23400' data-ltp='5.15'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23400</td><td>PE</td><td>5.15</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='23450' data-ltp='31.05'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>23450</td><td>PE</td><td>31.05</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23450' data-ltp='1.15'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23450</td><td>PE</td><td>1.15</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23450' data-ltp='5.75'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23450</td><td>PE</td><td>5.75</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='23500' data-ltp='905.95'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23500</td><td>CE</td><td>905.95</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='23500' data-ltp='815.95'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23500</td><td>CE</td><td>815.95</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='23500' data-ltp='846.85'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23500</td><td>CE</td><td>846.85</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23500' data-ltp='16.05'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23500</td><td>PE</td><td>16.05</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='23500' data-ltp='32.05'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>23500</td><td>PE</td><td>32.05</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23500' data-ltp='1.15'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23500</td><td>PE</td><td>1.15</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23500' data-ltp='6.45'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23500</td><td>PE</td><td>6.45</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23550' data-ltp='1.25'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23550</td><td>PE</td><td>1.25</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23550' data-ltp='7.05'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23550</td><td>PE</td><td>7.05</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='23600' data-ltp='714.0'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23600</td><td>CE</td><td>714.00</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='23600' data-ltp='748.9'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23600</td><td>CE</td><td>748.90</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23600' data-ltp='21.95'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23600</td><td>PE</td><td>21.95</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23600' data-ltp='1.3'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23600</td><td>PE</td><td>1.30</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23600' data-ltp='7.85'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23600</td><td>PE</td><td>7.85</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='23650' data-ltp='667.2'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23650</td><td>CE</td><td>667.20</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='23650' data-ltp='45.5'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>23650</td><td>PE</td><td>45.50</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23650' data-ltp='1.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23650</td><td>PE</td><td>1.35</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23650' data-ltp='9.5'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23650</td><td>PE</td><td>9.50</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='23700' data-ltp='621.6'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23700</td><td>CE</td><td>621.60</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='23700' data-ltp='657.9'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23700</td><td>CE</td><td>657.90</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23700' data-ltp='29.5'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23700</td><td>PE</td><td>29.50</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='23700' data-ltp='51.95'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>23700</td><td>PE</td><td>51.95</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23700' data-ltp='1.45'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23700</td><td>PE</td><td>1.45</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23700' data-ltp='10.95'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23700</td><td>PE</td><td>10.95</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='23750' data-ltp='578.4'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23750</td><td>CE</td><td>578.40</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='23750' data-ltp='605.5'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23750</td><td>CE</td><td>605.50</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23750' data-ltp='1.6'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23750</td><td>PE</td><td>1.60</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23750' data-ltp='13.55'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23750</td><td>PE</td><td>13.55</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='23800' data-ltp='633.65'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23800</td><td>CE</td><td>633.65</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='23800' data-ltp='512.4'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23800</td><td>CE</td><td>512.40</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='23800' data-ltp='560.0'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23800</td><td>CE</td><td>560.00</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23800' data-ltp='39.7'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23800</td><td>PE</td><td>39.70</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23800' data-ltp='1.9'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23800</td><td>PE</td><td>1.90</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23800' data-ltp='16.6'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23800</td><td>PE</td><td>16.60</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='23850' data-ltp='463.1'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23850</td><td>CE</td><td>463.10</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='23850' data-ltp='522.4'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23850</td><td>CE</td><td>522.40</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23850' data-ltp='46.65'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23850</td><td>PE</td><td>46.65</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23850' data-ltp='2.15'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23850</td><td>PE</td><td>2.15</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23850' data-ltp='20.55'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23850</td><td>PE</td><td>20.55</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='23900' data-ltp='412.7'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23900</td><td>CE</td><td>412.70</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='23900' data-ltp='471.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23900</td><td>CE</td><td>471.65</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23900' data-ltp='54.05'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23900</td><td>PE</td><td>54.05</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23900' data-ltp='2.55'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23900</td><td>PE</td><td>2.55</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23900' data-ltp='25.4'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23900</td><td>PE</td><td>25.40</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='23950' data-ltp='492.6'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23950</td><td>CE</td><td>492.60</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='23950' data-ltp='363.3'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23950</td><td>CE</td><td>363.30</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='23950' data-ltp='428.4'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23950</td><td>CE</td><td>428.40</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='23950' data-ltp='63.3'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>23950</td><td>PE</td><td>63.30</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='23950' data-ltp='92.3'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>23950</td><td>PE</td><td>92.30</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='23950' data-ltp='3.15'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>23950</td><td>PE</td><td>3.15</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='23950' data-ltp='31.6'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>23950</td><td>PE</td><td>31.60</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24000' data-ltp='448.5'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24000</td><td>CE</td><td>448.50</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='24000' data-ltp='508.0'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24000</td><td>CE</td><td>508.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24000' data-ltp='315.8'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24000</td><td>CE</td><td>315.80</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24000' data-ltp='382.7'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24000</td><td>CE</td><td>382.70</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24000' data-ltp='72.8'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24000</td><td>PE</td><td>72.80</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='24000' data-ltp='105.15'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24000</td><td>PE</td><td>105.15</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24000' data-ltp='4.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24000</td><td>PE</td><td>4.35</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24000' data-ltp='39.75'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24000</td><td>PE</td><td>39.75</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24050' data-ltp='419.55'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24050</td><td>CE</td><td>419.55</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24050' data-ltp='267.05'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24050</td><td>CE</td><td>267.05</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24050' data-ltp='341.8'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24050</td><td>CE</td><td>341.80</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24050' data-ltp='6.05'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24050</td><td>PE</td><td>6.05</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24050' data-ltp='48.75'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24050</td><td>PE</td><td>48.75</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24100' data-ltp='373.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24100</td><td>CE</td><td>373.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24100' data-ltp='220.55'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24100</td><td>CE</td><td>220.55</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24100' data-ltp='303.5'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24100</td><td>CE</td><td>303.50</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24100' data-ltp='98.5'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24100</td><td>PE</td><td>98.50</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='24100' data-ltp='132.45'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24100</td><td>PE</td><td>132.45</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24100' data-ltp='9.4'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24100</td><td>PE</td><td>9.40</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24100' data-ltp='59.7'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24100</td><td>PE</td><td>59.70</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24150' data-ltp='349.15'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24150</td><td>CE</td><td>349.15</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24150' data-ltp='176.15'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24150</td><td>CE</td><td>176.15</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24150' data-ltp='267.5'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24150</td><td>CE</td><td>267.50</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24150' data-ltp='15.05'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24150</td><td>PE</td><td>15.05</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24150' data-ltp='72.9'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24150</td><td>PE</td><td>72.90</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24200' data-ltp='306.8'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24200</td><td>CE</td><td>306.80</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='24200' data-ltp='370.05'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24200</td><td>CE</td><td>370.05</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24200' data-ltp='135.85'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24200</td><td>CE</td><td>135.85</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24200' data-ltp='232.45'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24200</td><td>CE</td><td>232.45</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24200' data-ltp='129.55'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24200</td><td>PE</td><td>129.55</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='24200' data-ltp='161.45'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24200</td><td>PE</td><td>161.45</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24200' data-ltp='24.3'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24200</td><td>PE</td><td>24.30</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24200' data-ltp='88.5'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24200</td><td>PE</td><td>88.50</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24250' data-ltp='274.75'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24250</td><td>CE</td><td>274.75</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='24250' data-ltp='338.4'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24250</td><td>CE</td><td>338.40</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24250' data-ltp='99.9'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24250</td><td>CE</td><td>99.90</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24250' data-ltp='200.45'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24250</td><td>CE</td><td>200.45</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24250' data-ltp='146.75'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24250</td><td>PE</td><td>146.75</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='24250' data-ltp='175.05'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24250</td><td>PE</td><td>175.05</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24250' data-ltp='38.85'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24250</td><td>PE</td><td>38.85</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24250' data-ltp='106.5'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24250</td><td>PE</td><td>106.50</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24300' data-ltp='243.35'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24300</td><td>CE</td><td>243.35</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='24300' data-ltp='307.15'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24300</td><td>CE</td><td>307.15</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24300' data-ltp='70.3'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24300</td><td>CE</td><td>70.30</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24300' data-ltp='170.8'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24300</td><td>CE</td><td>170.80</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24300' data-ltp='168.75'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24300</td><td>PE</td><td>168.75</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='24300' data-ltp='201.7'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24300</td><td>PE</td><td>201.70</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24300' data-ltp='59.3'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24300</td><td>PE</td><td>59.30</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24300' data-ltp='127.15'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24300</td><td>PE</td><td>127.15</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24350' data-ltp='216.75'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24350</td><td>CE</td><td>216.75</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='24350' data-ltp='277.5'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24350</td><td>CE</td><td>277.50</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24350' data-ltp='47.65'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24350</td><td>CE</td><td>47.65</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24350' data-ltp='144.2'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24350</td><td>CE</td><td>144.20</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24350' data-ltp='190.75'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24350</td><td>PE</td><td>190.75</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='24350' data-ltp='220.95'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24350</td><td>PE</td><td>220.95</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24350' data-ltp='86.8'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24350</td><td>PE</td><td>86.80</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24350' data-ltp='150.1'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24350</td><td>PE</td><td>150.10</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24400' data-ltp='189.2'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24400</td><td>CE</td><td>189.20</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='24400' data-ltp='251.7'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24400</td><td>CE</td><td>251.70</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24400' data-ltp='31.25'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24400</td><td>CE</td><td>31.25</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24400' data-ltp='119.9'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24400</td><td>CE</td><td>119.90</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24400' data-ltp='215.15'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24400</td><td>PE</td><td>215.15</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='24400' data-ltp='247.4'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24400</td><td>PE</td><td>247.40</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24400' data-ltp='120.75'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24400</td><td>PE</td><td>120.75</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24400' data-ltp='176.55'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24400</td><td>PE</td><td>176.55</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24450' data-ltp='167.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24450</td><td>CE</td><td>167.00</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='24450' data-ltp='231.7'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24450</td><td>CE</td><td>231.70</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24450' data-ltp='20.25'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24450</td><td>CE</td><td>20.25</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24450' data-ltp='99.15'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24450</td><td>CE</td><td>99.15</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24450' data-ltp='238.1'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24450</td><td>PE</td><td>238.10</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='24450' data-ltp='267.0'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24450</td><td>PE</td><td>267.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24450' data-ltp='160.6'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24450</td><td>PE</td><td>160.60</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24450' data-ltp='205.8'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24450</td><td>PE</td><td>205.80</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24500' data-ltp='145.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24500</td><td>CE</td><td>145.00</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='24500' data-ltp='202.05'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24500</td><td>CE</td><td>202.05</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24500' data-ltp='13.45'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24500</td><td>CE</td><td>13.45</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24500' data-ltp='80.5'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24500</td><td>CE</td><td>80.50</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24500' data-ltp='269.25'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24500</td><td>PE</td><td>269.25</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='24500' data-ltp='297.8'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24500</td><td>PE</td><td>297.80</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24500' data-ltp='203.05'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24500</td><td>PE</td><td>203.05</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24500' data-ltp='236.8'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24500</td><td>PE</td><td>236.80</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24550' data-ltp='126.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24550</td><td>CE</td><td>126.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24550' data-ltp='8.8'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24550</td><td>CE</td><td>8.80</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24550' data-ltp='64.9'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24550</td><td>CE</td><td>64.90</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24550' data-ltp='297.1'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24550</td><td>PE</td><td>297.10</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24550' data-ltp='249.05'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24550</td><td>PE</td><td>249.05</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24550' data-ltp='272.2'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24550</td><td>PE</td><td>272.20</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24600' data-ltp='108.4'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24600</td><td>CE</td><td>108.40</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='24600' data-ltp='162.05'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24600</td><td>CE</td><td>162.05</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24600' data-ltp='6.15'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24600</td><td>CE</td><td>6.15</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24600' data-ltp='51.7'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24600</td><td>CE</td><td>51.70</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24600' data-ltp='330.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24600</td><td>PE</td><td>330.00</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='24600' data-ltp='356.0'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24600</td><td>PE</td><td>356.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24600' data-ltp='295.65'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24600</td><td>PE</td><td>295.65</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24600' data-ltp='308.1'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24600</td><td>PE</td><td>308.10</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24650' data-ltp='93.7'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24650</td><td>CE</td><td>93.70</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24650' data-ltp='4.5'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24650</td><td>CE</td><td>4.50</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24650' data-ltp='41.55'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24650</td><td>CE</td><td>41.55</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24650' data-ltp='343.9'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24650</td><td>PE</td><td>343.90</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24650' data-ltp='342.1'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24650</td><td>PE</td><td>342.10</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24700' data-ltp='78.8'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24700</td><td>CE</td><td>78.80</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='24700' data-ltp='125.1'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24700</td><td>CE</td><td>125.10</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24700' data-ltp='3.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24700</td><td>CE</td><td>3.35</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24700' data-ltp='32.35'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24700</td><td>CE</td><td>32.35</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24700' data-ltp='398.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24700</td><td>PE</td><td>398.00</td></tr>
<tr data-expiry='08-Sep-2026' data-type='PE' data-strike='24700' data-ltp='417.0'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24700</td><td>PE</td><td>417.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24700' data-ltp='393.0'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24700</td><td>PE</td><td>393.00</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24700' data-ltp='387.75'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24700</td><td>PE</td><td>387.75</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24750' data-ltp='67.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24750</td><td>CE</td><td>67.00</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='24750' data-ltp='112.2'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24750</td><td>CE</td><td>112.20</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24750' data-ltp='2.65'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24750</td><td>CE</td><td>2.65</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24750' data-ltp='25.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24750</td><td>CE</td><td>25.65</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24750' data-ltp='432.25'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24750</td><td>PE</td><td>432.25</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24750' data-ltp='438.5'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24750</td><td>PE</td><td>438.50</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24750' data-ltp='424.5'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24750</td><td>PE</td><td>424.50</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24800' data-ltp='56.75'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24800</td><td>CE</td><td>56.75</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='24800' data-ltp='97.1'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>24800</td><td>CE</td><td>97.10</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24800' data-ltp='2.2'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24800</td><td>CE</td><td>2.20</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24800' data-ltp='19.95'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24800</td><td>CE</td><td>19.95</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24800' data-ltp='474.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24800</td><td>PE</td><td>474.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24800' data-ltp='491.0'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24800</td><td>PE</td><td>491.00</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24800' data-ltp='475.95'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24800</td><td>PE</td><td>475.95</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24850' data-ltp='48.3'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24850</td><td>CE</td><td>48.30</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24850' data-ltp='1.95'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24850</td><td>CE</td><td>1.95</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24850' data-ltp='15.95'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24850</td><td>CE</td><td>15.95</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24850' data-ltp='529.6'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24850</td><td>PE</td><td>529.60</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24850' data-ltp='518.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24850</td><td>PE</td><td>518.65</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24900' data-ltp='40.2'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24900</td><td>CE</td><td>40.20</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24900' data-ltp='1.7'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24900</td><td>CE</td><td>1.70</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24900' data-ltp='12.85'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24900</td><td>CE</td><td>12.85</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='24900' data-ltp='543.8'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24900</td><td>PE</td><td>543.80</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24900' data-ltp='589.1'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24900</td><td>PE</td><td>589.10</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24900' data-ltp='568.5'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24900</td><td>PE</td><td>568.50</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='24950' data-ltp='35.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>24950</td><td>CE</td><td>35.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='24950' data-ltp='1.55'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24950</td><td>CE</td><td>1.55</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='24950' data-ltp='10.35'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24950</td><td>CE</td><td>10.35</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='24950' data-ltp='635.25'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>24950</td><td>PE</td><td>635.25</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='24950' data-ltp='605.0'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>24950</td><td>PE</td><td>605.00</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='25000' data-ltp='27.9'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25000</td><td>CE</td><td>27.90</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='25000' data-ltp='55.95'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>25000</td><td>CE</td><td>55.95</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25000' data-ltp='1.4'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25000</td><td>CE</td><td>1.40</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25000' data-ltp='8.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25000</td><td>CE</td><td>8.65</td></tr>
<tr data-expiry='01-Sep-2026' data-type='PE' data-strike='25000' data-ltp='648.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25000</td><td>PE</td><td>648.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='25000' data-ltp='689.55'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25000</td><td>PE</td><td>689.55</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='25000' data-ltp='664.0'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25000</td><td>PE</td><td>664.00</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='25050' data-ltp='23.6'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25050</td><td>CE</td><td>23.60</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25050' data-ltp='1.3'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25050</td><td>CE</td><td>1.30</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25050' data-ltp='6.75'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25050</td><td>CE</td><td>6.75</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='25050' data-ltp='739.75'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25050</td><td>PE</td><td>739.75</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='25100' data-ltp='19.3'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25100</td><td>CE</td><td>19.30</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='25100' data-ltp='40.4'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>25100</td><td>CE</td><td>40.40</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25100' data-ltp='1.2'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25100</td><td>CE</td><td>1.20</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25100' data-ltp='5.55'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25100</td><td>CE</td><td>5.55</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='25100' data-ltp='785.1'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25100</td><td>PE</td><td>785.10</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='25100' data-ltp='749.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25100</td><td>PE</td><td>749.65</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25150' data-ltp='1.1'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25150</td><td>CE</td><td>1.10</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25150' data-ltp='4.7'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25150</td><td>CE</td><td>4.70</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='25200' data-ltp='14.45'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25200</td><td>CE</td><td>14.45</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25200' data-ltp='1.05'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25200</td><td>CE</td><td>1.05</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25200' data-ltp='4.2'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25200</td><td>CE</td><td>4.20</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='25200' data-ltp='884.9'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25200</td><td>PE</td><td>884.90</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='25200' data-ltp='855.4'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25200</td><td>PE</td><td>855.40</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25250' data-ltp='1.05'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25250</td><td>CE</td><td>1.05</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25250' data-ltp='3.6'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25250</td><td>CE</td><td>3.60</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='25300' data-ltp='21.4'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>25300</td><td>CE</td><td>21.40</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25300' data-ltp='0.95'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25300</td><td>CE</td><td>0.95</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25300' data-ltp='3.2'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25300</td><td>CE</td><td>3.20</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='25300' data-ltp='979.85'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25300</td><td>PE</td><td>979.85</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='25300' data-ltp='955.45'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25300</td><td>PE</td><td>955.45</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25350' data-ltp='0.9'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25350</td><td>CE</td><td>0.90</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25350' data-ltp='2.8'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25350</td><td>CE</td><td>2.80</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='25400' data-ltp='7.25'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25400</td><td>CE</td><td>7.25</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25400' data-ltp='0.8'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25400</td><td>CE</td><td>0.80</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25400' data-ltp='2.5'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25400</td><td>CE</td><td>2.50</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='25400' data-ltp='1088.75'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25400</td><td>PE</td><td>1,088.75</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='25400' data-ltp='1045.95'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25400</td><td>PE</td><td>1,045.95</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25450' data-ltp='0.8'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25450</td><td>CE</td><td>0.80</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25450' data-ltp='2.3'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25450</td><td>CE</td><td>2.30</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='25500' data-ltp='5.95'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25500</td><td>CE</td><td>5.95</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25500' data-ltp='0.7'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25500</td><td>CE</td><td>0.70</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25500' data-ltp='2.1'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25500</td><td>CE</td><td>2.10</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='25500' data-ltp='1190.0'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25500</td><td>PE</td><td>1,190.00</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='25500' data-ltp='1154.85'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25500</td><td>PE</td><td>1,154.85</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='25550' data-ltp='5.65'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25550</td><td>CE</td><td>5.65</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25550' data-ltp='0.7'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25550</td><td>CE</td><td>0.70</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25550' data-ltp='1.85'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25550</td><td>CE</td><td>1.85</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='25600' data-ltp='9.8'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>25600</td><td>CE</td><td>9.80</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25600' data-ltp='0.6'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25600</td><td>CE</td><td>0.60</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25600' data-ltp='1.45'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25600</td><td>CE</td><td>1.45</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='25650' data-ltp='4.75'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25650</td><td>CE</td><td>4.75</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25650' data-ltp='0.65'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25650</td><td>CE</td><td>0.65</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25650' data-ltp='1.4'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25650</td><td>CE</td><td>1.40</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='25700' data-ltp='4.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25700</td><td>CE</td><td>4.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25700' data-ltp='0.6'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25700</td><td>CE</td><td>0.60</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25700' data-ltp='1.15'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25700</td><td>CE</td><td>1.15</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='25750' data-ltp='4.0'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25750</td><td>CE</td><td>4.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25750' data-ltp='0.55'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25750</td><td>CE</td><td>0.55</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25750' data-ltp='1.15'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25750</td><td>CE</td><td>1.15</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='25750' data-ltp='1256.7'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25750</td><td>PE</td><td>1,256.70</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='25800' data-ltp='3.45'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25800</td><td>CE</td><td>3.45</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25800' data-ltp='0.5'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25800</td><td>CE</td><td>0.50</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25800' data-ltp='1.05'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25800</td><td>CE</td><td>1.05</td></tr>
<tr data-expiry='18-Aug-2026' data-type='PE' data-strike='25800' data-ltp='1485.0'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25800</td><td>PE</td><td>1,485.00</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='25800' data-ltp='1440.0'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25800</td><td>PE</td><td>1,440.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25850' data-ltp='0.5'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25850</td><td>CE</td><td>0.50</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25850' data-ltp='0.9'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25850</td><td>CE</td><td>0.90</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='25900' data-ltp='3.2'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>25900</td><td>CE</td><td>3.20</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25900' data-ltp='0.45'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25900</td><td>CE</td><td>0.45</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25900' data-ltp='0.85'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25900</td><td>CE</td><td>0.85</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='25950' data-ltp='0.5'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>25950</td><td>CE</td><td>0.50</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='25950' data-ltp='0.9'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>25950</td><td>CE</td><td>0.90</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='26000' data-ltp='2.95'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>26000</td><td>CE</td><td>2.95</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='26000' data-ltp='4.75'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>26000</td><td>CE</td><td>4.75</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26000' data-ltp='0.45'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26000</td><td>CE</td><td>0.45</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26000' data-ltp='0.95'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26000</td><td>CE</td><td>0.95</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='26000' data-ltp='1656.0'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26000</td><td>PE</td><td>1,656.00</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26050' data-ltp='0.5'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26050</td><td>CE</td><td>0.50</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26050' data-ltp='0.75'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26050</td><td>CE</td><td>0.75</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='26100' data-ltp='4.05'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>26100</td><td>CE</td><td>4.05</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26100' data-ltp='0.45'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26100</td><td>CE</td><td>0.45</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26100' data-ltp='0.75'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26100</td><td>CE</td><td>0.75</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='26150' data-ltp='3.45'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>26150</td><td>CE</td><td>3.45</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26150' data-ltp='0.5'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26150</td><td>CE</td><td>0.50</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26150' data-ltp='0.7'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26150</td><td>CE</td><td>0.70</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='26200' data-ltp='2.35'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>26200</td><td>CE</td><td>2.35</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='26200' data-ltp='3.5'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>26200</td><td>CE</td><td>3.50</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26200' data-ltp='0.45'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26200</td><td>CE</td><td>0.45</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26200' data-ltp='0.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26200</td><td>CE</td><td>0.65</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='26250' data-ltp='3.05'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>26250</td><td>CE</td><td>3.05</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26250' data-ltp='0.5'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26250</td><td>CE</td><td>0.50</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26250' data-ltp='0.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26250</td><td>CE</td><td>0.65</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='26300' data-ltp='2.55'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>26300</td><td>CE</td><td>2.55</td></tr>
<tr data-expiry='08-Sep-2026' data-type='CE' data-strike='26300' data-ltp='2.65'><td>17 Aug 2026 09:31 IST</td><td>08-Sep-2026</td><td>26300</td><td>CE</td><td>2.65</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26300' data-ltp='0.45'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26300</td><td>CE</td><td>0.45</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26300' data-ltp='0.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26300</td><td>CE</td><td>0.65</td></tr>
<tr data-expiry='25-Aug-2026' data-type='PE' data-strike='26300' data-ltp='1951.85'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26300</td><td>PE</td><td>1,951.85</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26350' data-ltp='0.4'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26350</td><td>CE</td><td>0.40</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26400' data-ltp='0.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26400</td><td>CE</td><td>0.35</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26400' data-ltp='0.6'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26400</td><td>CE</td><td>0.60</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26450' data-ltp='0.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26450</td><td>CE</td><td>0.35</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26500' data-ltp='0.3'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26500</td><td>CE</td><td>0.30</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26500' data-ltp='0.65'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26500</td><td>CE</td><td>0.65</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26550' data-ltp='0.4'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26550</td><td>CE</td><td>0.40</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26550' data-ltp='0.75'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26550</td><td>CE</td><td>0.75</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26600' data-ltp='0.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26600</td><td>CE</td><td>0.35</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26600' data-ltp='0.55'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26600</td><td>CE</td><td>0.55</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26650' data-ltp='0.3'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26650</td><td>CE</td><td>0.30</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26700' data-ltp='0.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26700</td><td>CE</td><td>0.35</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26700' data-ltp='0.55'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26700</td><td>CE</td><td>0.55</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='26750' data-ltp='1.9'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>26750</td><td>CE</td><td>1.90</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26750' data-ltp='0.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26750</td><td>CE</td><td>0.35</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26800' data-ltp='0.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26800</td><td>CE</td><td>0.35</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26800' data-ltp='0.6'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26800</td><td>CE</td><td>0.60</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26850' data-ltp='0.4'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26850</td><td>CE</td><td>0.40</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26900' data-ltp='0.4'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26900</td><td>CE</td><td>0.40</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='26900' data-ltp='0.6'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>26900</td><td>CE</td><td>0.60</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='26950' data-ltp='0.4'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>26950</td><td>CE</td><td>0.40</td></tr>
<tr data-expiry='01-Sep-2026' data-type='CE' data-strike='27000' data-ltp='1.75'><td>17 Aug 2026 09:31 IST</td><td>01-Sep-2026</td><td>27000</td><td>CE</td><td>1.75</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='27000' data-ltp='0.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>27000</td><td>CE</td><td>0.35</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='27000' data-ltp='0.6'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>27000</td><td>CE</td><td>0.60</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='27050' data-ltp='0.4'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>27050</td><td>CE</td><td>0.40</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='27100' data-ltp='0.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>27100</td><td>CE</td><td>0.35</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='27150' data-ltp='0.3'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>27150</td><td>CE</td><td>0.30</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='27150' data-ltp='0.55'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>27150</td><td>CE</td><td>0.55</td></tr>
<tr data-expiry='18-Aug-2026' data-type='CE' data-strike='27200' data-ltp='0.35'><td>17 Aug 2026 09:31 IST</td><td>18-Aug-2026</td><td>27200</td><td>CE</td><td>0.35</td></tr>
<tr data-expiry='25-Aug-2026' data-type='CE' data-strike='27200' data-ltp='0.8'><td>17 Aug 2026 09:31 IST</td><td>25-Aug-2026</td><td>27200</td><td>CE</td><td>0.80</td></tr>
</table>

---

