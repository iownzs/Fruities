from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="delivery-excel-ui-v1">
/* ===== Delivery Excel UI v1 ===== */
.dx-wrap{
  margin-top:12px;
}
.dx-top{
  display:grid;
  gap:12px;
  margin-bottom:14px;
}
.dx-search-row{
  display:flex;
  gap:10px;
  align-items:center;
}
.dx-search{
  flex:1;
  border:1px solid var(--bd,#e5e7eb);
  border-radius:14px;
  padding:12px 14px;
  font-size:14px;
  outline:none;
  background:var(--card,#fff);
  color:var(--tx,#111827);
}
.dx-chip-row,.dx-filter-row{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
}
.dx-chip{
  border:1px solid var(--bd,#e5e7eb);
  border-radius:999px;
  background:var(--card,#fff);
  color:var(--tx,#111827);
  padding:9px 14px;
  font-weight:800;
  font-size:13px;
  cursor:pointer;
}
.dx-chip.on{
  background:#15803d;
  color:white;
  border-color:#15803d;
}
.dx-select{
  border:1px solid var(--bd,#e5e7eb);
  border-radius:13px;
  background:var(--card,#fff);
  color:var(--tx,#111827);
  padding:10px 12px;
  font-weight:750;
  min-width:140px;
}
.dx-section{
  border:1px solid var(--bd,#e5e7eb);
  border-radius:16px;
  overflow:hidden;
  margin:14px 0;
  background:var(--card,#fff);
}
.dx-section-head{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:10px;
  padding:12px 14px;
  border-bottom:1px solid var(--bd,#e5e7eb);
  font-weight:900;
}
.dx-section-head.out{color:#15803d}
.dx-section-head.wait{color:#ea580c}
.dx-section-head.done{color:#2563eb}
.dx-scroll{
  overflow:auto;
  -webkit-overflow-scrolling:touch;
}
.dx-table{
  width:max-content;
  min-width:100%;
  border-collapse:separate;
  border-spacing:0;
  font-size:13px;
}
.dx-table th{
  position:sticky;
  top:0;
  z-index:2;
  background:#f8fafc;
  color:#111827;
  font-size:12px;
  text-align:left;
  padding:10px 12px;
  border-bottom:1px solid #e5e7eb;
  border-right:1px solid #e5e7eb;
  white-space:nowrap;
}
.dx-table td{
  vertical-align:middle;
  padding:12px;
  border-bottom:1px solid #e5e7eb;
  border-right:1px solid #e5e7eb;
  color:var(--tx,#111827);
  background:var(--card,#fff);
  line-height:1.45;
}
.dx-table tr:last-child td{border-bottom:0}
.dx-order{
  font-weight:950;
  font-size:14px;
  white-space:nowrap;
}
.dx-prio{
  display:inline-flex;
  margin-top:6px;
  padding:4px 8px;
  border-radius:9px;
  font-size:12px;
  font-weight:900;
}
.dx-prio.rush{background:#fee2e2;color:#dc2626}
.dx-prio.normal{background:#dcfce7;color:#15803d}
.dx-prio.low{background:#f3f4f6;color:#4b5563}
.dx-status{
  display:inline-flex;
  padding:6px 9px;
  border-radius:9px;
  font-weight:900;
  font-size:12px;
  white-space:nowrap;
}
.dx-status.out{background:#dcfce7;color:#15803d}
.dx-status.wait{background:#ffedd5;color:#ea580c}
.dx-status.delivered{background:#dbeafe;color:#2563eb}
.dx-name{
  font-weight:850;
  white-space:nowrap;
}
.dx-phone{
  color:var(--t2,#4b5563);
  white-space:nowrap;
}
.dx-link{
  border:0;
  background:transparent;
  color:#15803d;
  font-weight:900;
  cursor:pointer;
  padding:0;
  margin-top:3px;
  display:inline-block;
}
.dx-action{
  border:1px solid #15803d;
  background:#15803d;
  color:#fff;
  border-radius:10px;
  padding:9px 13px;
  font-weight:900;
  cursor:pointer;
  min-width:74px;
}
.dx-action.assign{
  border-color:#ea580c;
  background:#ea580c;
}
.dx-action.view{
  border-color:#d1d5db;
  background:#f9fafb;
  color:#111827;
}
.dx-muted{color:#6b7280}
.dx-timer{font-weight:900;color:#15803d}
.dx-empty{
  padding:18px;
  color:#6b7280;
  font-weight:800;
}
.dx-modal-backdrop{
  position:fixed;
  inset:0;
  background:rgba(0,0,0,.38);
  z-index:99999;
  display:flex;
  align-items:flex-end;
  justify-content:center;
}
.dx-modal{
  width:min(560px,100%);
  max-height:80vh;
  overflow:auto;
  background:#fff;
  color:#111827;
  border-radius:22px 22px 0 0;
  padding:18px;
  box-shadow:0 -12px 40px rgba(0,0,0,.22);
}
.dx-modal h3{margin:0 0 12px;font-size:18px}
.dx-modal pre{
  white-space:pre-wrap;
  font-family:inherit;
  line-height:1.45;
  margin:0;
}
.dx-modal button{
  margin-top:16px;
  width:100%;
  border:0;
  border-radius:12px;
  padding:12px;
  background:#15803d;
  color:#fff;
  font-weight:900;
}
@media(max-width:700px){
  .dx-wrap{
    margin-left:-6px;
    margin-right:-6px;
  }
  .dx-select{
    min-width:calc(50% - 5px);
    flex:1;
  }
  .dx-table{
    font-size:12px;
  }
  .dx-table th,.dx-table td{
    padding:9px 10px;
  }
  .dx-section{
    border-radius:14px;
  }
}
</style>

<script id="delivery-excel-renderer-v1">
(function(){
  if(window.__deliveryExcelV1Installed) return;
  window.__deliveryExcelV1Installed = true;

  var dxState = {
    status:'all',
    priority:'all',
    city:'all',
    date:'all',
    rider:'all',
    q:''
  };

  function dxEsc(v){
    return String(v ?? '')
      .replaceAll('&','&amp;')
      .replaceAll('<','&lt;')
      .replaceAll('>','&gt;')
      .replaceAll('"','&quot;')
      .replaceAll("'","&#039;");
  }

  function dxMoney(v){
    var n = Number(v || 0);
    return '₱' + n.toLocaleString('en-PH',{maximumFractionDigits:2});
  }

  function dxOrderById(id){
    try{
      if(typeof orderById === 'function') return orderById(id);
    }catch(e){}
    var arr = (window.S && Array.isArray(S.orders)) ? S.orders : [];
    return arr.find(function(o){return String(o.id || o.orderNumber || o.orderId) === String(id);}) || null;
  }

  function dxGetOrder(d){
    return dxOrderById(d.oid || d.orderId || d.order || d.id) || {};
  }

  function dxNormStatus(d,o){
    var s = String((o && o.deliveryStatus) || d.deliveryStatus || d.status || '').toLowerCase();
    if(s === 'delivered' || o.deliveredAt || d.deliveredAt) return 'delivered';
    if(s === 'out_for_delivery' || s === 'out' || s === 'out for delivery') return 'out';
    if(s === 'assigned') return 'out';
    if(d.rider || d.riderName || o.rider || o.riderName){
      if(s !== 'waiting') return 'out';
    }
    return 'waiting';
  }

  function dxStatusLabel(s){
    if(s === 'out') return 'Out for Delivery';
    if(s === 'delivered') return 'Delivered';
    return 'Waiting for Rider';
  }

  function dxPriority(o,d){
    return String(o.priority || d.priority || 'normal').toLowerCase();
  }

  function dxPriorityLabel(p){
    if(p === 'rush') return 'Rush';
    if(p === 'low') return 'Low';
    return 'Normal';
  }

  function dxCreated(o,d){
    var raw = o.createdAt || o.time || d.createdAt || d.startedAt || d.time;
    if(!raw) return '-';
    try{
      var dt = new Date(raw);
      if(isNaN(dt.getTime())) return String(raw);
      return dt.toLocaleTimeString('en-PH',{hour:'numeric',minute:'2-digit'});
    }catch(e){return String(raw)}
  }

  function dxDeliveryDate(o,d){
    var date = o.deliveryDate || o.delivery_date || o.scheduledDate || d.deliveryDate || d.delivery_date || '';
    var time = o.deliveryTime || o.delivery_time || o.scheduledTime || d.deliveryTime || d.delivery_time || '';
    if(date && time) return dxFmtDate(date) + '<br>' + dxEsc(dxFmtTime(time));
    return dxEsc(date || time || '-');
  }

  function dxFmtDate(v){
    try{
      if(!v) return '';
      var dt = new Date(String(v).includes('T') ? v : String(v) + 'T00:00:00');
      if(isNaN(dt.getTime())) return dxEsc(v);
      return dxEsc(dt.toLocaleDateString('en-PH',{month:'short',day:'numeric'}));
    }catch(e){return dxEsc(v)}
  }

  function dxFmtTime(v){
    try{
      if(!v) return '';
      if(String(v).includes(':')){
        var parts = String(v).split(':');
        var dt = new Date();
        dt.setHours(Number(parts[0]), Number(parts[1] || 0), 0, 0);
        return dt.toLocaleTimeString('en-PH',{hour:'numeric',minute:'2-digit'});
      }
      return v;
    }catch(e){return v}
  }

  function dxCustomerName(o,d){
    return o.cust || o.customerName || o.name || d.cust || d.customerName || '-';
  }

  function dxCustomerPhone(o,d){
    return o.phone || o.customerPhone || o.customerNumber || d.phone || d.customerPhone || d.customerNumber || '-';
  }

  function dxRecipientName(o,d){
    return o.recipient || o.recipientName || o.receiverName || d.recipient || d.recipientName || dxCustomerName(o,d);
  }

  function dxRecipientPhone(o,d){
    return o.recipientPhone || o.recipientNumber || o.receiverPhone || d.recipientPhone || d.recipientNumber || dxCustomerPhone(o,d);
  }

  function dxAddress(o,d){
    return o.deliveryAddress || o.addr || o.address || d.deliveryAddress || d.addr || d.address || '-';
  }

  function dxCity(o,d){
    var c = o.city || d.city || '';
    if(c) return c;
    var a = String(dxAddress(o,d)).toLowerCase();
    var cities = ['caloocan','manila','quezon city','valenzuela','malabon','navotas','makati','pasig','taguig','pasay','marikina','mandaluyong','san juan','paranaque','las pinas','muntinlupa'];
    var found = cities.find(function(x){return a.includes(x);});
    return found ? found.replace(/\b\w/g,function(m){return m.toUpperCase();}) : 'Other';
  }

  function dxAddressPreview(o,d){
    var a = String(dxAddress(o,d));
    var city = dxCity(o,d);
    var short = a.length > 28 ? a.slice(0,28) + '...' : a;
    return dxEsc(short) + '<br><span class="dx-muted">' + dxEsc(city) + '</span><br><button class="dx-link" onclick="dxShowAddress(\'' + dxEsc(d.id) + '\')">[View]</button>';
  }

  function dxItems(o,d){
    return Array.isArray(o.items) ? o.items : (Array.isArray(d.items) ? d.items : []);
  }

  function dxItemsPreview(o,d){
    var items = dxItems(o,d);
    var total = o.total || d.total || 0;
    var count = items.length || Number(o.itemCount || d.itemCount || 0);
    var label = count ? (count + ' item' + (count === 1 ? '' : 's')) : 'Items';
    return dxEsc(label) + '<br><strong>' + dxMoney(total) + '</strong><br><button class="dx-link" onclick="dxShowItems(\'' + dxEsc(d.id) + '\')">[View]</button>';
  }

  function dxRiderTimer(d,o,status){
    var rider = d.rider || d.riderName || o.rider || o.riderName || '';
    if(status === 'waiting') return '<span class="dx-muted">Not assigned<br>-</span>';

    var start = o.outForDeliveryAt || o.deliveryOutAt || d.outAt || d.startedAt || d.assignedAt || o.assignedAt;
    var end = o.deliveredAt || d.deliveredAt;

    if(status === 'delivered'){
      var mins = start && end ? Math.max(1, Math.round((Number(end)-Number(start))/60000)) : '';
      return dxEsc(rider || '-') + '<br><span class="dx-timer">Delivered' + (mins ? ' in ' + mins + 'm' : '') + '</span>';
    }

    var txt = '';
    if(start){
      var ms = Date.now() - Number(start);
      var m = Math.floor(ms/60000);
      var s = Math.floor((ms%60000)/1000);
      txt = m + 'm ' + String(s).padStart(2,'0') + 's';
    }else{
      txt = 'Running';
    }

    return dxEsc(rider || '-') + '<br><span class="dx-timer">' + dxEsc(txt) + '</span>';
  }

  function dxAction(d,o,status){
    var id = dxEsc(d.id);
    if(status === 'out') return '<button class="dx-action" onclick="dxMarkDelivered(\''+id+'\')">Done</button>';
    if(status === 'delivered') return '<button class="dx-action view" onclick="dxShowItems(\''+id+'\')">View</button>';
    return '<button class="dx-action assign" onclick="quickAssignRider(\''+id+'\')">Assign</button>';
  }

  function dxDeliveryList(){
    var arr = (window.S && Array.isArray(S.deliveries)) ? S.deliveries.slice() : [];
    return arr;
  }

  function dxMatch(d){
    var o = dxGetOrder(d);
    var status = dxNormStatus(d,o);
    var prio = dxPriority(o,d);
    var city = dxCity(o,d).toLowerCase();
    var rider = String(d.rider || d.riderName || o.rider || o.riderName || '').toLowerCase();
    var q = dxState.q.toLowerCase();

    if(dxState.status !== 'all' && dxState.status !== status) return false;
    if(dxState.priority !== 'all' && dxState.priority !== prio) return false;
    if(dxState.city !== 'all' && city !== dxState.city) return false;
    if(dxState.rider !== 'all'){
      if(dxState.rider === 'assigned' && !rider) return false;
      if(dxState.rider === 'unassigned' && rider) return false;
      if(dxState.rider !== 'assigned' && dxState.rider !== 'unassigned' && rider !== dxState.rider) return false;
    }
    if(dxState.date !== 'all'){
      var date = String(o.deliveryDate || o.delivery_date || o.scheduledDate || d.deliveryDate || '').slice(0,10);
      var today = new Date();
      var iso = today.toISOString().slice(0,10);
      var tom = new Date(today.getTime()+86400000).toISOString().slice(0,10);
      if(dxState.date === 'today' && date !== iso) return false;
      if(dxState.date === 'tomorrow' && date !== tom) return false;
    }

    if(q){
      var blob = [
        d.id,o.id,o.orderNumber,dxCustomerName(o,d),dxCustomerPhone(o,d),
        dxRecipientName(o,d),dxRecipientPhone(o,d),dxAddress(o,d),dxCity(o,d),
        dxPriority(o,d),dxStatusLabel(status)
      ].join(' ').toLowerCase();
      if(!blob.includes(q)) return false;
    }

    return true;
  }

  function dxRow(d){
    var o = dxGetOrder(d);
    var status = dxNormStatus(d,o);
    var prio = dxPriority(o,d);
    return '<tr>' +
      '<td><div class="dx-order">'+dxEsc(d.id || o.id || o.orderNumber || '-')+'</div><span class="dx-prio '+dxEsc(prio)+'">'+dxEsc(dxPriorityLabel(prio))+'</span></td>' +
      '<td><span class="dx-status '+(status==='out'?'out':status==='delivered'?'delivered':'wait')+'">'+dxEsc(dxStatusLabel(status))+'</span></td>' +
      '<td>'+dxEsc(dxCreated(o,d))+'</td>' +
      '<td><div class="dx-name">'+dxEsc(dxCustomerName(o,d))+'</div><div class="dx-phone">'+dxEsc(dxCustomerPhone(o,d))+'</div></td>' +
      '<td><div class="dx-name">'+dxEsc(dxRecipientName(o,d))+'</div><div class="dx-phone">'+dxEsc(dxRecipientPhone(o,d))+'</div></td>' +
      '<td style="min-width:190px">'+dxAddressPreview(o,d)+'</td>' +
      '<td style="min-width:110px">'+dxDeliveryDate(o,d)+'</td>' +
      '<td style="min-width:110px">'+dxItemsPreview(o,d)+'</td>' +
      '<td style="min-width:125px">'+dxRiderTimer(d,o,status)+'</td>' +
      '<td>'+dxAction(d,o,status)+'</td>' +
    '</tr>';
  }

  function dxTable(items){
    if(!items.length) return '<div class="dx-empty">No orders here.</div>';
    return '<div class="dx-scroll"><table class="dx-table">' +
      '<thead><tr>' +
      '<th>Order # / Prio</th><th>Status</th><th>Created</th><th>Customer</th><th>Recipient</th><th>Address</th><th>Delivery Date</th><th>Items / Total</th><th>Rider / Timer</th><th>Action</th>' +
      '</tr></thead><tbody>' + items.map(dxRow).join('') + '</tbody></table></div>';
  }

  function dxSection(title, cls, items){
    return '<section class="dx-section">' +
      '<div class="dx-section-head '+cls+'"><span>'+dxEsc(title)+' ('+items.length+')</span><span>⌃</span></div>' +
      dxTable(items) +
    '</section>';
  }

  function dxUniqueCities(list){
    var set = {};
    list.forEach(function(d){ var o = dxGetOrder(d); set[dxCity(o,d).toLowerCase()] = dxCity(o,d); });
    return Object.entries(set).sort(function(a,b){return a[1].localeCompare(b[1]);});
  }

  function dxUniqueRiders(list){
    var set = {};
    list.forEach(function(d){
      var o = dxGetOrder(d);
      var r = d.rider || d.riderName || o.rider || o.riderName || '';
      if(r) set[String(r).toLowerCase()] = r;
    });
    return Object.entries(set).sort(function(a,b){return a[1].localeCompare(b[1]);});
  }

  function dxFindDeliveryArea(){
    var existing = document.getElementById('deliveryExcelRoot');
    if(existing) return existing;

    var headings = Array.from(document.querySelectorAll('h1,h2,h3'));
    var h = headings.find(function(x){ return /delivery tracker|delivery/i.test(x.textContent || ''); });
    var box = h ? (h.closest('.card') || h.parentElement) : null;

    if(!box){
      box = document.querySelector('[data-v="delivery"]') || document.body;
    }

    var root = document.createElement('div');
    root.id = 'deliveryExcelRoot';
    root.className = 'dx-wrap';

    box.innerHTML = '';
    box.appendChild(root);
    return root;
  }

  window.renderDeliveryExcel = function(){
    var root = dxFindDeliveryArea();
    var all = dxDeliveryList();
    var filtered = all.filter(dxMatch);

    var active = filtered.filter(function(d){return dxNormStatus(d,dxGetOrder(d)) === 'out';});
    var waiting = filtered.filter(function(d){return dxNormStatus(d,dxGetOrder(d)) === 'waiting';});
    var delivered = filtered.filter(function(d){return dxNormStatus(d,dxGetOrder(d)) === 'delivered';});

    var cities = dxUniqueCities(all);
    var riders = dxUniqueRiders(all);

    root.innerHTML =
      '<div class="dx-top">' +
        '<div class="dx-search-row"><input class="dx-search" id="dxSearch" placeholder="Search order / customer / recipient / address" value="'+dxEsc(dxState.q)+'" oninput="dxSetSearch(this.value)"></div>' +
        '<div class="dx-chip-row">' +
          ['all','out','waiting','delivered'].map(function(s){
            var label = s==='all'?'All':s==='out'?'Active':s==='waiting'?'Waiting':'Delivered';
            return '<button class="dx-chip '+(dxState.status===s?'on':'')+'" onclick="dxSetStatus(\''+s+'\')">'+label+'</button>';
          }).join('') +
          '<button class="dx-chip '+(dxState.priority==='rush'?'on':'')+'" onclick="dxToggleRush()">🔴 Rush</button>' +
        '</div>' +
        '<div class="dx-filter-row">' +
          '<select class="dx-select" onchange="dxSetPriority(this.value)"><option value="all">Priority: All</option><option value="rush" '+(dxState.priority==='rush'?'selected':'')+'>Rush</option><option value="normal" '+(dxState.priority==='normal'?'selected':'')+'>Normal</option><option value="low" '+(dxState.priority==='low'?'selected':'')+'>Low</option></select>' +
          '<select class="dx-select" onchange="dxSetCity(this.value)"><option value="all">City: All</option>' + cities.map(function(c){return '<option value="'+dxEsc(c[0])+'" '+(dxState.city===c[0]?'selected':'')+'>'+dxEsc(c[1])+'</option>';}).join('') + '</select>' +
          '<select class="dx-select" onchange="dxSetDate(this.value)"><option value="all">Delivery Date: All</option><option value="today" '+(dxState.date==='today'?'selected':'')+'>Today</option><option value="tomorrow" '+(dxState.date==='tomorrow'?'selected':'')+'>Tomorrow</option></select>' +
          '<select class="dx-select" onchange="dxSetRider(this.value)"><option value="all">Rider: All</option><option value="assigned" '+(dxState.rider==='assigned'?'selected':'')+'>Assigned</option><option value="unassigned" '+(dxState.rider==='unassigned'?'selected':'')+'>Not assigned</option>' + riders.map(function(r){return '<option value="'+dxEsc(r[0])+'" '+(dxState.rider===r[0]?'selected':'')+'>'+dxEsc(r[1])+'</option>';}).join('') + '</select>' +
        '</div>' +
      '</div>' +
      dxSection('OUT FOR DELIVERY','out',active) +
      dxSection('WAITING FOR RIDER','wait',waiting) +
      dxSection('DELIVERED HISTORY','done',delivered.slice(0,20)) +
      '<div class="dx-muted" style="padding:8px 2px 18px;font-weight:800">Showing '+filtered.length+' of '+all.length+' delivery orders</div>';
  };

  window.dxSetSearch = function(v){ dxState.q = v; renderDeliveryExcel(); };
  window.dxSetStatus = function(v){ dxState.status = v; renderDeliveryExcel(); };
  window.dxSetPriority = function(v){ dxState.priority = v; renderDeliveryExcel(); };
  window.dxSetCity = function(v){ dxState.city = v; renderDeliveryExcel(); };
  window.dxSetDate = function(v){ dxState.date = v; renderDeliveryExcel(); };
  window.dxSetRider = function(v){ dxState.rider = v; renderDeliveryExcel(); };
  window.dxToggleRush = function(){ dxState.priority = dxState.priority === 'rush' ? 'all' : 'rush'; renderDeliveryExcel(); };

  window.dxShowAddress = function(delId){
    var d = dxDeliveryList().find(function(x){return String(x.id) === String(delId);});
    if(!d) return;
    var o = dxGetOrder(d);
    var txt = 'Address:\\n' + dxAddress(o,d) + '\\n\\nCity:\\n' + dxCity(o,d) + '\\n\\nDelivery Date / Time:\\n' + (o.deliveryDate || o.scheduledDate || '-') + ' ' + (o.deliveryTime || o.scheduledTime || '');
    dxModal('Address Details', txt);
  };

  window.dxShowItems = function(delId){
    var d = dxDeliveryList().find(function(x){return String(x.id) === String(delId);});
    if(!d) return;
    var o = dxGetOrder(d);
    var items = dxItems(o,d);
    var txt = items.length ? items.map(function(it){
      var q = it.q || it.qty || it.quantity || 1;
      var n = it.n || it.name || it.productName || 'Item';
      var p = it.p || it.price || 0;
      return q + 'x ' + n + (p ? ' — ' + dxMoney(p*q) : '');
    }).join('\\n') : 'No item list found.';
    txt += '\\n\\nTotal:\\n' + dxMoney(o.total || d.total || 0);
    dxModal('Items / Total', txt);
  };

  function dxModal(title, text){
    var old = document.getElementById('dxModalBackdrop');
    if(old) old.remove();
    var div = document.createElement('div');
    div.id = 'dxModalBackdrop';
    div.className = 'dx-modal-backdrop';
    div.innerHTML = '<div class="dx-modal"><h3>'+dxEsc(title)+'</h3><pre>'+dxEsc(text)+'</pre><button onclick="document.getElementById(\\'dxModalBackdrop\\').remove()">Close</button></div>';
    document.body.appendChild(div);
  }

  window.dxMarkDelivered = function(delId){
    var d = dxDeliveryList().find(function(x){return String(x.id) === String(delId);});
    if(!d) return alert('Delivery not found: ' + delId);

    var o = dxGetOrder(d);
    var now = Date.now();

    d.status = 'delivered';
    d.deliveryStatus = 'delivered';
    d.deliveredAt = d.deliveredAt || now;
    d.doneAt = d.doneAt || now;

    if(o){
      o.status = o.status === 'cancelled' ? o.status : 'completed';
      o.deliveryStatus = 'delivered';
      o.deliveredAt = o.deliveredAt || now;
      o.deliveryDeliveredAt = o.deliveryDeliveredAt || now;
      o.rider = o.rider || d.rider || d.riderName || '';
      o.riderName = o.riderName || d.riderName || d.rider || '';
    }

    try{ if(typeof addAct === 'function') addAct('✅','Delivery Done',String(delId),'var(--green)'); }catch(e){}
    try{ if(typeof sv === 'function') sv(); }catch(e){}
    try{ if(typeof toast === 'function') toast('Delivery marked delivered'); }catch(e){}
    renderDeliveryExcel();
  };

  var oldRDel = window.rDel;
  window.rDel = function(){
    try{
      renderDeliveryExcel();
    }catch(e){
      console.error('Delivery Excel render failed', e);
      if(typeof oldRDel === 'function') oldRDel.apply(this,arguments);
    }
  };

  document.addEventListener('DOMContentLoaded',function(){
    setTimeout(function(){
      try{ renderDeliveryExcel(); }catch(e){}
    },600);
  });

  setInterval(function(){
    if(document.getElementById('deliveryExcelRoot')){
      try{ renderDeliveryExcel(); }catch(e){}
    }
  },5000);
})();
</script>
'''

if "delivery-excel-renderer-v1" in html:
    print("Delivery Excel patch already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    if insert_at == -1:
        html += patch
    else:
        html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Delivery Excel UI patch added to index.html")
