from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<script id="pickup-instead-removes-delivery-v1">
(function(){
  if(window.__pickupInsteadRemovesDeliveryV1) return;
  window.__pickupInsteadRemovesDeliveryV1 = true;

  function getOrders(){
    return window.S && Array.isArray(S.orders) ? S.orders : [];
  }

  function findOrder(id){
    try{
      if(typeof orderById === 'function') return orderById(id);
    }catch(e){}

    return getOrders().find(function(o){
      return String(o.id || o.orderNumber || o.orderId) === String(id);
    }) || null;
  }

  function deliveryIdFor(orderId){
    return 'DEL-' + String(orderId || '').replace(/^ORD-/,'').replace(/^DEL-/,'');
  }

  function removeDeliveryRecord(orderId){
    if(!window.S || !Array.isArray(S.deliveries)) return;

    var delId = deliveryIdFor(orderId);

    S.deliveries = S.deliveries.filter(function(d){
      return !(
        String(d.id || '') === String(delId) ||
        String(d.orderId || '') === String(orderId) ||
        String(d.oid || '') === String(orderId) ||
        String(d.order || '') === String(orderId)
      );
    });
  }

  function forcePickupState(orderId){
    var o = findOrder(orderId);
    if(!o) return;

    // Mark as pickup flow
    o.fulfillmentType = 'pickup';
    o.orderType = 'pickup';
    o.kitForPickup = true;
    o.kitPickup = false;
    o.pickupStatus = 'waiting';

    // Clear delivery flow
    o.deliveryStatus = 'none';
    o.rider = '';
    o.riderName = '';
    o.riderNotes = '';
    o.outForDeliveryAt = '';
    o.deliveryOutAt = '';
    o.deliveryDeliveredAt = '';

    removeDeliveryRecord(o.id || o.orderNumber || o.orderId || orderId);

    try{ if(typeof sv === 'function') sv(); }catch(e){}
    try{ if(typeof rPickup === 'function') rPickup(); }catch(e){}
    try{ if(typeof renderDeliveryExcel === 'function') renderDeliveryExcel(); }catch(e){}
  }

  function wrapKitSendToPickup(){
    if(typeof window.kitSendToPickup !== 'function') return false;
    if(window.kitSendToPickup.__pickupInsteadRemovesDeliveryV1) return true;

    var oldFn = window.kitSendToPickup;

    window.kitSendToPickup = function(id){
      var result = oldFn.apply(this, arguments);

      setTimeout(function(){
        forcePickupState(id);
      }, 100);

      return result;
    };

    window.kitSendToPickup.__pickupInsteadRemovesDeliveryV1 = true;

    try{ kitSendToPickup = window.kitSendToPickup; }catch(e){}

    return true;
  }

  setTimeout(wrapKitSendToPickup, 300);
  setTimeout(wrapKitSendToPickup, 1000);
  setTimeout(wrapKitSendToPickup, 2500);
})();
</script>
'''

if "pickup-instead-removes-delivery-v1" in html:
    print("Pickup instead delivery cleanup already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Pickup Instead now removes delivery state/record.")
