from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

old = r'''  function isDeliveryOrder(o){
    var type = String(o.orderType || o.fulfillmentType || o.type || '').toLowerCase();
    return (
      type === 'delivery' ||
      o.deliveryAddress ||
      o.addr ||
      o.recipient ||
      o.recipientPhone
    );
  }'''

new = r'''  function isPickupFlow(o){
    var type = String(o.orderType || o.fulfillmentType || o.type || '').toLowerCase();

    return (
      type === 'pickup' ||
      o.pickupStatus === 'waiting' ||
      o.pickupStatus === 'picked_up' ||
      o.kitForPickup === true ||
      o.kitPickup === true
    );
  }

  function isDeliveryOrder(o){
    if(!o) return false;

    // Pickup flow should never appear in Delivery tab,
    // even if old delivery/address fields still exist.
    if(isPickupFlow(o)) return false;

    var type = String(o.orderType || o.fulfillmentType || o.type || '').toLowerCase();

    return (
      type === 'delivery' ||
      o.deliveryAddress ||
      o.addr ||
      o.recipient ||
      o.recipientPhone
    );
  }'''

if old not in html:
    print("Exact isDeliveryOrder block not found. Showing nearby:")
    idx = html.find("function isDeliveryOrder")
    print(html[idx:idx+700])
    raise SystemExit(1)

html = html.replace(old, new, 1)

p.write_text(html, encoding="utf-8")
print("DONE: Delivery tab now excludes pickup-flow orders.")
