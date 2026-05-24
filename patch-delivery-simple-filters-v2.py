from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

removed = 0

# Remove old simple filter v1
for sid in ["delivery-simple-filters-v1"]:
    html, c1 = re.subn(r'\s*<style id="'+re.escape(sid)+r'">.*?</style>\s*', '\n', html, flags=re.S)
    html, c2 = re.subn(r'\s*<script id="'+re.escape(sid)+r'">.*?</script>\s*', '\n', html, flags=re.S)
    removed += c1 + c2

patch = r'''
<style id="delivery-simple-filters-v2">
#deliveryExcelRoot .dx-top{
  display:none !important;
}

#deliverySimpleFilters{
  padding:10px 12px;
  margin:0 0 12px;
  background:var(--w,#fff);
  border:1px solid var(--b,#e5e7eb);
  border-radius:18px;
}

.delivery-simple-filter-row{
  display:flex;
  gap:7px;
  overflow-x:auto;
  -webkit-overflow-scrolling:touch;
  scrollbar-width:none;
  padding-bottom:2px;
}

.delivery-simple-filter-row::-webkit-scrollbar{
  display:none;
}

.delivery-simple-filter{
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

.delivery-simple-filter.on,
.delivery-simple-filter.active{
  border-color:var(--green,#15803d);
  background:var(--gl,#e9f7ef);
  color:var(--gd,#166534);
}

.delivery-simple-filter[type="date"]{
  min-width:145px;
}

.delivery-simple-summary{
  margin-top:8px;
  font-size:11px;
  color:var(--t3,#6b7280);
  font-weight:800;
}

@media(max-width:768px){
  #deliverySimpleFilters{
    margin-left:-2px;
    margin-right:-2px;
  }
}
</style>

<script id="delivery-simple-filters-v2">
(function(){
  if(window.__deliverySimpleFiltersV2) return;
  window.__deliverySimpleFiltersV2 = true;

  var state = {
    status:'all',
    priority:'all',
    date:'all',
    rider:'all'
  };

  var raf = null;

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

  function getSections(){
    return Array.from(document.querySelectorAll('#deliveryExcelRoot .dx-section'));
  }

  function applyNow(){
    var visibleTotal = 0;

    getSections().forEach(function(section){
      var visible = 0;
      var rows = Array.from(section.querySelectorAll('tbody tr'));

      rows.forEach(function(row){
        var show = true;

        var status = row.getAttribute('data-dx-status') || '';
        var priority = row.getAttribute('data-dx-priority') || '';
        var date = row.getAttribute('data-dx-date') || '';
        var rider = row.getAttribute('data-dx-rider') || '';

        if(state.status !== 'all' && status !== state.status) show = false;
        if(state.priority !== 'all' && priority !== state.priority) show = false;
        if(state.date !== 'all' && date !== state.date) show = false;
        if(state.rider === 'assigned' && !rider) show = false;
        if(state.rider === 'unassigned' && rider) show = false;

        row.hidden = !show;

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

    var summary = document.querySelector('#deliverySimpleFilters .delivery-simple-summary');
    if(summary){
      var active = ['status','priority','date','rider'].filter(function(k){return state[k] !== 'all';}).length;
      summary.textContent = active
        ? visibleTotal + ' visible • ' + active + ' active filter' + (active > 1 ? 's' : '')
        : 'Showing delivery orders';
    }

    updateVisuals();
  }

  function scheduleApply(){
    if(raf) cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function(){
      raf = null;
      applyNow();
    });
  }

  function updateVisuals(){
    var root = document.getElementById('deliverySimpleFilters');
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

    var existing = document.getElementById('deliverySimpleFilters');
    if(existing) existing.remove();

    var div = document.createElement('div');
    div.id = 'deliverySimpleFilters';

    div.innerHTML =
      '<div class="delivery-simple-filter-row">' +
        '<button type="button" class="delivery-simple-filter" data-status="all">All</button>' +
        '<button type="button" class="delivery-simple-filter" data-status="waiting">Waiting</button>' +
        '<button type="button" class="delivery-simple-filter" data-status="out">Out</button>' +
        '<button type="button" class="delivery-simple-filter" data-status="delivered">Delivered</button>' +

        '<select class="delivery-simple-filter" data-key="priority">' +
          '<option value="all">Priority: All</option>' +
          '<option value="rush">Rush</option>' +
          '<option value="normal">Normal</option>' +
          '<option value="low">Low</option>' +
        '</select>' +

        '<input type="date" class="delivery-simple-filter" data-key="date">' +

        '<select class="delivery-simple-filter" data-key="rider">' +
          '<option value="all">Rider: All</option>' +
          '<option value="assigned">Assigned</option>' +
          '<option value="unassigned">Not assigned</option>' +
        '</select>' +

        '<button type="button" class="delivery-simple-filter" data-reset="1">Reset</button>' +
      '</div>' +
      '<div class="delivery-simple-summary">Showing delivery orders</div>';

    root.insertBefore(div, root.firstChild);

    div.addEventListener('click', function(e){
      var pos = saveScroll();

      var statusBtn = e.target.closest('[data-status]');
      if(statusBtn){
        state.status = statusBtn.getAttribute('data-status') || 'all';
        scheduleApply();
        restoreScroll(pos);
        return;
      }

      var resetBtn = e.target.closest('[data-reset]');
      if(resetBtn){
        state.status = 'all';
        state.priority = 'all';
        state.date = 'all';
        state.rider = 'all';
        scheduleApply();
        restoreScroll(pos);
        return;
      }
    });

    div.addEventListener('change', function(e){
      var pos = saveScroll();

      var key = e.target.getAttribute('data-key');
      if(!key) return;

      state[key] = e.target.value || 'all';
      scheduleApply();
      restoreScroll(pos);
    });

    updateVisuals();
    scheduleApply();
  }

  function wrapRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__simpleFiltersV2) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var pos = saveScroll();
      var result = old.apply(this, arguments);

      buildFilters();
      restoreScroll(pos);

      return result;
    };

    window.renderDeliveryExcel.__simpleFiltersV2 = true;
    return true;
  }

  setTimeout(function(){ wrapRender(); buildFilters(); }, 300);
  setTimeout(function(){ wrapRender(); buildFilters(); }, 1200);
})();
</script>
'''

if "delivery-simple-filters-v2" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]

p.write_text(html, encoding="utf-8")
print("DONE: replaced simple filters v1 with optimized v2.")
print("Removed old blocks:", removed)
