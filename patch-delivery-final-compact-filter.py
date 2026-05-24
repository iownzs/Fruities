from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="delivery-final-compact-filter-v10">
/* Final delivery filter stabilizer: hide old filter UI until final compact bar is ready */
#deliveryExcelRoot .dx-top{
  opacity:0 !important;
  height:0 !important;
  overflow:hidden !important;
  margin:0 !important;
  padding:0 !important;
  pointer-events:none !important;
}

#deliveryExcelRoot .dx-top.delivery-final-filter-card{
  opacity:1 !important;
  height:auto !important;
  overflow:visible !important;
  pointer-events:auto !important;
  padding:10px 12px !important;
  margin:0 0 12px !important;
  background:var(--w,#fff) !important;
  border:1px solid var(--b,#e5e7eb) !important;
  border-radius:18px !important;
  box-shadow:0 8px 24px rgba(15,23,42,.04) !important;
}

.delivery-final-filter-row{
  display:flex !important;
  align-items:center !important;
  gap:7px !important;
  overflow-x:auto !important;
  overflow-y:hidden !important;
  -webkit-overflow-scrolling:touch !important;
  scrollbar-width:none !important;
  padding-bottom:2px !important;
}

.delivery-final-filter-row::-webkit-scrollbar{
  display:none !important;
}

.delivery-final-filter{
  flex:0 0 auto !important;
  min-width:92px !important;
  max-width:170px !important;
  height:34px !important;
  padding:7px 10px !important;
  border-radius:999px !important;
  border:1px solid var(--b2,#d1d5db) !important;
  background:var(--w,#fff) !important;
  color:var(--t,#111827) !important;
  font-size:12px !important;
  font-weight:800 !important;
  font-family:inherit !important;
  outline:none !important;
  cursor:pointer !important;
}

.delivery-final-filter.active,
.delivery-final-filter.on{
  border-color:var(--green,#15803d) !important;
  background:var(--gl,#e9f7ef) !important;
  color:var(--gd,#166534) !important;
}

.delivery-final-filter[type="date"]{
  min-width:145px !important;
}

.delivery-final-reset{
  min-width:82px !important;
}

.delivery-final-summary{
  margin-top:8px;
  font-size:11px;
  color:var(--t3,#6b7280);
  font-weight:800;
  padding:0 2px;
}

@media(max-width:768px){
  #deliveryExcelRoot .dx-top.delivery-final-filter-card{
    margin-left:-2px !important;
    margin-right:-2px !important;
  }

  .delivery-final-filter{
    min-width:86px !important;
  }

  .delivery-final-filter[type="date"]{
    min-width:138px !important;
  }
}
</style>

<script id="delivery-final-compact-filter-v10">
(function(){
  if(window.__deliveryFinalCompactFilterV10) return;
  window.__deliveryFinalCompactFilterV10 = true;

  window.dxFinalFilterState = window.dxFinalFilterState || {
    status:'all',
    priority:'all',
    city:'all',
    date:'all',
    rider:'all'
  };

  function st(){ return window.dxFinalFilterState; }

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

  function rows(){
    return Array.from(document.querySelectorAll('#deliveryExcelRoot tbody tr'));
  }

  function titleCase(v){
    return String(v || '').replace(/\b\w/g,function(x){return x.toUpperCase();});
  }

  function uniqueAttr(attr){
    var map = {};
    rows().forEach(function(row){
      var v = row.getAttribute(attr) || '';
      if(v) map[v] = titleCase(v);
    });
    return Object.keys(map).sort().map(function(k){return [k,map[k]];});
  }

  function todayISO(offset){
    var d = new Date();
    d.setDate(d.getDate() + (offset || 0));
    return d.toISOString().slice(0,10);
  }

  function applyFinalFilters(){
    var s = st();
    var visibleTotal = 0;

    document.querySelectorAll('#deliveryExcelRoot .dx-section').forEach(function(section){
      var visible = 0;

      section.querySelectorAll('tbody tr').forEach(function(row){
        var show = true;
        var status = row.getAttribute('data-dx-status') || '';
        var priority = row.getAttribute('data-dx-priority') || '';
        var city = row.getAttribute('data-dx-city') || '';
        var rider = row.getAttribute('data-dx-rider') || '';
        var date = row.getAttribute('data-dx-date') || '';

        if(s.status !== 'all' && status !== s.status) show = false;
        if(s.priority !== 'all' && priority !== s.priority) show = false;
        if(s.city !== 'all' && city !== s.city) show = false;

        if(s.rider === 'assigned' && !rider) show = false;
        if(s.rider === 'unassigned' && rider) show = false;
        if(s.rider !== 'all' && s.rider !== 'assigned' && s.rider !== 'unassigned' && rider !== s.rider) show = false;

        if(s.date === 'today' && date !== todayISO(0)) show = false;
        else if(s.date === 'tomorrow' && date !== todayISO(1)) show = false;
        else if(s.date !== 'all' && s.date !== 'today' && s.date !== 'tomorrow' && date !== s.date) show = false;

        row.style.display = show ? '' : 'none';

        if(show){
          visible++;
          visibleTotal++;
        }
      });

      var head = section.querySelector('.dx-section-head span');
      if(head){
        if(!head.getAttribute('data-base-title')){
          head.setAttribute('data-base-title', (head.textContent || '').replace(/\s*\(\d+\)\s*$/,''));
        }
        head.textContent = head.getAttribute('data-base-title') + ' (' + visible + ')';
      }
    });

    var summary = document.querySelector('#deliveryExcelRoot .delivery-final-summary');
    if(summary){
      var active = ['status','priority','city','date','rider'].filter(function(k){ return s[k] && s[k] !== 'all'; }).length;
      summary.textContent = active
        ? visibleTotal + ' visible • ' + active + ' active filter' + (active > 1 ? 's' : '')
        : 'Showing delivery orders';
    }
  }

  function opt(value,label,current){
    return '<option value="'+esc(value)+'" '+(String(current)===String(value)?'selected':'')+'>'+esc(label)+'</option>';
  }

  function btnStatus(value,label){
    var on = st().status === value;
    return '<button type="button" class="delivery-final-filter '+(on?'on active':'')+'" onclick="dxFinalSetStatus(\''+value+'\')">'+esc(label)+'</button>';
  }

  function buildFinalFilter(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    var top = root.querySelector('.dx-top');
    if(!top) return;

    var s = st();
    var cities = uniqueAttr('data-dx-city');
    var riders = uniqueAttr('data-dx-rider');

    top.className = 'dx-top delivery-final-filter-card';

    top.innerHTML =
      '<div class="delivery-final-filter-row">' +
        btnStatus('all','All') +
        btnStatus('out','Active') +
        btnStatus('waiting','Waiting') +
        btnStatus('delivered','Delivered') +

        '<select class="delivery-final-filter '+(s.priority !== 'all' ? 'active' : '')+'" onchange="dxFinalSetFilter(\'priority\',this.value)">' +
          opt('all','Priority: All',s.priority) +
          opt('rush','Rush',s.priority) +
          opt('normal','Normal',s.priority) +
          opt('low','Low',s.priority) +
        '</select>' +

        '<select class="delivery-final-filter '+(s.city !== 'all' ? 'active' : '')+'" onchange="dxFinalSetFilter(\'city\',this.value)">' +
          opt('all','City: All',s.city) +
          cities.map(function(c){return opt(c[0],c[1],s.city);}).join('') +
        '</select>' +

        '<input type="date" class="delivery-final-filter '+(s.date !== 'all' ? 'active' : '')+'" value="'+(s.date !== 'all' ? esc(s.date) : '')+'" onchange="dxFinalSetFilter(\'date\',this.value || \'all\')">' +

        '<select class="delivery-final-filter '+(s.rider !== 'all' ? 'active' : '')+'" onchange="dxFinalSetFilter(\'rider\',this.value)">' +
          opt('all','Rider: All',s.rider) +
          opt('assigned','Assigned',s.rider) +
          opt('unassigned','Not assigned',s.rider) +
          riders.map(function(r){return opt(r[0],r[1],s.rider);}).join('') +
        '</select>' +

        '<button type="button" class="delivery-final-filter delivery-final-reset" onclick="dxFinalResetFilters()">Reset</button>' +
      '</div>' +
      '<div class="delivery-final-summary">Showing delivery orders</div>';

    applyFinalFilters();
  }

  window.dxFinalSetStatus = function(value){
    var pos = saveScroll();
    st().status = value || 'all';
    buildFinalFilter();
    applyFinalFilters();
    restoreScroll(pos);
    setTimeout(function(){ restoreScroll(pos); }, 80);
    return false;
  };

  window.dxFinalSetFilter = function(key,value){
    var pos = saveScroll();
    st()[key] = value || 'all';
    buildFinalFilter();
    applyFinalFilters();
    restoreScroll(pos);
    setTimeout(function(){ restoreScroll(pos); }, 80);
    return false;
  };

  window.dxFinalResetFilters = function(){
    var pos = saveScroll();
    window.dxFinalFilterState = {status:'all',priority:'all',city:'all',date:'all',rider:'all'};
    buildFinalFilter();
    applyFinalFilters();
    restoreScroll(pos);
    setTimeout(function(){ restoreScroll(pos); }, 80);
    return false;
  };

  function wrapRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__finalCompactFilterV10) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var pos = saveScroll();
      var result = old.apply(this, arguments);

      buildFinalFilter();
      restoreScroll(pos);

      setTimeout(function(){
        buildFinalFilter();
        restoreScroll(pos);
      }, 50);

      return result;
    };

    window.renderDeliveryExcel.__finalCompactFilterV10 = true;
    return true;
  }

  function protectFilterClicks(){
    document.addEventListener('click', function(e){
      if(!e.target.closest || !e.target.closest('#deliveryExcelRoot .delivery-final-filter-row')) return;
      var pos = saveScroll();
      setTimeout(function(){ restoreScroll(pos); }, 0);
      setTimeout(function(){ restoreScroll(pos); }, 80);
      setTimeout(function(){ restoreScroll(pos); }, 180);
    }, true);

    document.addEventListener('change', function(e){
      if(!e.target.closest || !e.target.closest('#deliveryExcelRoot .delivery-final-filter-row')) return;
      var pos = saveScroll();
      setTimeout(function(){ restoreScroll(pos); }, 0);
      setTimeout(function(){ restoreScroll(pos); }, 80);
      setTimeout(function(){ restoreScroll(pos); }, 180);
    }, true);
  }

  protectFilterClicks();

  setTimeout(function(){ wrapRender(); buildFinalFilter(); }, 100);
  setTimeout(function(){ wrapRender(); buildFinalFilter(); }, 500);
  setTimeout(function(){ wrapRender(); buildFinalFilter(); }, 1200);
})();
</script>
'''

if "delivery-final-compact-filter-v10" in html:
    print("Final compact filter already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Final compact delivery filter added.")
