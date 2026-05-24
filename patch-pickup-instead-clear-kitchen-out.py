from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

old = r'''    // Mark as pickup flow
    o.fulfillmentType = 'pickup';
    o.orderType = 'pickup';
    o.kitForPickup = true;
    o.kitPickup = false;
    o.pickupStatus = 'waiting';'''

new = r'''    // Mark as pickup flow
    o.fulfillmentType = 'pickup';
    o.orderType = 'pickup';
    o.kitForPickup = true;
    o.kitPickup = false;
    o.pickupStatus = 'waiting';

    // Important: no longer treat as Kitchen sent-to-delivery.
    o.kitchenStatus = 'sent_to_pickup';
    o.kitStatus = 'out';'''

if old not in html:
    print("Pickup state block not found or already patched.")
else:
    html = html.replace(old, new, 1)
    p.write_text(html, encoding="utf-8")
    print("DONE: Pickup Instead clears delivery qualification.")
