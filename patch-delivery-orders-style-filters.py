from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="delivery-orders-style-filters-v7">
/* Delivery filters copied from Orders compact filter design */
#deliveryExcelRoot .dx-top{
  opacity:0;
}

#deliveryExcelRoot .dx-top.delivery-filter-ready-v7{
  opacity:1;
}

#deliveryExcelRoot .dx-top.delivery-order-filter-card{
  padding:10px 12px !important;
  margin:0 0 12px !important;
  background:var(--w,#fff) !important;
  border:1px solid var(--b,#e5e7eb) !important;
  border-radius:18px !important;
  box-shadow:0 8px 24px rgba(15,23,42,.04) !important;
}

#deliveryExcelRoot .delivery-filter-min-v7{
  display:flex !important;
  align-items:center !important;
  gap:7px !important;
  overflow-x:auto !important;
  overflow-y:hidden !important;
  -webkit-overflow-scrolling:touch !important;
  scrollbar-width:none !important;
  padding-bottom:2px !important;
}

#deliveryExcelRoot .delivery-filter-min-v7::-webkit-scrollbar{
  display:none !important;
}

#deliveryExcelRoot .delivery-mini-filter{
  flex:0 0 auto !important;
  min-width:92px !important;
  max-width:170px !important;
  padding:7px 10px !important;
  border-radius:999px !important;
  border:1px solid var(--b2,#d1d5db) !important;
  background:var(--w,#fff) !important;
  color:var(--t,#111827) !important;
  font-size:12px !important;
  font-weight:700 !important;
  font-family:inherit !important;
  outline:none !important;
  box-shadow:none !important;
  height:34px !important;
}

#deliveryExcelRoot input.delivery-mini-filter{
  min-width:150px !important;
}

#deliveryExcelRoot input[type="date"].delivery-mini-filter{
  min-width:150px !important;
}

#deliveryExcelRoot .delivery-mini-filter.active,
#deliveryExcelRoot .delivery-mini-filter.on{
  border-color:var(--green,#15803d) !important;
  background:var(--gl,#e9f7ef) !important;
  color:var(--gd,#166534) !important;
}

#deliveryExcelRoot .delivery-reset-btn-v7{
  flex:0 0 auto !important;
  border:1px solid var(--b2,#d1d5db) !important;
  background:var(--w,#fff) !important;
  color:var(--t,#111827) !important;
  border-radius:999px !important;
  padding:7px 12px !important;
  height:34px !important;
  font-size:12px !important;
  font-weight:900 !important;
  font-family:inherit !important;
  cursor:pointer !important;
}

#deliveryExcelRoot .delivery-filter-summary-v7{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:8px;
  margin-top:8px;
  font-size:11px;
  color:var(--t3,#6b7280);
  font-weight:800;
  padding:0 2px;
}

#deliveryExcelRoot .delivery-filter-summary-v7 .active-dot{
  display:none;
  width:7px;
  height:7px;
  border-radius:50%;
  background:var(--orange,#ff6b35);
  box-shadow:0 0 8px rgba(255,107,53,.55);
}

#deliveryExcelRoot .delivery-filter-summary-v7.has-active .active-dot{
  display:inline-block;
}

@media(max-width:768px){
  #deliveryExcelRoot .dx-top.delivery-order-filter-card{
    margin-left:-2px !important;
    margin-right:-2px !important;
  }

  #deliveryExcelRoot .delivery-mini-filter{
    min-width:88px !important;
  }

  #deliveryExcelRoot input.delivery-mini-filter{
    min-width:132px !important;
  }

  #deliveryExcelRoot input[type="date"].delivery-mini-filter{
    min-width:142px !important;
  }
}
</style>

<script id="delivery-orders-style-filters-v7">
(function(){
  if(window.__deliveryOrdersStyleFiltersV7) return;
  window.__deliveryOrdersStyleFiltersV7 = true;

  function esc(v){
    return String(v == null ? '' : v)
      .replaceAll('&','&amp;')
      .replaceAll('<','&lt;')
      .replaceAll('>','&gt;')
      .replaceAll('"','&quot;')
      .replaceAll("'","&#039;");
  }

  function state(){
    window.dxFilterState = window.dxFilterState || {
      q:'',
      status:'all',
      priority:'all',
      city:'all',
      date:'all',
      rider:'all'
    };
    return window.dxFilterState;
  }

  function getRows(){
    return Array.from(document.querySelectorAll('#deliveryExcelRoot tbody tr'));
  }

  function titleCase(v){
    return String(v || '').replace(/\b\w/g,function(x){return x.toUpperCase();});
  }

  function getCities(){
    var map = {};
    getRows().forEach(function(row){
      var c = row.getAttribute('data-dx-city') || '';
      if(c) map[c] = titleCase(c);
    });
    return Object.keys(map).sort().map(function(k){return [k,map[k]];});
  }

  function getRiders(){
    var map = {};
    getRows().forEach(function(row){
      var r = row.getAttribute('data-dx-rider') || '';
      if(r) map[r] = titleCase(r);
    });
    return Object.keys(map).sort().map(function(k){return [k,map[k]];});
  }

  function activeCount(){
    var st = state();
    var n = 0;
    if(st.q) n++;
    if(st.status !== 'all') n++;
    if(st.priority !== 'all') n++;
    if(st.city !== 'all') n++;
    if(st.date !== 'all') n++;
    if(st.rider !== 'all') n++;
    return n;
  }

  function applyFilters(){
    if(typeof window.dxApplyRowFilters === 'function'){
      window.dxApplyRowFilters();
    }

    setTimeout(updateSummary, 0);
  }

  function updateSummary(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    var sum = root.querySelector('.delivery-filter-summary-v7');
    if(!sum) return;

    var rows = getRows();
    var visible = rows.filter(function(r){return r.style.display !== 'none';}).length;
    var active = activeCount();

    sum.classList.toggle('has-active', active > 0);

    var label = active
      ? visible + ' visible • ' + active + ' active filter' + (active > 1 ? 's' : '')
      : 'Showing delivery orders';

    sum.querySelector('.delivery-summary-text').textContent = label;
  }

  function setStatus(v){
    state().status = v || 'all';
    buildFilterBar();
    applyFilters();
  }

  function resetFilters(){
    var st = state();
    st.q = '';
    st.status = 'all';
    st.priority = 'all';
    st.city = 'all';
    st.date = 'all';
    st.rider = 'all';

    buildFilterBar();
    applyFilters();
  }

  window.dxDeliveryOrdersFilterSet = function(key, value){
    var st = state();
    st[key] = value || 'all';
    applyFilters();
    updateActiveControls();
  };

  window.dxDeliveryOrdersFilterSearch = function(value){
    state().q = value || '';
    applyFilters();
  };

  window.dxDeliveryOrdersFilterStatus = setStatus;
  window.dxDeliveryOrdersFilterReset = resetFilters;

  function opt(value,label,current){
    return '<option value="'+esc(value)+'" '+(String(current)===String(value)?'selected':'')+'>'+esc(label)+'</option>';
  }

  function updateActiveControls(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    var st = state();

    root.querySelectorAll('[data-dx-status-pill]').forEach(function(btn){
      var on = btn.getAttribute('data-dx-status-pill') === st.status;
      btn.classList.toggle('active', on);
      btn.classList.toggle('on', on);
    });

    root.querySelectorAll('select.delivery-mini-filter,input.delivery-mini-filter').forEach(function(el){
      var key = el.getAttribute('data-dx-filter-key');
      if(!key) return;
      var active = key === 'q' ? !!st.q : st[key] && st[key] !== 'all';
      el.classList.toggle('active', !!active);
    });

    updateSummary();
  }

  function buildFilterBar(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    var oldTop = root.querySelector('.dx-top');
    if(!oldTop) return;

    var st = state();
    var cities = getCities();
    var riders = getRiders();

    oldTop.className = 'dx-top delivery-order-filter-card delivery-filter-ready-v7';

    oldTop.innerHTML =
      '<div class="delivery-filter-min-v7">' +
        '<input class="delivery-mini-filter" data-dx-filter-key="q" placeholder="Search" value="'+esc(st.q)+'" oninput="dxDeliveryOrdersFilterSearch(this.value)">' +

        '<button type="button" class="delivery-mini-filter" data-dx-status-pill="all" onclick="dxDeliveryOrdersFilterStatus(\'all\')">All</button>' +
        '<button type="button" class="delivery-mini-filter" data-dx-status-pill="out" onclick="dxDeliveryOrdersFilterStatus(\'out\')">Active</button>' +
        '<button type="button" class="delivery-mini-filter" data-dx-status-pill="waiting" onclick="dxDeliveryOrdersFilterStatus(\'waiting\')">Waiting</button>' +
        '<button type="button" class="delivery-mini-filter" data-dx-status-pill="delivered" onclick="dxDeliveryOrdersFilterStatus(\'delivered\')">Delivered</button>' +

        '<select class="delivery-mini-filter" data-dx-filter-key="priority" onchange="dxDeliveryOrdersFilterSet(\'priority\',this.value)">' +
          opt('all','Priority: All',st.priority) +
          opt('rush','Rush',st.priority) +
          opt('normal','Normal',st.priority) +
          opt('low','Low',st.priority) +
        '</select>' +

        '<select class="delivery-mini-filter" data-dx-filter-key="city" onchange="dxDeliveryOrdersFilterSet(\'city\',this.value)">' +
          opt('all','City: All',st.city) +
          cities.map(function(c){return opt(c[0],c[1],st.city);}).join('') +
        '</select>' +

        '<input type="date" class="delivery-mini-filter" data-dx-filter-key="date" value="'+(st.date && !['all','today','tomorrow'].includes(st.date) ? esc(st.date) : '')+'" onchange="dxDeliveryOrdersFilterSet(\'date\',this.value || \'all\')">' +

        '<select class="delivery-mini-filter" data-dx-filter-key="rider" onchange="dxDeliveryOrdersFilterSet(\'rider\',this.value)">' +
          opt('all','Rider: All',st.rider) +
          opt('assigned','Assigned',st.rider) +
          opt('unassigned','Not assigned',st.rider) +
          riders.map(function(r){return opt(r[0],r[1],st.rider);}).join('') +
        '</select>' +

        '<button type="button" class="delivery-reset-btn-v7" onclick="dxDeliveryOrdersFilterReset()">Reset</button>' +
      '</div>' +
      '<div class="delivery-filter-summary-v7"><span><span class="active-dot"></span> <span class="delivery-summary-text">Showing delivery orders</span></span></div>';

    updateActiveControls();
  }

  function wrapRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__ordersStyleFiltersV7) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var result = old.apply(this, arguments);

      setTimeout(function(){
        buildFilterBar();
        applyFilters();
      }, 0);

      setTimeout(function(){
        buildFilterBar();
        applyFilters();
      }, 80);

      return result;
    };

    window.renderDeliveryExcel.__ordersStyleFiltersV7 = true;
    return true;
  }

  function boot(){
    wrapRender();
    buildFilterBar();
    applyFilters();
  }

  setTimeout(boot, 100);
  setTimeout(boot, 500);
  setTimeout(boot, 1200);
})();
</script>
'''

if "delivery-orders-style-filters-v7" in html:
    print("Delivery Orders-style filter patch already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Delivery filters now use Orders-style compact design.")
