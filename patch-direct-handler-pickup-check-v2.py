from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

start = html.find('<script id="direct-send-delivery-handler-v3">')
end = html.find('</script>', start)

if start == -1 or end == -1:
    print("FAILED: direct-send-delivery-handler-v3 not found")
    raise SystemExit(1)

block = html[start:end]

old = r'''  function isPickupOrder(o){
    var type = String(o.orderType || o.fulfillmentType || '').toLowerCase();
    return (
      type === 'pickup' ||
      o.kitForPickup ||
      o.kitPickup ||
      o.pickupStatus === 'waiting' ||
      o.pickupStatus === 'picked_up'
    );
  }'''

new = r'''  function isPickupOrder(o){
    var type = String(o.orderType || o.fulfillmentType || '').toLowerCase();

    // Direct Send Delivery button is only shown on delivery cards.
    // Block only explicit pickup type, not old pickup flags.
    return type === 'pickup';
  }'''

if old not in block:
    print("FAILED: old pickup block not found inside direct handler. Showing handler pickup area:")
    m = re.search(r"function isPickupOrder\(o\).*?\n  \}", block, re.S)
    print(m.group(0) if m else block[:1200])
    raise SystemExit(1)

block = block.replace(old, new, 1)
html = html[:start] + block + html[end:]

p.write_text(html, encoding="utf-8")
print("DONE: direct handler pickup check patched.")
