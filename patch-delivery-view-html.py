from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

new_delivery = r'''
    <!-- DELIVERY -->
    <div class="view" id="view-delivery">
      <div class="sh">
        <div>
          <h2>🚚 Delivery</h2>
          <div style="font-size:12px;color:var(--t3);margin-top:2px">Excel-style delivery dispatch board</div>
        </div>
        <button class="btn bg bsm" onclick="renderDeliveryExcel()">↻ Refresh</button>
      </div>

      <div id="deliveryExcelRoot" class="dx-wrap">
        <div class="dx-empty">Loading delivery board...</div>
      </div>
    </div>

    <!-- PICK UP -->'''

pattern = r'''    <!-- DELIVERY -->.*?    <!-- PICK UP -->'''

new_html, count = re.subn(pattern, new_delivery, html, count=1, flags=re.S)

if count != 1:
    print("FAILED: Could not replace Delivery section. Match count:", count)
    raise SystemExit(1)

p.write_text(new_html, encoding="utf-8")
print("DONE: Replaced old Delivery tab HTML with Excel root.")
