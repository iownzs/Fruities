from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

old = r'''    var id = d.id || d.orderId || o.id || o.orderNumber || '-';'''

new = r'''    var realOrderId = o.id || o.orderNumber || o.orderId || d.orderId || d.oid || d.order || d.id || '-';
    var id = String(realOrderId).startsWith('DEL-')
      ? 'ORD-' + String(realOrderId).replace(/^DEL-/,'')
      : realOrderId;'''

if old not in html:
    print("Target id line not found.")
    raise SystemExit(1)

html = html.replace(old, new, 1)
p.write_text(html, encoding="utf-8")
print("DONE: Delivery table now displays ORD number.")
