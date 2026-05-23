from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<script id="delivery-assign-done-fix-v11">
(function(){
  if(window.__deliveryAssignDoneFixV11) return;
  window.__deliveryAssignDoneFixV11 = true;

  function getOrders(){
    return window.S && Array.isArray(S.orders) ? S.orders : [];
  }

  function getDeliveries(){
    if(!window.S) window.S = {};
    if(!Array.isArray(S.deliveries)) S.deliveries = [];
    return S.deliveries;
  }

  function findOrder(id){
    return getOrders().find(function(o){
      return String(o.id || o.orderNumber || o.orderId) === String(id);
    }) || null;
  }

  function findDelivery(delId, orderId){
    return getDeliveries().find(function(d){
      return (
        String(d.id || '') === String(delId || '') ||
        String(d.orderId || d.oid || d.order || '') === String(orderId || '')
      );
    }) || null;
  }

  function ensureDelivery(delId, orderId){
    var d = findDelivery(delId, orderId);
    if(d) return d;

    var o = findOrder(orderId || delId);
    if(!o) return null;

    var newId = delId && String(delId).startsWith('DEL-')
      ? delId
      : 'DEL-' + String(o.id || o.orderNumber || orderId || Date.now()).replace(/^ORD-/,'').replace(/^DEL-/,'');

    d = {
      id: newId,
      oid: o.id || o.orderNumber || orderId,
      orderId: o.id || o.orderNumber || orderId,
      status: 'waiting',
      deliveryStatus: o.deliveryStatus || 'waiting',
      rider: o.rider || '',
      riderName: o.riderName || '',
      createdAt: o.createdAt || o.time || new Date().toISOString(),
      items: o.items || [],
      total: o.total || 0
    };

    getDeliveries().push(d);
    return d;
  }

  window.dxExcelAssignRider = function(delId, orderId){
    var d = ensureDelivery(delId, orderId);
    var o = findOrder(orderId || (d && (d.orderId || d.oid)));

    if(!d){
      alert('Delivery/order not found.');
      return;
    }

    var current = d.rider || d.riderName || (o && (o.rider || o.riderName)) || '';
    var rider = prompt('Enter rider name:', current);

    if(rider === null) return;

    rider = rider.trim();

    if(!rider){
      alert('Enter a rider name.');
      return;
    }

    var now = Date.now();

    d.rider = rider;
    d.riderName = rider;
    d.status = 'out';
    d.deliveryStatus = 'out_for_delivery';
    d.assignedAt = d.assignedAt || now;
    d.startedAt = d.startedAt || now;
    d.outAt = d.outAt || now;

    if(o){
      o.rider = rider;
      o.riderName = rider;
      o.deliveryStatus = 'out_for_delivery';
      o.assignedAt = o.assignedAt || now;
      o.outForDeliveryAt = o.outForDeliveryAt || now;
      o.deliveryOutAt = o.deliveryOutAt || now;
    }

    try{ if(typeof sv === 'function') sv(); }catch(e){}
    try{ if(typeof toast === 'function') toast('🏍️ Rider assigned'); }catch(e){}
    try{ if(typeof renderDeliveryExcel === 'function') renderDeliveryExcel(); }catch(e){}
  };

  window.dxExcelDone = function(delId, orderId){
    var d = ensureDelivery(delId, orderId);
    var o = findOrder(orderId || (d && (d.orderId || d.oid)));

    if(!d){
      alert('Delivery/order not found.');
      return;
    }

    var now = Date.now();

    d.status = 'delivered';
    d.deliveryStatus = 'delivered';
    d.deliveredAt = d.deliveredAt || now;
    d.doneAt = d.doneAt || now;

    if(o){
      o.deliveryStatus = 'delivered';
      o.deliveredAt = o.deliveredAt || now;
      o.deliveryDeliveredAt = o.deliveryDeliveredAt || now;
      o.status = o.status === 'cancelled' ? o.status : 'completed';
    }

    try{ if(typeof sv === 'function') sv(); }catch(e){}
    try{ if(typeof toast === 'function') toast('✅ Delivery done'); }catch(e){}
    try{ if(typeof renderDeliveryExcel === 'function') renderDeliveryExcel(); }catch(e){}
  };

  document.addEventListener('click', function(e){
    var btn = e.target && e.target.closest ? e.target.closest('[data-dx-action]') : null;
    if(!btn) return;

    var action = btn.getAttribute('data-dx-action');
    if(action !== 'assign' && action !== 'done') return;

    e.preventDefault();
    e.stopPropagation();

    var delId = btn.getAttribute('data-del-id') || '';
    var orderId = btn.getAttribute('data-order-id') || '';

    if(action === 'assign'){
      window.dxExcelAssignRider(delId, orderId);
    }

    if(action === 'done'){
      window.dxExcelDone(delId, orderId);
    }
  }, true);
})();
</script>
'''

if "delivery-assign-done-fix-v11" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: delivery assign/done fix added.")
else:
    print("Already installed.")
