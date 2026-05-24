from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="delivery-filter-ui-fix-v3">
/* Fix Delivery filter buttons/layout after smooth filter patch */

#deliveryExcelRoot .dx-top{
  display:grid !important;
  gap:10px !important;
}

#deliveryExcelRoot .dx-chip-row{
  display:flex !important;
  gap:8px !important;
  overflow-x:auto !important;
  flex-wrap:nowrap !important;
  padding-bottom:4px !important;
  -webkit-overflow-scrolling:touch !important;
}

#deliveryExcelRoot .dx-chip{
  flex:0 0 auto !important;
  white-space:nowrap !important;
}

#deliveryExcelRoot .dx-chip.on,
#deliveryExcelRoot .dx-chip[data-active="1"]{
  background:#15803d !important;
  color:#fff !important;
  border-color:#15803d !important;
}

#deliveryExcelRoot .dx-filter-row{
  display:grid !important;
  grid-template-columns:repeat(2,minmax(0,1fr)) !important;
  gap:8px !important;
  align-items:center !important;
}

#deliveryExcelRoot .dx-filter-row > *{
  min-width:0 !important;
}

#deliveryExcelRoot .dx-select{
  width:100% !important;
  min-width:0 !important;
}

.dx-date-wrap{
  display:flex !important;
  gap:8px !important;
  align-items:center !important;
  min-width:0 !important;
}

.dx-date-wrap input[type="date"]{
  flex:1 !important;
  min-width:0 !important;
}

.dx-date-clear{
  flex:0 0 auto !important;
  min-width:88px !important;
}

@media(max-width:700px){
  #deliveryExcelRoot .dx-filter-row{
    grid-template-columns:1fr !important;
  }

  .dx-date-wrap{
    display:grid !important;
    grid-template-columns:1fr 110px !important;
  }

  #deliveryExcelRoot .dx-chip-row{
    margin-left:-2px !important;
    margin-right:-2px !important;
  }
}
</style>

<script id="delivery-filter-ui-fix-v3">
(function(){
  if(window.__deliveryFilterUiFixV3) return;
  window.__deliveryFilterUiFixV3 = true;

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

  function updateChipVisuals(){
    var st = state();
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    root.querySelectorAll('.dx-chip').forEach(function(btn){
      var text = (btn.textContent || '').toLowerCase();
      var active = false;

      if(text === 'all') active = st.status === 'all';
      else if(text.indexOf('active') !== -1) active = st.status === 'out';
      else if(text.indexOf('waiting') !== -1) active = st.status === 'waiting';
      else if(text.indexOf('delivered') !== -1) active = st.status === 'delivered';
      else if(text.indexOf('rush') !== -1) active = st.priority === 'rush';

      btn.classList.toggle('on', active);
      if(active) btn.setAttribute('data-active','1');
      else btn.removeAttribute('data-active');
    });
  }

  function enhanceCalendarLayout(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    var row = root.querySelector('.dx-filter-row');
    if(!row) return;

    var dateInput = row.querySelector('input[type="date"]');
    if(dateInput && !dateInput.closest('.dx-date-wrap')){
      var clearBtn = Array.from(row.querySelectorAll('button')).find(function(b){
        return (b.textContent || '').toLowerCase().includes('all dates');
      });

      var wrap = document.createElement('div');
      wrap.className = 'dx-date-wrap';

      dateInput.parentNode.insertBefore(wrap, dateInput);
      wrap.appendChild(dateInput);

      if(clearBtn){
        clearBtn.classList.add('dx-date-clear');
        wrap.appendChild(clearBtn);
      }
    }
  }

  function applyAndVisual(){
    updateChipVisuals();
    enhanceCalendarLayout();

    if(typeof window.dxApplyRowFilters === 'function'){
      window.dxApplyRowFilters();
    }
  }

  function wrapFilterFn(name, updater){
    var old = window[name];

    window[name] = function(v){
      updater(v);
      applyAndVisual();
      return false;
    };

    window[name].__uiFixV3 = true;
  }

  function install(){
    var st = state();

    wrapFilterFn('dxFilterSearch', function(v){ st.q = v || ''; });
    wrapFilterFn('dxFilterSetStatus', function(v){ st.status = v || 'all'; });
    wrapFilterFn('dxFilterPriority', function(v){ st.priority = v || 'all'; });
    wrapFilterFn('dxFilterCity', function(v){ st.city = v || 'all'; });
    wrapFilterFn('dxFilterDate', function(v){ st.date = v || 'all'; });
    wrapFilterFn('dxFilterRider', function(v){ st.rider = v || 'all'; });
    wrapFilterFn('dxFilterRush', function(){
      st.priority = st.priority === 'rush' ? 'all' : 'rush';
    });

    applyAndVisual();
  }

  function wrapRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__filterUiFixV3) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var result = old.apply(this, arguments);
      setTimeout(applyAndVisual, 0);
      setTimeout(applyAndVisual, 100);
      return result;
    };

    window.renderDeliveryExcel.__filterUiFixV3 = true;
    return true;
  }

  setTimeout(function(){
    install();
    wrapRender();
  }, 400);

  setTimeout(function(){
    install();
    wrapRender();
    applyAndVisual();
  }, 1200);
})();
</script>
'''

if "delivery-filter-ui-fix-v3" in html:
    print("Delivery filter UI fix already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Delivery filter UI fix added.")
