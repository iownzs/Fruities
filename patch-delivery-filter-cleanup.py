from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="delivery-filter-cleanup-v4">
/* Clean Delivery filter UI */
#deliveryExcelRoot .dx-date-clear{
  display:none !important;
}

#deliveryExcelRoot .dx-reset-filter{
  border:1px solid #d1d5db;
  background:#fff;
  color:#111827;
  border-radius:14px;
  padding:12px 14px;
  font-weight:900;
  cursor:pointer;
  white-space:nowrap;
}

#deliveryExcelRoot .dx-reset-filter:active{
  transform:scale(.98);
}

@media(max-width:700px){
  #deliveryExcelRoot .dx-reset-filter{
    width:100%;
  }
}
</style>

<script id="delivery-filter-cleanup-v4">
(function(){
  if(window.__deliveryFilterCleanupV4) return;
  window.__deliveryFilterCleanupV4 = true;

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

  function apply(){
    if(typeof window.dxApplyRowFilters === 'function'){
      window.dxApplyRowFilters();
    }
  }

  function cleanupFilterUI(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    // Remove Rush chip because Priority dropdown already handles it
    root.querySelectorAll('.dx-chip').forEach(function(btn){
      var txt = (btn.textContent || '').toLowerCase();
      if(txt.indexOf('rush') !== -1){
        btn.remove();
      }
    });

    // Remove All Dates button
    root.querySelectorAll('button').forEach(function(btn){
      var txt = (btn.textContent || '').toLowerCase();
      if(txt.indexOf('all dates') !== -1){
        btn.remove();
      }
    });

    // Add Reset button once
    var filterRow = root.querySelector('.dx-filter-row');
    if(filterRow && !filterRow.querySelector('.dx-reset-filter')){
      var reset = document.createElement('button');
      reset.type = 'button';
      reset.className = 'dx-reset-filter';
      reset.textContent = 'Reset';
      reset.onclick = function(){
        var st = state();
        st.q = '';
        st.status = 'all';
        st.priority = 'all';
        st.city = 'all';
        st.date = 'all';
        st.rider = 'all';

        var search = root.querySelector('.dx-search');
        if(search) search.value = '';

        root.querySelectorAll('select.dx-select').forEach(function(sel){
          sel.value = 'all';
        });

        root.querySelectorAll('input[type="date"]').forEach(function(input){
          input.value = '';
        });

        root.querySelectorAll('.dx-chip').forEach(function(chip){
          var isAll = (chip.textContent || '').trim().toLowerCase() === 'all';
          chip.classList.toggle('on', isAll);
          if(isAll) chip.setAttribute('data-active','1');
          else chip.removeAttribute('data-active');
        });

        apply();
      };

      filterRow.appendChild(reset);
    }
  }

  function wrapRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__filterCleanupV4) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var result = old.apply(this, arguments);
      setTimeout(cleanupFilterUI, 0);
      setTimeout(cleanupFilterUI, 100);
      return result;
    };

    window.renderDeliveryExcel.__filterCleanupV4 = true;
    return true;
  }

  setTimeout(function(){
    cleanupFilterUI();
    wrapRender();
  }, 300);

  setTimeout(function(){
    cleanupFilterUI();
    wrapRender();
  }, 1200);
})();
</script>
'''

if "delivery-filter-cleanup-v4" in html:
    print("Delivery filter cleanup already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Delivery filter cleanup added.")
