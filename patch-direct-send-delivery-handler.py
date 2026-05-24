from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<script id="direct-send-delivery-handler-v3">
(function(){
  if(window.__directSendDeliveryHandlerV3) return;
  window.__directSendDeliveryHandlerV3 = true;

  function getOrders(){
    return window.S && Array.isArray(S.orders) ? S.orders : [];
  }

  function getDeliveries(){
    if(!window.S) window.S = {};
    if(!Array.isArray(S.deliveries)) S.deliveries = [];
    return S.deliveries;
  }

  function findOrder(id){
    try{
      if(typeof orderById === 'function') return orderById(id);
    }catch(e){}

    return getOrders().find(function(o){
      return String(o.id || o.orderNumber || o.orderId) === String(id);
    }) || null;
  }

  function isPickupOrder(o){
    var type = String(o.orderType || o.fulfillmentType || '').toLowerCase();
    return (
      type === 'pickup' ||
      o.kitForPickup ||
      o.kitPickup ||
      o.pickupStatus === 'waiting' ||
      o.pickupStatus === 'picked_up'
    );
  }

  function makeDeliveryId(orderId){
    return 'DEL-' + String(orderId || Date.now()).replace(/^ORD-/,'').replace(/^DEL-/,'');
  }

  function findDelivery(orderId){
    var delId = makeDeliveryId(orderId);
    return getDeliveries().find(function(d){
      return (
        String(d.id || '') === String(delId) ||
        String(d.orderId || '') === String(orderId) ||
        String(d.oid || '') === String(orderId) ||
        String(d.order || '') === String(orderId)
      );
    }) || null;
  }

  window.directSendDelivery = function(orderId){
    var o = findOrder(orderId);

    if(!o){
      alert('Order not found: ' + orderId);
      return;
    }

    if(isPickupOrder(o)){
      alert('This is a pickup order. Use For Pickup instead.');
      return;
    }

    var now = Date.now();
    var oid = o.id || o.orderNumber || o.orderId || orderId;

    // Follow your current Kitchen output
    o.kitStatus = 'out';
    o.kitchenStatus = 'out';

    // Delivery waiting state
    o.deliveryStatus = 'waiting';
    o.pickupStatus = 'none';
    o.sentToDeliveryAt = o.sentToDeliveryAt || now;
    o.deliverySentAt = o.deliverySentAt || now;
    o.kitOutAt = o.kitOutAt || now;

    var d = findDelivery(oid);

    if(!d){
      d = {
        id: makeDeliveryId(oid),
        oid: oid,
        orderId: oid,
        order: oid,
        status: 'waiting',
        deliveryStatus: 'waiting',
        rider: '',
        riderName: '',
        createdAt: o.createdAt || o.time || new Date().toISOString(),
        sentToDeliveryAt: now,
        deliverySentAt: now,
        items: o.items || [],
        total: o.total || 0
      };
      getDeliveries().push(d);
    }else{
      d.oid = d.oid || oid;
      d.orderId = d.orderId || oid;
      d.order = d.order || oid;
      d.status = 'waiting';
      d.deliveryStatus = 'waiting';
      d.sentToDeliveryAt = d.sentToDeliveryAt || now;
      d.deliverySentAt = d.deliverySentAt || now;
      d.items = d.items || o.items || [];
      d.total = d.total || o.total || 0;
    }

    try{ if(typeof sv === 'function') sv(); }catch(e){}
    try{ if(typeof toast === 'function') toast('🚚 Sent to Delivery'); }catch(e){}
    try{ if(typeof rKitchen === 'function') rKitchen(); }catch(e){}
    try{ if(typeof renderDeliveryExcel === 'function') renderDeliveryExcel(); }catch(e){}

    return d;
  };

  document.addEventListener('click', function(e){
    var btn = e.target && e.target.closest ? e.target.closest('button') : null;
    if(!btn) return;

    var txt = (btn.textContent || '').trim();
    if(txt.indexOf('Send Delivery') === -1 && txt.indexOf('Send to Delivery') === -1) return;

    var onclick = btn.getAttribute('onclick') || '';
    var match = onclick.match(/kitAction\(['"]([^'"]+)['"]\s*,\s*['"]out['"]\)/);

    if(!match) return;

    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();

    window.directSendDelivery(match[1]);
  }, true);
})();
</script>
'''

if "direct-send-delivery-handler-v3" in html:
    print("Direct Send Delivery handler already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Direct Send Delivery handler added.")
