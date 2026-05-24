from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

old = r'''  function deliveries(){
    if(window.S && Array.isArray(S.deliveries) && S.deliveries.length){
      return S.deliveries;
    }

    return orders()
      .filter(function(o){
        return (
          o.orderType === 'delivery' ||
          o.fulfillmentType === 'delivery' ||
          o.deliveryStatus ||
          o.deliveryAddress ||
          o.addr
        );
      })
      .map(function(o){
        return {
          id: o.id || o.orderNumber || o.orderId,
          orderId: o.id || o.orderNumber || o.orderId,
          status: o.deliveryStatus || 'waiting',
          deliveryStatus: o.deliveryStatus || 'waiting',
          rider: o.rider || '',
          riderName: o.riderName || '',
          createdAt: o.createdAt || o.time,
          items: o.items || [],
          total: o.total || 0
        };
      });
  }'''

new = r'''  function isDeliveryOrder(o){
    var type = String(o.orderType || o.fulfillmentType || o.type || '').toLowerCase();
    return (
      type === 'delivery' ||
      o.deliveryAddress ||
      o.addr ||
      o.recipient ||
      o.recipientPhone
    );
  }

  function isSentToDelivery(o,d){
    var ks = String(o.kitchenStatus || o.kitStatus || '').toLowerCase();
    var ds = String(o.deliveryStatus || d.deliveryStatus || d.status || '').toLowerCase();

    // Already active/completed delivery should remain visible.
    if(ds === 'out_for_delivery' || ds === 'out' || ds === 'delivered') return true;
    if(o.rider || o.riderName || d.rider || d.riderName) return true;
    if(o.deliveredAt || d.deliveredAt || o.outForDeliveryAt || o.deliveryOutAt) return true;

    // Only waiting orders that Kitchen actually sent should appear.
    if(
      ks === 'sent_to_delivery' ||
      ks === 'out' ||
      ks === 'delivery' ||
      o.sentToDeliveryAt ||
      o.deliverySentAt ||
      o.deliverySyncedAt ||
      d.sentToDeliveryAt ||
      d.deliverySentAt
    ){
      return true;
    }

    return false;
  }

  function deliveries(){
    var list = [];

    if(window.S && Array.isArray(S.deliveries) && S.deliveries.length){
      list = S.deliveries.filter(function(d){
        var o = orderOf(d);
        return isDeliveryOrder(o) && isSentToDelivery(o,d);
      });

      return list;
    }

    return orders()
      .filter(function(o){
        return isDeliveryOrder(o) && isSentToDelivery(o,{});
      })
      .map(function(o){
        return {
          id: 'DEL-' + String(o.id || o.orderNumber || o.orderId).replace(/^ORD-/,'').replace(/^DEL-/,''),
          orderId: o.id || o.orderNumber || o.orderId,
          oid: o.id || o.orderNumber || o.orderId,
          status: o.deliveryStatus || 'waiting',
          deliveryStatus: o.deliveryStatus || 'waiting',
          rider: o.rider || '',
          riderName: o.riderName || '',
          createdAt: o.createdAt || o.time,
          items: o.items || [],
          total: o.total || 0
        };
      });
  }'''

if old not in html:
    print("Exact deliveries() block not found. Trying regex replace...")
    pattern = r"  function deliveries\(\)\{.*?\n  \}\n\n  function orderOf"
    repl = new + "\n\n  function orderOf"
    html2, count = re.subn(pattern, repl, html, count=1, flags=re.S)
    if count != 1:
      print("FAILED: could not patch deliveries()")
      raise SystemExit(1)
    html = html2
else:
    html = html.replace(old, new, 1)

p.write_text(html, encoding="utf-8")
print("DONE: Delivery tab now shows only orders sent to delivery.")
