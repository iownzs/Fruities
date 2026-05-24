from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<script id="delivery-real-filters-v1">
(function(){
  if(window.__deliveryRealFiltersV1) return;
  window.__deliveryRealFiltersV1 = true;

  window.dxFilterState = window.dxFilterState || {
    q: '',
    status: 'all',
    priority: 'all',
    city: 'all',
    date: 'all',
    rider: 'all'
  };

  function lower(v){
    return String(v == null ? '' : v).toLowerCase();
  }

  function normDate(v){
    if(!v) return '';
    try{
      return String(v).slice(0,10);
    }catch(e){
      return '';
    }
  }

  function todayISO(offset){
    var d = new Date();
    d.setDate(d.getDate() + (offset || 0));
    return d.toISOString().slice(0,10);
  }

  function getOrderOfDelivery(d){
    try{
      if(typeof orderOf === 'function') return orderOf(d) || {};
    }catch(e){}

    var id = d.orderId || d.oid || d.order || d.id;
    var arr = window.S && Array.isArray(S.orders) ? S.orders : [];
    return arr.find(function(o){
      return String(o.id || o.orderNumber || o.orderId) === String(id);
    }) || {};
  }

  function statusOf2(d,o){
    var s = lower((o && o.deliveryStatus) || d.deliveryStatus || d.status);

    if(s === 'delivered' || o.deliveredAt || d.deliveredAt) return 'delivered';
    if(s === 'out_for_delivery' || s === 'out' || o.outForDeliveryAt || d.outAt || d.startedAt) return 'out';
    return 'waiting';
  }

  function priorityOf2(d,o){
    var p = lower((o && o.priority) || d.priority || 'normal');
    if(p !== 'rush' && p !== 'low') p = 'normal';
    return p;
  }

  function cityOf2(d,o){
    var c = (o && o.city) || d.city || '';
    if(c) return lower(c);

    var a = lower((o && (o.deliveryAddress || o.addr || o.address)) || d.deliveryAddress || d.addr || d.address);
    var cities = ['caloocan','manila','quezon city','valenzuela','malabon','navotas','makati','pasig','taguig','pasay'];
    for(var i=0;i<cities.length;i++){
      if(a.indexOf(cities[i]) !== -1) return cities[i];
    }

    return 'other';
  }

  function riderOf2(d,o){
    return lower((o && (o.rider || o.riderName)) || d.rider || d.riderName);
  }

  function deliveryDateOf2(d,o){
    return normDate((o && (o.deliveryDate || o.delivery_date || o.scheduledDate)) || d.deliveryDate || d.delivery_date);
  }

  function textBlob(d,o){
    return lower([
      d.id,d.orderId,d.oid,d.order,
      o.id,o.orderNumber,o.orderId,
      o.cust,o.customerName,o.phone,o.customerPhone,
      o.recipient,o.recipientName,o.recipientPhone,
      o.deliveryAddress,o.addr,o.address,
      cityOf2(d,o),
      priorityOf2(d,o),
      statusOf2(d,o)
    ].join(' '));
  }

  function matchesFilter(d){
    var o = getOrderOfDelivery(d);
    var st = window.dxFilterState;
    var status = statusOf2(d,o);
    var priority = priorityOf2(d,o);
    var city = cityOf2(d,o);
    var rider = riderOf2(d,o);
    var delDate = deliveryDateOf2(d,o);

    if(st.status !== 'all' && st.status !== status) return false;
    if(st.priority !== 'all' && st.priority !== priority) return false;
    if(st.city !== 'all' && st.city !== city) return false;

    if(st.rider === 'assigned' && !rider) return false;
    if(st.rider === 'unassigned' && rider) return false;
    if(st.rider !== 'all' && st.rider !== 'assigned' && st.rider !== 'unassigned' && rider !== st.rider) return false;

    if(st.date === 'today' && delDate !== todayISO(0)) return false;
    if(st.date === 'tomorrow' && delDate !== todayISO(1)) return false;

    if(st.q && textBlob(d,o).indexOf(lower(st.q)) === -1) return false;

    return true;
  }

  function uniqueCities(list){
    var map = {};
    list.forEach(function(d){
      var o = getOrderOfDelivery(d);
      var c = cityOf2(d,o);
      map[c] = c.replace(/\b\w/g, function(x){return x.toUpperCase();});
    });
    return Object.keys(map).sort().map(function(k){return [k,map[k]];});
  }

  function uniqueRiders(list){
    var map = {};
    list.forEach(function(d){
      var o = getOrderOfDelivery(d);
      var r = riderOf2(d,o);
      if(r) map[r] = ((o && (o.rider || o.riderName)) || d.rider || d.riderName);
    });
    return Object.keys(map).sort().map(function(k){return [k,map[k]];});
  }

  function filterBar(all){
    var st = window.dxFilterState;
    var cities = uniqueCities(all);
    var riders = uniqueRiders(all);

    function chip(key,label){
      return '<button type="button" class="dx-chip '+(st.status===key?'on':'')+'" onclick="dxFilterSetStatus(\''+key+'\')">'+label+'</button>';
    }

    return '' +
      '<div class="dx-top">' +
        '<div class="dx-search-row"><input class="dx-search" placeholder="Search order / customer / recipient / address" value="'+String(st.q).replace(/"/g,'&quot;')+'" oninput="dxFilterSearch(this.value)"></div>' +
        '<div class="dx-chip-row">' +
          chip('all','All') +
          chip('out','Active') +
          chip('waiting','Waiting') +
          chip('delivered','Delivered') +
          '<button type="button" class="dx-chip '+(st.priority==='rush'?'on':'')+'" onclick="dxFilterRush()">🔴 Rush</button>' +
        '</div>' +
        '<div class="dx-filter-row">' +
          '<select class="dx-select" onchange="dxFilterPriority(this.value)">' +
            '<option value="all">Priority: All</option>' +
            '<option value="rush" '+(st.priority==='rush'?'selected':'')+'>Rush</option>' +
            '<option value="normal" '+(st.priority==='normal'?'selected':'')+'>Normal</option>' +
            '<option value="low" '+(st.priority==='low'?'selected':'')+'>Low</option>' +
          '</select>' +
          '<select class="dx-select" onchange="dxFilterCity(this.value)"><option value="all">City: All</option>' +
            cities.map(function(c){return '<option value="'+c[0]+'" '+(st.city===c[0]?'selected':'')+'>'+c[1]+'</option>';}).join('') +
          '</select>' +
          '<select class="dx-select" onchange="dxFilterDate(this.value)">' +
            '<option value="all">Delivery Date: All</option>' +
            '<option value="today" '+(st.date==='today'?'selected':'')+'>Today</option>' +
            '<option value="tomorrow" '+(st.date==='tomorrow'?'selected':'')+'>Tomorrow</option>' +
          '</select>' +
          '<select class="dx-select" onchange="dxFilterRider(this.value)"><option value="all">Rider: All</option><option value="assigned" '+(st.rider==='assigned'?'selected':'')+'>Assigned</option><option value="unassigned" '+(st.rider==='unassigned'?'selected':'')+'>Not assigned</option>' +
            riders.map(function(r){return '<option value="'+r[0]+'" '+(st.rider===r[0]?'selected':'')+'>'+r[1]+'</option>';}).join('') +
          '</select>' +
        '</div>' +
      '</div>';
  }

  function replaceFilterBar(all){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    var oldTop = root.querySelector('.dx-top');
    if(oldTop){
      oldTop.outerHTML = filterBar(all);
    }
  }

  function enhanceRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__realFiltersV1) return true;

    var oldRender = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var oldDeliveriesFn = null;

      if(typeof window.deliveries === 'function'){
        oldDeliveriesFn = window.deliveries;
      }

      var result = oldRender.apply(this, arguments);

      try{
        var all = [];
        if(window.S && Array.isArray(S.deliveries)){
          all = S.deliveries.slice();
        }

        if(typeof window.deliveries === 'function'){
          all = window.deliveries();
        }

        var filtered = all.filter(matchesFilter);

        // If the original simple renderer didn't filter, rebuild sections using available section/table functions if exposed.
        // Safer fallback: hide rows by matching visible order text is avoided, so we re-render through existing functions only when possible.
        replaceFilterBar(all);

        if(typeof window.__dxFilterRebuild === 'function'){
          window.__dxFilterRebuild(filtered);
        }
      }catch(e){
        console.warn('delivery real filter post render failed', e);
      }

      return result;
    };

    window.renderDeliveryExcel.__realFiltersV1 = true;
    return true;
  }

  window.dxFilterSearch = function(v){ dxFilterState.q = v; renderDeliveryExcel(); };
  window.dxFilterSetStatus = function(v){ dxFilterState.status = v; renderDeliveryExcel(); };
  window.dxFilterPriority = function(v){ dxFilterState.priority = v; renderDeliveryExcel(); };
  window.dxFilterCity = function(v){ dxFilterState.city = v; renderDeliveryExcel(); };
  window.dxFilterDate = function(v){ dxFilterState.date = v; renderDeliveryExcel(); };
  window.dxFilterRider = function(v){ dxFilterState.rider = v; renderDeliveryExcel(); };
  window.dxFilterRush = function(){ dxFilterState.priority = dxFilterState.priority === 'rush' ? 'all' : 'rush'; renderDeliveryExcel(); };

  // Lightweight row filter fallback: hide/show rows after render.
  window.dxApplyRowFilters = function(){
    document.querySelectorAll('.dx-section').forEach(function(section){
      var visible = 0;
      section.querySelectorAll('tbody tr').forEach(function(row){
        var text = lower(row.textContent || '');
        var st = dxFilterState;
        var show = true;

        if(st.q && text.indexOf(lower(st.q)) === -1) show = false;
        if(st.priority !== 'all' && text.indexOf(st.priority) === -1) show = false;
        if(st.status === 'waiting' && text.indexOf('waiting') === -1) show = false;
        if(st.status === 'out' && text.indexOf('out for delivery') === -1) show = false;
        if(st.status === 'delivered' && text.indexOf('delivered') === -1) show = false;
        if(st.city !== 'all' && text.indexOf(st.city) === -1) show = false;
        if(st.rider === 'assigned' && text.indexOf('not assigned') !== -1) show = false;
        if(st.rider === 'unassigned' && text.indexOf('not assigned') === -1) show = false;

        row.style.display = show ? '' : 'none';
        if(show) visible++;
      });
    });
  };

  var oldRenderLater = null;
  setTimeout(function(){
    enhanceRender();

    if(typeof window.renderDeliveryExcel === 'function' && !window.renderDeliveryExcel.__rowFilterWrapV1){
      oldRenderLater = window.renderDeliveryExcel;

      window.renderDeliveryExcel = function(){
        var result = oldRenderLater.apply(this, arguments);
        replaceFilterBar((window.S && Array.isArray(S.deliveries)) ? S.deliveries : []);
        setTimeout(window.dxApplyRowFilters, 0);
        return result;
      };

      window.renderDeliveryExcel.__rowFilterWrapV1 = true;
    }
  },500);

  setTimeout(enhanceRender,1500);
})();
</script>
'''

if "delivery-real-filters-v1" in html:
    print("Delivery real filters already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Delivery real filters added.")
