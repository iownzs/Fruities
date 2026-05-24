from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<script id="kitchen-send-create-delivery-v2">
(function(){
  if(window.__kitchenSendCreateDeliveryV2) return;
  window.__kitchenSendCreateDeliveryV2 = true;

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

  function isDeliveryOrder(o){
    var type = String(o.orderType || o.fulfillmentType || '').toLowerCase();
    return (
      type === 'delivery' ||
      o.deliveryAddress ||
      o.addr ||
      o.recipient ||
      o.recipientPhone
    );
  }

  function makeDeliveryId(orderId){
    return 'DEL-' + String(orderId || Date.now()).replace(/^ORD-/,'').replace(/^DEL-/,'');
  }

  function findDeliveryByOrder(orderId){
    return getDeliveries().find(function(d){
      return (
        String(d.orderId || '') === String(orderId) ||
        String(d.oid || '') === String(orderId) ||
        String(d.order || '') === String(orderId) ||
        String(d.id || '') === String(makeDeliveryId(orderId))
      );
    }) || null;
  }

  function createOrUpdateDeliveryFromOrder(orderId){
    var o = findOrder(orderId);
    if(!o) return null;
    if(isPickupOrder(o)) return null;
    if(!isDeliveryOrder(o)) return null;

    var oid = o.id || o.orderNumber || o.orderId || orderId;
    var now = Date.now();

    o.kitStatus = 'out';
    o.kitchenStatus = 'out';
    o.deliveryStatus = o.deliveryStatus === 'delivered' ? 'delivered' : 'waiting';
    o.pickupStatus = 'none';
    o.sentToDeliveryAt = o.sentToDeliveryAt || now;
    o.deliverySentAt = o.deliverySentAt || now;
    o.kitOutAt = o.kitOutAt || now;

    var d = findDeliveryByOrder(oid);

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
      d.status = d.status === 'delivered' ? 'delivered' : 'waiting';
      d.deliveryStatus = d.deliveryStatus === 'delivered' ? 'delivered' : 'waiting';
      d.sentToDeliveryAt = d.sentToDeliveryAt || now;
      d.deliverySentAt = d.deliverySentAt || now;
      d.items = d.items || o.items || [];
      d.total = d.total || o.total || 0;
    }

    return d;
  }

  function wrapKitAction(){
    if(typeof window.kitAction !== 'function') return false;
    if(window.kitAction.__createDeliveryV2) return true;

    var oldKitAction = window.kitAction;

    window.kitAction = function(id, action){
      var result = oldKitAction.apply(this, arguments);

      if(String(action) === 'out'){
        setTimeout(function(){
          var d = createOrUpdateDeliveryFromOrder(id);

          try{ if(typeof sv === 'function') sv(); }catch(e){}
          try{ if(typeof toast === 'function' && d) toast('🚚 Sent to Delivery'); }catch(e){}
          try{ if(typeof rKitchen === 'function') rKitchen(); }catch(e){}
          try{ if(typeof renderDeliveryExcel === 'function') renderDeliveryExcel(); }catch(e){}
        }, 120);
      }

      return result;
    };

    window.kitAction.__createDeliveryV2 = true;

    try{ kitAction = window.kitAction; }catch(e){}

    return true;
  }

  setTimeout(wrapKitAction, 300);
  setTimeout(wrapKitAction, 1000);
  setTimeout(wrapKitAction, 2500);
})();
</script>
'''

if "kitchen-send-create-delivery-v2" in html:
    print("Kitchen send create delivery patch already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Kitchen Send Delivery now creates delivery record.")
