from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

old = r'''  function deliveries(){
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

new = r'''  function deliveryFromOrder(o){
    var oid = o.id || o.orderNumber || o.orderId;
    return {
      id: 'DEL-' + String(oid || '').replace(/^ORD-/,'').replace(/^DEL-/,''),
      orderId: oid,
      oid: oid,
      status: o.deliveryStatus || 'waiting',
      deliveryStatus: o.deliveryStatus || 'waiting',
      rider: o.rider || '',
      riderName: o.riderName || '',
      createdAt: o.createdAt || o.time,
      items: o.items || [],
      total: o.total || 0,
      sentToDeliveryAt: o.sentToDeliveryAt || o.deliverySentAt || o.kitOutAt || ''
    };
  }

  function deliveries(){
    var existing = (window.S && Array.isArray(S.deliveries)) ? S.deliveries : [];
    var result = [];

    existing.forEach(function(d){
      var o = orderOf(d);
      if(isDeliveryOrder(o) && isSentToDelivery(o,d)){
        result.push(d);
      }
    });

    var seen = {};
    result.forEach(function(d){
      var oid = d.orderId || d.oid || d.order || d.id;
      if(oid) seen[String(oid)] = true;
      if(d.id) seen[String(d.id)] = true;
    });

    orders().forEach(function(o){
      var oid = o.id || o.orderNumber || o.orderId;
      if(!oid) return;

      if(seen[String(oid)]) return;
      if(seen['DEL-' + String(oid).replace(/^ORD-/,'').replace(/^DEL-/,'')]) return;

      if(isDeliveryOrder(o) && isSentToDelivery(o,{})){
        result.push(deliveryFromOrder(o));
      }
    });

    return result;
  }'''

if old not in html:
    print("Exact deliveries() block not found. Trying regex.")
    pattern = r"  function deliveries\(\)\{.*?\n  \}\n\n  function orderOf"
    repl = new + "\n\n  function orderOf"
    html2, count = re.subn(pattern, repl, html, count=1, flags=re.S)
    if count != 1:
      print("FAILED: Could not patch deliveries().")
      raise SystemExit(1)
    html = html2
else:
    html = html.replace(old, new, 1)

p.write_text(html, encoding="utf-8")
print("DONE: Delivery Excel now merges sent Kitchen orders from S.orders.")
