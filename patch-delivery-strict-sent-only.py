from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

old = r'''      ks === 'sent_to_delivery' ||
      ks === 'out' ||
      ks === 'delivery' ||
      o.sentToDeliveryAt ||
      o.deliverySentAt ||
      o.deliverySyncedAt ||
      d.sentToDeliveryAt ||
      d.deliverySentAt'''

new = r'''      ks === 'sent_to_delivery' ||
      o.sentToDeliveryAt ||
      o.deliverySentAt ||
      d.sentToDeliveryAt ||
      d.deliverySentAt'''

if old not in html:
    print("Target block not found. Checking current isSentToDelivery block:")
    idx = html.find("function isSentToDelivery")
    print(html[idx:idx+900])
    raise SystemExit(1)

html = html.replace(old, new, 1)
p.write_text(html, encoding="utf-8")
print("DONE: Delivery waiting orders now require Send to Delivery.")
