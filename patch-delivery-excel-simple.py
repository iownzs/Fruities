from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<script id="delivery-excel-simple-v5">
(function(){
  if(window.__deliveryExcelSimpleV5) return;
  window.__deliveryExcelSimpleV5 = true;

  function esc(v){
    return String(v == null ? '' : v)
      .replaceAll('&','&amp;')
      .replaceAll('<','&lt;')
      .replaceAll('>','&gt;')
      .replaceAll('"','&quot;')
      .replaceAll("'","&#039;");
  }

  function money(v){
    var n = Number(v || 0);
    return '₱' + n.toLocaleString('en-PH',{maximumFractionDigits:2});
  }

  function orders(){
    return window.S && Array.isArray(S.orders) ? S.orders : [];
  }

  function deliveries(){
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
  }

  function orderOf(d){
    var id = d.orderId || d.oid || d.order || d.id;
    return orders().find(function(o){
      return String(o.id || o.orderNumber || o.orderId) === String(id);
    }) || {};
  }

  function statusOf(d,o){
    var s = String(o.deliveryStatus || d.deliveryStatus || d.status || '').toLowerCase();

    if(s === 'delivered' || o.deliveredAt || d.deliveredAt) return 'delivered';
    if(s === 'out_for_delivery' || s === 'out' || s === 'out for delivery') return 'out';
    if(o.rider || o.riderName || d.rider || d.riderName){
      if(s !== 'waiting') return 'out';
    }

    return 'waiting';
  }

  function statusLabel(s){
    if(s === 'out') return 'Out for Delivery';
    if(s === 'delivered') return 'Delivered';
    return 'Waiting for Rider';
  }

  function priorityOf(o,d){
    var p = String(o.priority || d.priority || 'normal').toLowerCase();
    if(p !== 'rush' && p !== 'low') p = 'normal';
    return p;
  }

  function created(o,d){
    var raw = o.createdAt || o.time || d.createdAt || d.time || '';
    if(!raw) return '-';
    try{
      var dt = new Date(raw);
      if(isNaN(dt.getTime())) return raw;
      return dt.toLocaleTimeString('en-PH',{hour:'numeric',minute:'2-digit'});
    }catch(e){
      return raw;
    }
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

  function cityOf(o,d){
    var c = o.city || d.city || '';
    if(c) return c;

    var a = String(address(o,d)).toLowerCase();
    var cities = ['caloocan','manila','quezon city','valenzuela','malabon','navotas','makati','pasig','taguig','pasay'];
    for(var i=0;i<cities.length;i++){
      if(a.indexOf(cities[i]) !== -1){
        return cities[i].replace(/\b\w/g,function(x){return x.toUpperCase();});
      }
    }
    return 'Other';
  }

  function deliveryDate(o,d){
    var date = o.deliveryDate || o.delivery_date || o.scheduledDate || d.deliveryDate || '';
    var time = o.deliveryTime || o.delivery_time || o.scheduledTime || d.deliveryTime || '';
    return (date || '-') + (time ? '<br>' + esc(time) : '');
  }

  function itemText(o,d){
    var items = Array.isArray(o.items) ? o.items : (Array.isArray(d.items) ? d.items : []);
    var total = o.total || d.total || 0;
    var count = items.length;
    return (count ? count + ' item' + (count === 1 ? '' : 's') : 'Items') + '<br><b>' + money(total) + '</b>';
  }

  function riderTimer(d,o,s){
    var rider = o.rider || o.riderName || d.rider || d.riderName || '';

    if(s === 'waiting'){
      return '<span class="dx-muted">Not assigned<br>-</span>';
    }

    if(s === 'delivered'){
      return esc(rider || '-') + '<br><span class="dx-timer">Delivered</span>';
    }

    return esc(rider || '-') + '<br><span class="dx-timer">Running</span>';
  }

  function action(d,o,s){
    var id = esc(d.id || d.orderId || o.id || o.orderNumber || '');
    if(s === 'out'){
      return '<button class="dx-action" onclick="dxSimpleDone(\''+id+'\')">Done</button>';
    }
    if(s === 'delivered'){
      return '<button class="dx-action view">View</button>';
    }
    return '<button class="dx-action assign" onclick="quickAssignRider(\''+id+'\')">Assign</button>';
  }

  function row(d){
    var o = orderOf(d);
    var s = statusOf(d,o);
    var p = priorityOf(o,d);
    var id = d.id || d.orderId || o.id || o.orderNumber || '-';
    var a = address(o,d);
    var shortAddr = String(a).length > 26 ? String(a).slice(0,26) + '...' : String(a);

    return '<tr>' +
      '<td><div class="dx-order">'+esc(id)+'</div><span class="dx-prio '+esc(p)+'">'+esc(p.charAt(0).toUpperCase()+p.slice(1))+'</span></td>' +
      '<td><span class="dx-status '+(s === 'out' ? 'out' : s === 'delivered' ? 'delivered' : 'wait')+'">'+esc(statusLabel(s))+'</span></td>' +
      '<td>'+esc(created(o,d))+'</td>' +
      '<td><div class="dx-name">'+esc(customer(o,d))+'</div><div class="dx-phone">'+esc(customerPhone(o,d))+'</div></td>' +
      '<td><div class="dx-name">'+esc(recipient(o,d))+'</div><div class="dx-phone">'+esc(recipientPhone(o,d))+'</div></td>' +
      '<td style="min-width:180px">'+esc(shortAddr)+'<br><span class="dx-muted">'+esc(cityOf(o,d))+'</span></td>' +
      '<td style="min-width:110px">'+deliveryDate(o,d)+'</td>' +
      '<td style="min-width:110px">'+itemText(o,d)+'</td>' +
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
      '</tr></thead><tbody>' + list.map(row).join('') + '</tbody></table></div>';
  }

  function section(title, cls, list){
    return '<section class="dx-section">' +
      '<div class="dx-section-head '+cls+'"><span>'+esc(title)+' ('+list.length+')</span><span>⌃</span></div>' +
      table(list) +
    '</section>';
  }

  window.renderDeliveryExcel = function(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    var all = deliveries();

    var active = [];
    var waiting = [];
    var delivered = [];

    all.forEach(function(d){
      var o = orderOf(d);
      var s = statusOf(d,o);
      if(s === 'out') active.push(d);
      else if(s === 'delivered') delivered.push(d);
      else waiting.push(d);
    });

    root.innerHTML =
      '<div class="dx-top">' +
        '<div class="dx-search-row"><input class="dx-search" placeholder="Search order / customer / recipient / address"></div>' +
        '<div class="dx-chip-row">' +
          '<button class="dx-chip on">All</button>' +
          '<button class="dx-chip">Active</button>' +
          '<button class="dx-chip">Waiting</button>' +
          '<button class="dx-chip">Delivered</button>' +
          '<button class="dx-chip">🔴 Rush</button>' +
        '</div>' +
        '<div class="dx-filter-row">' +
          '<select class="dx-select"><option>Priority: All</option></select>' +
          '<select class="dx-select"><option>City: All</option></select>' +
          '<select class="dx-select"><option>Delivery Date: All</option></select>' +
          '<select class="dx-select"><option>Rider: All</option></select>' +
        '</div>' +
      '</div>' +
      section('OUT FOR DELIVERY','out',active) +
      section('WAITING FOR RIDER','wait',waiting) +
      section('DELIVERED HISTORY','done',delivered.slice(0,20)) +
      '<div class="dx-muted" style="padding:8px 2px 18px;font-weight:800">Showing '+all.length+' delivery orders</div>';
  };

  window.dxSimpleDone = function(id){
    var d = deliveries().find(function(x){return String(x.id || x.orderId) === String(id);});
    if(!d) return alert('Delivery not found: ' + id);

    var o = orderOf(d);
    d.status = 'delivered';
    d.deliveryStatus = 'delivered';
    d.deliveredAt = Date.now();

    if(o){
      o.deliveryStatus = 'delivered';
      o.deliveredAt = Date.now();
      o.status = 'completed';
    }

    try{ if(typeof sv === 'function') sv(); }catch(e){}
    try{ if(typeof toast === 'function') toast('Delivery marked done'); }catch(e){}
    renderDeliveryExcel();
  };

  function boot(){
    if(document.getElementById('deliveryExcelRoot')){
      renderDeliveryExcel();
    }
  }

  window.addEventListener('load',function(){
    setTimeout(boot,300);
    setTimeout(boot,1000);
    setTimeout(boot,2500);
  });

  document.addEventListener('DOMContentLoaded',function(){
    setTimeout(boot,300);
    setTimeout(boot,1000);
  });

  setInterval(boot,3000);
})();
</script>
'''

if "delivery-excel-simple-v5" in html:
    print("Simple renderer already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Simple delivery renderer added.")
