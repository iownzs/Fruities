from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="delivery-filter-no-search-preserve-scroll-v8">
/* Hide/remove search from Delivery compact filters */
#deliveryExcelRoot .delivery-mini-filter[data-dx-filter-key="q"]{
  display:none !important;
}
</style>

<script id="delivery-filter-no-search-preserve-scroll-v8">
(function(){
  if(window.__deliveryFilterNoSearchPreserveScrollV8) return;
  window.__deliveryFilterNoSearchPreserveScrollV8 = true;

  function saveScroll(){
    return Array.from(document.querySelectorAll('#deliveryExcelRoot .dx-scroll')).map(function(el){
      return {
        el: el,
        left: el.scrollLeft || 0,
        top: el.scrollTop || 0
      };
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

  function applyKeepScroll(){
    var pos = saveScroll();

    if(typeof window.dxApplyRowFilters === 'function'){
      window.dxApplyRowFilters();
    }

    restoreScroll(pos);
  }

  function removeSearchBox(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    root.querySelectorAll('[data-dx-filter-key="q"]').forEach(function(el){
      el.remove();
    });
  }

  function patchFilterFns(){
    var st = state();

    window.dxDeliveryOrdersFilterSet = function(key, value){
      st[key] = value || 'all';
      applyKeepScroll();

      if(typeof window.dxDeliveryOrdersFilterReset !== 'function'){
        return false;
      }

      return false;
    };

    window.dxDeliveryOrdersFilterStatus = function(v){
      st.status = v || 'all';
      updateVisuals();
      applyKeepScroll();
      return false;
    };

    window.dxDeliveryOrdersFilterSearch = function(){
      st.q = '';
      applyKeepScroll();
      return false;
    };

    window.dxDeliveryOrdersFilterReset = function(){
      st.q = '';
      st.status = 'all';
      st.priority = 'all';
      st.city = 'all';
      st.date = 'all';
      st.rider = 'all';

      var root = document.getElementById('deliveryExcelRoot');
      if(root){
        root.querySelectorAll('select.delivery-mini-filter').forEach(function(sel){
          sel.value = 'all';
        });

        root.querySelectorAll('input[type="date"]').forEach(function(input){
          input.value = '';
        });
      }

      updateVisuals();
      applyKeepScroll();
      return false;
    };
  }

  function updateVisuals(){
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
      var active = st[key] && st[key] !== 'all';
      el.classList.toggle('active', !!active);
    });
  }

  function stopFilterClickScroll(){
    document.addEventListener('click', function(e){
      var filter = e.target && e.target.closest ? e.target.closest('#deliveryExcelRoot .delivery-filter-min-v7') : null;
      if(!filter) return;

      e.stopPropagation();

      var pos = saveScroll();
      setTimeout(function(){
        restoreScroll(pos);
      }, 0);
      setTimeout(function(){
        restoreScroll(pos);
      }, 80);
    }, true);
  }

  function wrapRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__noSearchPreserveScrollV8) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var pos = saveScroll();
      var result = old.apply(this, arguments);

      setTimeout(function(){
        removeSearchBox();
        patchFilterFns();
        updateVisuals();
        restoreScroll(pos);
      }, 0);

      setTimeout(function(){
        removeSearchBox();
        patchFilterFns();
        updateVisuals();
        restoreScroll(pos);
      }, 100);

      return result;
    };

    window.renderDeliveryExcel.__noSearchPreserveScrollV8 = true;
    return true;
  }

  stopFilterClickScroll();

  setTimeout(function(){
    removeSearchBox();
    patchFilterFns();
    updateVisuals();
    wrapRender();
  }, 300);

  setTimeout(function(){
    removeSearchBox();
    patchFilterFns();
    updateVisuals();
    wrapRender();
  }, 1200);
})();
</script>
'''

if "delivery-filter-no-search-preserve-scroll-v8" in html:
    print("Delivery no-search preserve-scroll patch already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Removed search filter and preserved scroll on filter clicks.")
