from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

removed = 0

# Remove filter experiment layers that run after render
ids = [
    "delivery-simple-filters-v1",
    "delivery-simple-filters-v2",
    "delivery-fast-filters-v3",
    "delivery-fast-filters-v4",
    "delivery-filter-compact-dropdowns-v1",
    "delivery-filter-chips-v1",
    "delivery-filter-skip-collapsed-history-v4",
    "delivery-filter-v3-less-lag-open-history-v1",
]

for sid in ids:
    html, c1 = re.subn(r'\s*<style id="'+re.escape(sid)+r'">.*?</style>\s*', '\n', html, flags=re.S)
    html, c2 = re.subn(r'\s*<script id="'+re.escape(sid)+r'">.*?</script>\s*', '\n', html, flags=re.S)
    removed += c1 + c2

patch = r'''
<style id="delivery-integrated-filter-renderer-v1">
#deliveryExcelRoot .dx-top{
  display:block !important;
}

.dx-integrated-filter{
  padding:10px 12px;
  margin:0 0 12px;
  background:var(--w,#fff);
  border:1px solid var(--b,#e5e7eb);
  border-radius:18px;
}

.dx-integrated-row{
  display:flex;
  gap:7px;
  overflow-x:auto;
  -webkit-overflow-scrolling:touch;
  scrollbar-width:none;
  padding-bottom:2px;
}

.dx-integrated-row::-webkit-scrollbar{
  display:none;
}

.dx-ifilter{
  flex:0 0 auto;
  height:34px;
  min-width:86px;
  max-width:155px;
  padding:7px 10px;
  border-radius:999px;
  border:1px solid var(--b2,#d1d5db);
  background:var(--w,#fff);
  color:var(--t,#111827);
  font-size:12px;
  font-weight:800;
  font-family:inherit;
  cursor:pointer;
  white-space:nowrap;
}

.dx-ifilter.on,
.dx-ifilter.active{
  border-color:var(--green,#15803d);
  background:var(--gl,#e9f7ef);
  color:var(--gd,#166534);
}

select.dx-ifilter{
  min-width:118px;
}

input[type="date"].dx-ifilter{
  min-width:142px;
}

.dx-integrated-summary{
  margin-top:8px;
  font-size:11px;
  color:var(--t3,#6b7280);
  font-weight:800;
}

@media(max-width:768px){
  .dx-integrated-filter{
    margin-left:-2px;
    margin-right:-2px;
  }
}
</style>

<script id="delivery-integrated-filter-renderer-v1">
(function(){
  if(window.__deliveryIntegratedFilterRendererV1) return;
  window.__deliveryIntegratedFilterRendererV1 = true;

  window.dxIntegratedState = window.dxIntegratedState || {
    status:'all',
    priority:'all',
    date:'all',
    rider:'all'
  };

  function esc(v){
    return String(v == null ? '' : v)
      .replaceAll('&','&amp;')
      .replaceAll('<','&lt;')
      .replaceAll('>','&gt;')
      .replaceAll('"','&quot;')
      .replaceAll("'","&#039;");
  }

  function saveScroll(){
    return Array.from(document.querySelectorAll('#deliveryExcelRoot .dx-scroll')).map(function(el){
      return {el:el,left:el.scrollLeft || 0,top:el.scrollTop || 0};
    });
  }

  function restoreScroll(pos){
    requestAnimationFrame(function(){
      pos.forEach(function(p){
        if(p.el){
          p.el.scrollLeft = p.left || 0;
          p.el.scrollTop = p.top || 0;
        }
      });
    });
  }

  function orders(){
    return window.S && Array.isArray(S.orders) ? S.orders : [];
  }

  function deliveryList(){
    return window.S && Array.isArray(S.deliveries) ? S.deliveries : [];
  }

  function orderOf(d){
    var id = d.orderId || d.oid || d.order || d.id || '';
    return orders().find(function(o){
      return String(o.id || o.orderNumber || o.orderId) === String(id) ||
             String('DEL-' + String(o.id || o.orderNumber || o.orderId).replace(/^ORD-/,'').replace(/^DEL-/,'')) === String(d.id || '');
    }) || {};
  }

  function isPickupFlow(o){
    var type = String(o.orderType || o.fulfillmentType || o.type || '').toLowerCase();
    return (
      type === 'pickup' ||
      o.pickupStatus === 'waiting' ||
      o.pickupStatus === 'picked_up' ||
      o.kitForPickup === true ||
      o.kitPickup === true
    );
  }

  function isDeliveryOrder(o){
    if(!o) return false;
    if(isPickupFlow(o)) return false;

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

    if(ds === 'out_for_delivery' || ds === 'out' || ds === 'delivered') return true;
    if(o.rider || o.riderName || d.rider || d.riderName) return true;
    if(o.deliveredAt || d.deliveredAt || o.outForDeliveryAt || o.deliveryOutAt) return true;

    return (
      ks === 'sent_to_delivery' ||
      ks === 'out' ||
      o.sentToDeliveryAt ||
      o.deliverySentAt ||
      d.sentToDeliveryAt ||
      d.deliverySentAt
    );
  }

  function deliveryFromOrder(o){
    var oid = o.id || o.orderNumber || o.orderId;
    return {
      id: 'DEL-' + String(oid || '').replace(/^ORD-/,'').replace(/^DEL-/,''),
      orderId: oid,
      oid: oid,
      order: oid,
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
    var result = [];
    var seen = {};

    deliveryList().forEach(function(d){
      var o = orderOf(d);
      if(isDeliveryOrder(o) && isSentToDelivery(o,d)){
        result.push(d);
        var oid = d.orderId || d.oid || d.order || d.id;
        if(oid) seen[String(oid)] = true;
        if(d.id) seen[String(d.id)] = true;
      }
    });

    orders().forEach(function(o){
      var oid = o.id || o.orderNumber || o.orderId;
      if(!oid) return;

      var delId = 'DEL-' + String(oid).replace(/^ORD-/,'').replace(/^DEL-/,'');
      if(seen[String(oid)] || seen[delId]) return;

      if(isDeliveryOrder(o) && isSentToDelivery(o,{})){
        result.push(deliveryFromOrder(o));
      }
    });

    return result;
  }

  function statusOf(d,o){
    var s = String((o && o.deliveryStatus) || d.deliveryStatus || d.status || '').toLowerCase();

    if(s === 'delivered' || o.deliveredAt || d.deliveredAt || o.deliveryDeliveredAt) return 'delivered';
    if(s === 'out_for_delivery' || s === 'out' || o.outForDeliveryAt || o.deliveryOutAt || d.outAt || d.startedAt) return 'out';

    return 'waiting';
  }

  function statusLabel(s){
    if(s === 'out') return 'Out for Delivery';
    if(s === 'delivered') return 'Delivered';
    return 'Waiting Rider';
  }

  function priorityOf(o,d){
    var p = String((o && o.priority) || d.priority || 'normal').toLowerCase();
    if(p !== 'rush' && p !== 'low') p = 'normal';
    return p;
  }

  function created(o,d){
    var t = (o && (o.createdAt || o.time)) || d.createdAt || d.time || '';
    if(!t) return '-';
    try{
      return new Date(t).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
    }catch(e){
      return String(t);
    }
  }

  function val(){
    for(var i=0;i<arguments.length;i++){
      if(arguments[i] !== undefined && arguments[i] !== null && String(arguments[i]).trim() !== ''){
        return arguments[i];
      }
    }
    return '-';
  }

  function customer(o,d){ return val(o.cust, o.customerName, o.name, d.cust, d.customerName); }
  function customerPhone(o,d){ return val(o.phone, o.customerPhone, o.customerNumber, d.phone, d.customerPhone); }
  function recipient(o,d){ return val(o.recipient, o.recipientName, d.recipient, d.recipientName, customer(o,d)); }
  function recipientPhone(o,d){ return val(o.recipientPhone, o.recipientNumber, d.recipientPhone, d.recipientNumber, customerPhone(o,d)); }
  function address(o,d){ return val(o.deliveryAddress, o.addr, o.address, d.deliveryAddress, d.addr, d.address); }

  function cityOf(o,d){
    var c = val(o.city, d.city, '');
    if(c && c !== '-') return c;

    var a = String(address(o,d)).toLowerCase();
    var cities = ['caloocan','manila','quezon city','valenzuela','malabon','navotas','makati','pasig','taguig','pasay'];
    for(var i=0;i<cities.length;i++){
      if(a.indexOf(cities[i]) !== -1) return cities[i].replace(/\b\w/g,function(x){return x.toUpperCase();});
    }
    return 'Other';
  }

  function deliveryDateRaw(o,d){
    return val(o.deliveryDate, o.delivery_date, o.scheduledDate, d.deliveryDate, d.delivery_date, '');
  }

  function deliveryDate(o,d){
    var date = deliveryDateRaw(o,d);
    var time = val(o.deliveryTime, o.delivery_time, o.scheduledTime, d.deliveryTime, d.delivery_time, '');
    if(date === '-' && time === '-') return '-';
    if(time === '-') return esc(date);
    if(date === '-') return esc(time);
    return esc(date) + '<br><span class="dx-muted">' + esc(time) + '</span>';
  }

  function itemText(o,d){
    var items = (o.items || d.items || []);
    if(!items || !items.length) return '-';
    var first = items[0] || {};
    var more = items.length - 1;
    var name = first.name || first.item || first.title || 'Item';
    var qty = first.qty || first.quantity || 1;
    return esc(name + ' x' + qty) + (more > 0 ? '<br><span class="dx-muted">+'+more+' more</span>' : '');
  }

  function totalOf(o,d){
    return Number(o.total || d.total || 0);
  }

  function fmt(ms){
    ms = Math.max(0, ms || 0);
    var m = Math.floor(ms / 60000);
    var s = Math.floor((ms % 60000) / 1000);
    var h = Math.floor(m / 60);
    m = m % 60;
    if(h) return h + 'h ' + m + 'm';
    return m + 'm ' + s + 's';
  }

  window.dxFormatDuration = window.dxFormatDuration || fmt;

  function riderTimer(d,o,s){
    var rider = o.rider || o.riderName || d.rider || d.riderName || '';

    if(s === 'waiting'){
      return '<span class="dx-muted">Not assigned</span>';
    }

    var start = o.outForDeliveryAt || o.deliveryOutAt || o.assignedAt || d.startedAt || d.outAt || d.assignedAt || Date.now();

    if(s === 'delivered'){
      var deliveredAt = o.deliveredAt || o.deliveryDeliveredAt || d.deliveredAt || d.doneAt || Date.now();
      return esc(rider || '-') + '<br><span class="dx-muted">Delivered in ' + esc(fmt(deliveredAt - start)) + '</span>';
    }

    return esc(rider || '-') + '<br><span class="dx-timer dx-live-timer" data-start="' + esc(start) + '">Running</span>';
  }

  function action(d,o,s){
    var delId = esc(d.id || '');
    var orderId = esc(o.id || o.orderNumber || d.orderId || d.oid || d.order || d.id || '');

    if(s === 'out'){
      return '<button type="button" class="dx-action" data-dx-action="done" data-del-id="'+delId+'" data-order-id="'+orderId+'">Done</button>';
    }

    if(s === 'delivered'){
      return '<button type="button" class="dx-action view" data-dx-action="view" data-del-id="'+delId+'" data-order-id="'+orderId+'">View</button>';
    }

    return '<button type="button" class="dx-action assign" data-dx-action="assign-sheet" data-del-id="'+delId+'" data-order-id="'+orderId+'">Assign</button>';
  }

  function matches(d,o){
    var st = window.dxIntegratedState;
    var s = statusOf(d,o);
    var p = priorityOf(o,d);
    var rowDate = String(deliveryDateRaw(o,d) || '').slice(0,10);
    var rider = String(o.rider || o.riderName || d.rider || d.riderName || '').toLowerCase();

    if(st.status !== 'all' && s !== st.status) return false;
    if(st.priority !== 'all' && p !== st.priority) return false;
    if(st.date !== 'all' && rowDate !== st.date) return false;

    if(st.rider === 'assigned' && !rider) return false;
    if(st.rider === 'unassigned' && rider) return false;

    return true;
  }

  function filterBar(){
    var st = window.dxIntegratedState;

    function statusBtn(v,label){
      return '<button type="button" class="dx-ifilter '+(st.status===v?'on active':'')+'" onclick="dxIntegratedSetStatus(\''+v+'\')">'+label+'</button>';
    }

    return '' +
      '<div class="dx-integrated-filter">' +
        '<div class="dx-integrated-row">' +
          statusBtn('all','All') +
          statusBtn('waiting','Waiting') +
          statusBtn('out','Out') +
          statusBtn('delivered','Delivered') +

          '<select class="dx-ifilter '+(st.priority !== 'all' ? 'active' : '')+'" onchange="dxIntegratedSetFilter(\'priority\',this.value)">' +
            '<option value="all" '+(st.priority==='all'?'selected':'')+'>Priority</option>' +
            '<option value="rush" '+(st.priority==='rush'?'selected':'')+'>Rush</option>' +
            '<option value="normal" '+(st.priority==='normal'?'selected':'')+'>Normal</option>' +
            '<option value="low" '+(st.priority==='low'?'selected':'')+'>Low</option>' +
          '</select>' +

          '<input type="date" class="dx-ifilter '+(st.date !== 'all' ? 'active' : '')+'" value="'+(st.date !== 'all' ? esc(st.date) : '')+'" onchange="dxIntegratedSetFilter(\'date\',this.value || \'all\')">' +

          '<select class="dx-ifilter '+(st.rider !== 'all' ? 'active' : '')+'" onchange="dxIntegratedSetFilter(\'rider\',this.value)">' +
            '<option value="all" '+(st.rider==='all'?'selected':'')+'>Rider</option>' +
            '<option value="assigned" '+(st.rider==='assigned'?'selected':'')+'>Assigned</option>' +
            '<option value="unassigned" '+(st.rider==='unassigned'?'selected':'')+'>Not assigned</option>' +
          '</select>' +

          '<button type="button" class="dx-ifilter" onclick="dxIntegratedResetFilters()">Reset</button>' +
        '</div>' +
      '</div>';
  }

  function row(d){
    var o = orderOf(d);
    var s = statusOf(d,o);
    var p = priorityOf(o,d);
    var realOrderId = o.id || o.orderNumber || o.orderId || d.orderId || d.oid || d.order || d.id || '-';
    var id = String(realOrderId).startsWith('DEL-') ? 'ORD-' + String(realOrderId).replace(/^DEL-/,'') : realOrderId;

    var a = address(o,d);
    var shortAddr = String(a).length > 26 ? String(a).slice(0,26) + '...' : String(a);

    var rowCity = String(cityOf(o,d) || 'Other').toLowerCase();
    var rowRider = String(o.rider || o.riderName || d.rider || d.riderName || '').toLowerCase();
    var rowDate = String(deliveryDateRaw(o,d) || '').slice(0,10);

    return '<tr data-dx-status="'+esc(s)+'" data-dx-priority="'+esc(p)+'" data-dx-city="'+esc(rowCity)+'" data-dx-rider="'+esc(rowRider)+'" data-dx-date="'+esc(rowDate)+'">' +
      '<td><div class="dx-order">'+esc(id)+'</div><span class="dx-prio '+esc(p)+'">'+esc(p.charAt(0).toUpperCase()+p.slice(1))+'</span></td>' +
      '<td><span class="dx-status '+(s === 'out' ? 'out' : s === 'delivered' ? 'delivered' : 'wait')+'">'+esc(statusLabel(s))+'</span></td>' +
      '<td>'+esc(created(o,d))+'</td>' +
      '<td><div class="dx-name">'+esc(customer(o,d))+'</div><div class="dx-phone">'+esc(customerPhone(o,d))+'</div></td>' +
      '<td><div class="dx-name">'+esc(recipient(o,d))+'</div><div class="dx-phone">'+esc(recipientPhone(o,d))+'</div></td>' +
      '<td style="min-width:180px">'+esc(shortAddr)+'<br><span class="dx-muted">'+esc(cityOf(o,d))+'</span><br><button type="button" class="dx-link" data-dx-action="address" data-del-id="'+esc(d.id || '')+'" data-order-id="'+esc(o.id || o.orderNumber || d.orderId || d.oid || d.order || d.id || '')+'">[View]</button></td>' +
      '<td style="min-width:110px">'+deliveryDate(o,d)+'</td>' +
      '<td style="min-width:110px">'+itemText(o,d)+'<br><span class="dx-muted">₱'+esc(totalOf(o,d).toFixed(2))+'</span><br><button type="button" class="dx-link" data-dx-action="items" data-del-id="'+esc(d.id || '')+'" data-order-id="'+esc(o.id || o.orderNumber || d.orderId || d.oid || d.order || d.id || '')+'">[View]</button></td>' +
      '<td style="min-width:115px">'+riderTimer(d,o,s)+'</td>' +
      '<td>'+action(d,o,s)+'</td>' +
    '</tr>';
  }

  function table(list){
    if(!list.length){
      return '<div class="dx-empty">No delivery orders found.</div>';
    }

    return '<div class="dx-scroll"><table class="dx-table">' +
      '<thead><tr>' +
        '<th>Order # / Prio</th>' +
        '<th>Status</th>' +
        '<th>Created</th>' +
        '<th>Customer</th>' +
        '<th>Recipient</th>' +
        '<th>Address</th>' +
        '<th>Delivery Date</th>' +
        '<th>Items / Total</th>' +
        '<th>Rider / Timer</th>' +
        '<th>Action</th>' +
      '</tr></thead>' +
      '<tbody>' + list.map(row).join('') + '</tbody>' +
    '</table></div>';
  }

  function section(title,list){
    return '<div class="dx-section">' +
      '<div class="dx-section-head"><span>'+esc(title)+' ('+list.length+')</span></div>' +
      table(list) +
    '</div>';
  }

  window.renderDeliveryExcel = function(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root){
      var view = document.getElementById('view-delivery');
      if(!view) return;
      root = document.createElement('div');
      root.id = 'deliveryExcelRoot';
      view.appendChild(root);
    }

    var pos = saveScroll();

    var all = deliveries();
    var filtered = all.filter(function(d){ return matches(d, orderOf(d)); });

    var out = filtered.filter(function(d){ return statusOf(d, orderOf(d)) === 'out'; });
    var waiting = filtered.filter(function(d){ return statusOf(d, orderOf(d)) === 'waiting'; });
    var delivered = filtered.filter(function(d){ return statusOf(d, orderOf(d)) === 'delivered'; });

    root.innerHTML =
      filterBar() +
      section('Out for Delivery', out) +
      section('Waiting for Rider', waiting) +
      section('Delivered History', delivered) +
      '<div class="dx-muted" style="padding:8px 2px 18px;font-weight:800">Showing '+filtered.length+' of '+all.length+' delivery orders</div>';

    try{
      if(typeof window.dxApplyDeliveredHistoryState === 'function'){
        window.dxApplyDeliveredHistoryState();
      }
    }catch(e){}

    restoreScroll(pos);

    try{
      if(typeof updateDeliveryLiveTimers === 'function') updateDeliveryLiveTimers();
    }catch(e){}
  };

  window.dxIntegratedSetStatus = function(v){
    window.dxIntegratedState.status = v || 'all';
    window.renderDeliveryExcel();
  };

  window.dxIntegratedSetFilter = function(k,v){
    window.dxIntegratedState[k] = v || 'all';
    window.renderDeliveryExcel();
  };

  window.dxIntegratedResetFilters = function(){
    window.dxIntegratedState = {status:'all',priority:'all',date:'all',rider:'all'};
    window.renderDeliveryExcel();
  };

  try{ renderDeliveryExcel = window.renderDeliveryExcel; }catch(e){}

  setTimeout(function(){
    try{ window.renderDeliveryExcel(); }catch(e){}
  },300);
})();
</script>
'''

if "delivery-integrated-filter-renderer-v1" in html:
    print("Integrated filter renderer already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]

p.write_text(html, encoding="utf-8")
print("DONE: installed integrated Delivery renderer.")
print("Removed old filter blocks:", removed)
