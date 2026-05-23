from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="delivery-assign-sheet-css-v12">
.dx-assign-backdrop{
  position:fixed;
  inset:0;
  z-index:100000;
  background:rgba(0,0,0,.42);
  display:flex;
  justify-content:center;
  align-items:flex-end;
}
.dx-assign-sheet{
  width:min(560px,100%);
  max-height:86vh;
  overflow:auto;
  background:var(--card,#fff);
  color:var(--tx,#111827);
  border-radius:24px 24px 0 0;
  padding:18px;
  box-shadow:0 -18px 50px rgba(0,0,0,.28);
}
.dx-assign-head{
  display:flex;
  justify-content:space-between;
  align-items:flex-start;
  gap:12px;
  margin-bottom:14px;
}
.dx-assign-head h3{
  margin:0;
  font-size:20px;
}
.dx-assign-close{
  border:0;
  background:#f3f4f6;
  color:#111827;
  border-radius:999px;
  width:34px;
  height:34px;
  font-weight:900;
  cursor:pointer;
}
.dx-assign-summary{
  display:grid;
  gap:8px;
  border:1px solid #e5e7eb;
  border-radius:16px;
  padding:12px;
  background:#f9fafb;
  margin-bottom:14px;
  font-size:13px;
}
.dx-assign-summary b{
  color:#111827;
}
.dx-rider-picks{
  display:flex;
  flex-wrap:wrap;
  gap:8px;
  margin:8px 0 14px;
}
.dx-rider-pick{
  border:1px solid #d1d5db;
  background:#fff;
  color:#111827;
  border-radius:999px;
  padding:9px 13px;
  font-weight:900;
  cursor:pointer;
}
.dx-rider-pick.on{
  background:#15803d;
  border-color:#15803d;
  color:white;
}
.dx-assign-label{
  display:block;
  font-size:12px;
  font-weight:900;
  color:#6b7280;
  margin:10px 0 6px;
  text-transform:uppercase;
  letter-spacing:.3px;
}
.dx-assign-input,.dx-assign-notes{
  width:100%;
  box-sizing:border-box;
  border:1px solid #d1d5db;
  border-radius:14px;
  padding:12px;
  font-size:15px;
  outline:none;
  background:#fff;
  color:#111827;
}
.dx-assign-notes{
  min-height:72px;
  resize:vertical;
}
.dx-assign-actions{
  display:flex;
  gap:10px;
  margin-top:16px;
}
.dx-assign-actions button{
  flex:1;
  border:0;
  border-radius:14px;
  padding:13px;
  font-weight:950;
  cursor:pointer;
}
.dx-assign-cancel{
  background:#f3f4f6;
  color:#111827;
}
.dx-assign-submit{
  background:#15803d;
  color:white;
}
@media(min-width:760px){
  .dx-assign-backdrop{
    align-items:center;
  }
  .dx-assign-sheet{
    border-radius:24px;
  }
}
</style>

<script id="delivery-assign-sheet-v12">
(function(){
  if(window.__deliveryAssignSheetV12) return;
  window.__deliveryAssignSheetV12 = true;

  var riderPresets = ['Juan','Mark','Carlo','Pedro','Alex'];

  function esc(v){
    return String(v == null ? '' : v)
      .replaceAll('&','&amp;')
      .replaceAll('<','&lt;')
      .replaceAll('>','&gt;')
      .replaceAll('"','&quot;')
      .replaceAll("'","&#039;");
  }

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
      id:newId,
      oid:o.id || o.orderNumber || orderId,
      orderId:o.id || o.orderNumber || orderId,
      status:'waiting',
      deliveryStatus:o.deliveryStatus || 'waiting',
      rider:o.rider || '',
      riderName:o.riderName || '',
      createdAt:o.createdAt || o.time || new Date().toISOString(),
      items:o.items || [],
      total:o.total || 0
    };

    getDeliveries().push(d);
    return d;
  }

  function orderLabel(o,d,id){
    return o.id || o.orderNumber || o.orderId || d.orderId || d.oid || d.id || id || '-';
  }

  function customer(o,d){
    return o.cust || o.customerName || o.name || d.cust || d.customerName || '-';
  }

  function customerPhone(o,d){
    return o.phone || o.customerPhone || o.customerNumber || d.phone || d.customerPhone || '-';
  }

  function recipient(o,d){
    return o.recipient || o.recipientName || d.recipient || d.recipientName || customer(o,d);
  }

  function recipientPhone(o,d){
    return o.recipientPhone || o.recipientNumber || d.recipientPhone || d.recipientNumber || customerPhone(o,d);
  }

  function address(o,d){
    return o.deliveryAddress || o.addr || o.address || d.deliveryAddress || d.addr || d.address || '-';
  }

  function city(o,d){
    return o.city || d.city || 'Other';
  }

  function deliveryDate(o,d){
    var date = o.deliveryDate || o.delivery_date || o.scheduledDate || d.deliveryDate || '';
    var time = o.deliveryTime || o.delivery_time || o.scheduledTime || d.deliveryTime || '';
    return (date || '-') + (time ? ' · ' + time : '');
  }

  function applyAssign(delId, orderId, rider, notes){
    var d = ensureDelivery(delId, orderId);

    if(!d){
      alert('Delivery/order not found.');
      return;
    }

    var o = findOrder(orderId || d.orderId || d.oid);
    var now = Date.now();

    d.rider = rider;
    d.riderName = rider;
    d.riderNotes = notes || d.riderNotes || '';
    d.status = 'out';
    d.deliveryStatus = 'out_for_delivery';
    d.assignedAt = d.assignedAt || now;
    d.startedAt = d.startedAt || now;
    d.outAt = d.outAt || now;

    if(o){
      o.rider = rider;
      o.riderName = rider;
      o.riderNotes = notes || o.riderNotes || '';
      o.deliveryStatus = 'out_for_delivery';
      o.assignedAt = o.assignedAt || now;
      o.outForDeliveryAt = o.outForDeliveryAt || now;
      o.deliveryOutAt = o.deliveryOutAt || now;
    }

    try{ if(typeof sv === 'function') sv(); }catch(e){}
    try{ if(typeof toast === 'function') toast('🏍️ Rider assigned'); }catch(e){}
    try{ if(typeof renderDeliveryExcel === 'function') renderDeliveryExcel(); }catch(e){}
  }

  function closeSheet(){
    var old = document.getElementById('dxAssignSheet');
    if(old) old.remove();
  }

  window.dxOpenAssignSheet = function(delId, orderId){
    closeSheet();

    var d = ensureDelivery(delId, orderId) || {};
    var o = findOrder(orderId || d.orderId || d.oid) || {};
    var current = d.rider || d.riderName || o.rider || o.riderName || '';

    var sheet = document.createElement('div');
    sheet.id = 'dxAssignSheet';
    sheet.className = 'dx-assign-backdrop';

    var presetHtml = riderPresets.map(function(name){
      return '<button type="button" class="dx-rider-pick '+(current === name ? 'on' : '')+'" data-rider="'+esc(name)+'">'+esc(name)+'</button>';
    }).join('');

    sheet.innerHTML =
      '<div class="dx-assign-sheet">' +
        '<div class="dx-assign-head">' +
          '<div>' +
            '<h3>🏍️ Assign Rider</h3>' +
            '<div style="font-size:13px;color:#6b7280;font-weight:800;margin-top:3px">'+esc(orderLabel(o,d,orderId || delId))+' · Waiting for Rider</div>' +
          '</div>' +
          '<button type="button" class="dx-assign-close" data-assign-close="1">×</button>' +
        '</div>' +

        '<div class="dx-assign-summary">' +
          '<div><b>Customer:</b> '+esc(customer(o,d))+' · '+esc(customerPhone(o,d))+'</div>' +
          '<div><b>Recipient:</b> '+esc(recipient(o,d))+' · '+esc(recipientPhone(o,d))+'</div>' +
          '<div><b>City:</b> '+esc(city(o,d))+'</div>' +
          '<div><b>Delivery:</b> '+esc(deliveryDate(o,d))+'</div>' +
          '<div><b>Address:</b> '+esc(address(o,d))+'</div>' +
        '</div>' +

        '<label class="dx-assign-label">Quick rider</label>' +
        '<div class="dx-rider-picks">'+presetHtml+'</div>' +

        '<label class="dx-assign-label">Rider name</label>' +
        '<input class="dx-assign-input" id="dxAssignRiderInput" placeholder="Enter rider name" value="'+esc(current)+'">' +

        '<label class="dx-assign-label">Notes for rider</label>' +
        '<textarea class="dx-assign-notes" id="dxAssignNotes" placeholder="Gate color, landmark, instructions...">'+esc(d.riderNotes || o.riderNotes || '')+'</textarea>' +

        '<div class="dx-assign-actions">' +
          '<button type="button" class="dx-assign-cancel" data-assign-close="1">Cancel</button>' +
          '<button type="button" class="dx-assign-submit" data-assign-submit="1">Assign & Start</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(sheet);

    setTimeout(function(){
      var input = document.getElementById('dxAssignRiderInput');
      if(input) input.focus();
    },100);

    sheet.addEventListener('click', function(e){
      var close = e.target.closest('[data-assign-close]');
      if(close){
        closeSheet();
        return;
      }

      var pick = e.target.closest('.dx-rider-pick');
      if(pick){
        sheet.querySelectorAll('.dx-rider-pick').forEach(function(b){b.classList.remove('on');});
        pick.classList.add('on');
        var input = document.getElementById('dxAssignRiderInput');
        if(input) input.value = pick.getAttribute('data-rider') || '';
        return;
      }

      var submit = e.target.closest('[data-assign-submit]');
      if(submit){
        var rider = (document.getElementById('dxAssignRiderInput') || {}).value || '';
        var notes = (document.getElementById('dxAssignNotes') || {}).value || '';

        rider = rider.trim();
        notes = notes.trim();

        if(!rider){
          alert('Enter a rider name.');
          return;
        }

        applyAssign(delId, orderId, rider, notes);
        closeSheet();
      }
    });
  };

  // Override the working assign function only. Done remains from v11.
  window.dxExcelAssignRider = function(delId, orderId){
    window.dxOpenAssignSheet(delId, orderId);
  };
})();
</script>
'''

if "delivery-assign-sheet-v12" in html:
    print("Assign sheet already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
      insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Assign rider sheet added.")
