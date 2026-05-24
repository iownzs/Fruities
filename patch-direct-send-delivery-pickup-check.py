from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

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

    // For Send Delivery, only block clearly explicit pickup orders.
    // Do not block because of old kitForPickup / pickupStatus fields.
    return type === 'pickup';
  }'''

count = html.count(old)

if count == 0:
    print("Target pickup check not found. Showing direct handler area:")
    idx = html.find("direct-send-delivery-handler-v3")
    print(html[idx:idx+1400])
    raise SystemExit(1)

html = html.replace(old, new, 1)
p.write_text(html, encoding="utf-8")
print("DONE: Direct Send Delivery pickup check fixed.")
