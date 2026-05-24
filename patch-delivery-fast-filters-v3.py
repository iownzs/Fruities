from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

removed = 0

# Remove old simple filters v1/v2
for sid in ["delivery-simple-filters-v1", "delivery-simple-filters-v2"]:
    html, c1 = re.subn(r'\s*<style id="'+re.escape(sid)+r'">.*?</style>\s*', '\n', html, flags=re.S)
    html, c2 = re.subn(r'\s*<script id="'+re.escape(sid)+r'">.*?</script>\s*', '\n', html, flags=re.S)
    removed += c1 + c2

patch = r'''
<style id="delivery-fast-filters-v3">
#deliveryExcelRoot .dx-top{
  display:none !important;
}

#deliveryFastFilters{
  padding:10px 12px;
  margin:0 0 12px;
  background:var(--w,#fff);
  border:1px solid var(--b,#e5e7eb);
  border-radius:18px;
}

.delivery-fast-row{
  display:flex;
  gap:7px;
  overflow-x:auto;
  -webkit-overflow-scrolling:touch;
  scrollbar-width:none;
  padding-bottom:2px;
}

.delivery-fast-row::-webkit-scrollbar{
  display:none;
}

.delivery-fast-filter{
  flex:0 0 auto;
  height:34px;
  min-width:88px;
  padding:7px 10px;
  border-radius:999px;
  border:1px solid var(--b2,#d1d5db);
  background:var(--w,#fff);
  color:var(--t,#111827);
  font-size:12px;
  font-weight:800;
  font-family:inherit;
  cursor:pointer;
}

.delivery-fast-filter.on,
.delivery-fast-filter.active{
  border-color:var(--green,#15803d);
  background:var(--gl,#e9f7ef);
  color:var(--gd,#166534);
}

.delivery-fast-filter[type="date"]{
  min-width:145px;
}

.delivery-fast-summary{
  margin-top:8px;
  font-size:11px;
  color:var(--t3,#6b7280);
  font-weight:800;
}

@media(max-width:768px){
  #deliveryFastFilters{
    margin-left:-2px;
    margin-right:-2px;
  }
}
</style>

<script id="delivery-fast-filters-v3">
(function(){
  if(window.__deliveryFastFiltersV3) return;
  window.__deliveryFastFiltersV3 = true;

  var state = {
    status:'all',
    priority:'all',
    date:'all',
    rider:'all'
  };

  var cache = [];

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

  function buildCache(){
    cache = [];

    document.querySelectorAll('#deliveryExcelRoot .dx-section').forEach(function(section){
      var head = section.querySelector('.dx-section-head span');

      if(head && !head.getAttribute('data-base-title')){
        head.setAttribute('data-base-title', (head.textContent || '').replace(/\s*\(\d+\)\s*$/,''));
      }

      section.querySelectorAll('tbody tr').forEach(function(row){
        cache.push({
          row: row,
          section: section,
          head: head,
          status: row.getAttribute('data-dx-status') || '',
          priority: row.getAttribute('data-dx-priority') || '',
          date: row.getAttribute('data-dx-date') || '',
          rider: row.getAttribute('data-dx-rider') || ''
        });
      });
    });
  }

  function match(item){
    if(state.status !== 'all' && item.status !== state.status) return false;
    if(state.priority !== 'all' && item.priority !== state.priority) return false;
    if(state.date !== 'all' && item.date !== state.date) return false;
    if(state.rider === 'assigned' && !item.rider) return false;
    if(state.rider === 'unassigned' && item.rider) return false;
    return true;
  }

  function applyFast(){
    var pos = saveScroll();
    var total = 0;
    var sectionCounts = new Map();

    for(var i=0; i<cache.length; i++){
      var item = cache[i];
      var show = match(item);

      item.row.style.display = show ? '' : 'none';

      if(show){
        total++;
        sectionCounts.set(item.section, (sectionCounts.get(item.section) || 0) + 1);
      }
    }

    sectionCounts.forEach(function(count, section){
      var head = section.querySelector('.dx-section-head span');
      if(head){
        var base = head.getAttribute('data-base-title') || head.textContent.replace(/\s*\(\d+\)\s*$/,'');
        head.textContent = base + ' (' + count + ')';
      }
    });

    document.querySelectorAll('#deliveryExcelRoot .dx-section').forEach(function(section){
      if(!sectionCounts.has(section)){
        var head = section.querySelector('.dx-section-head span');
        if(head){
          var base = head.getAttribute('data-base-title') || head.textContent.replace(/\s*\(\d+\)\s*$/,'');
          head.textContent = base + ' (0)';
        }
      }
    });

    var summary = document.querySelector('#deliveryFastFilters .delivery-fast-summary');
    if(summary){
      var active = ['status','priority','date','rider'].filter(function(k){return state[k] !== 'all';}).length;
      summary.textContent = active
        ? total + ' visible • ' + active + ' active filter' + (active > 1 ? 's' : '')
        : 'Showing delivery orders';
    }

    updateVisuals();
    restoreScroll(pos);
  }

  function updateVisuals(){
    var root = document.getElementById('deliveryFastFilters');
    if(!root) return;

    root.querySelectorAll('[data-status]').forEach(function(btn){
      btn.classList.toggle('on', btn.getAttribute('data-status') === state.status);
    });

    root.querySelectorAll('select').forEach(function(sel){
      var key = sel.getAttribute('data-key');
      sel.value = state[key] || 'all';
      sel.classList.toggle('active', state[key] !== 'all');
    });

    var date = root.querySelector('input[type="date"]');
    if(date){
      date.value = state.date === 'all' ? '' : state.date;
      date.classList.toggle('active', state.date !== 'all');
    }
  }

  function buildFilters(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    var existing = document.getElementById('deliveryFastFilters');
    if(existing) existing.remove();

    var div = document.createElement('div');
    div.id = 'deliveryFastFilters';

    div.innerHTML =
      '<div class="delivery-fast-row">' +
        '<button type="button" class="delivery-fast-filter" data-status="all">All</button>' +
        '<button type="button" class="delivery-fast-filter" data-status="waiting">Waiting</button>' +
        '<button type="button" class="delivery-fast-filter" data-status="out">Out</button>' +
        '<button type="button" class="delivery-fast-filter" data-status="delivered">Delivered</button>' +

        '<select class="delivery-fast-filter" data-key="priority">' +
          '<option value="all">Priority: All</option>' +
          '<option value="rush">Rush</option>' +
          '<option value="normal">Normal</option>' +
          '<option value="low">Low</option>' +
        '</select>' +

        '<input type="date" class="delivery-fast-filter" data-key="date">' +

        '<select class="delivery-fast-filter" data-key="rider">' +
          '<option value="all">Rider: All</option>' +
          '<option value="assigned">Assigned</option>' +
          '<option value="unassigned">Not assigned</option>' +
        '</select>' +

        '<button type="button" class="delivery-fast-filter" data-reset="1">Reset</button>' +
      '</div>' +
      '<div class="delivery-fast-summary">Showing delivery orders</div>';

    root.insertBefore(div, root.firstChild);

    div.addEventListener('click', function(e){
      var statusBtn = e.target.closest('[data-status]');
      if(statusBtn){
        state.status = statusBtn.getAttribute('data-status') || 'all';
        applyFast();
        return;
      }

      var resetBtn = e.target.closest('[data-reset]');
      if(resetBtn){
        state.status = 'all';
        state.priority = 'all';
        state.date = 'all';
        state.rider = 'all';
        applyFast();
        return;
      }
    });

    div.addEventListener('change', function(e){
      var key = e.target.getAttribute('data-key');
      if(!key) return;

      state[key] = e.target.value || 'all';
      applyFast();
    });

    buildCache();
    applyFast();
  }

  function wrapRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__fastFiltersV3) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var pos = saveScroll();
      var result = old.apply(this, arguments);

      buildFilters();
      restoreScroll(pos);

      return result;
    };

    window.renderDeliveryExcel.__fastFiltersV3 = true;
    return true;
  }

  setTimeout(function(){ wrapRender(); buildFilters(); }, 300);
  setTimeout(function(){ wrapRender(); buildFilters(); }, 1200);
})();
</script>
'''

if "delivery-fast-filters-v3" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]

p.write_text(html, encoding="utf-8")
print("DONE: installed fast delivery filters v3.")
print("Removed old simple filter blocks:", removed)
