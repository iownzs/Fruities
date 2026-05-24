from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

changed = 0

# Add data attributes to each delivery row for faster filtering.
old_vars = r'''    var a = address(o,d);
    var shortAddr = String(a).length > 26 ? String(a).slice(0,26) + '...' : String(a);

    return '<tr>' +'''

new_vars = r'''    var a = address(o,d);
    var shortAddr = String(a).length > 26 ? String(a).slice(0,26) + '...' : String(a);

    var rowCity = String(cityOf(o,d) || 'Other').toLowerCase();
    var rowRider = String(o.rider || o.riderName || d.rider || d.riderName || '').toLowerCase();
    var rowDate = String(o.deliveryDate || o.delivery_date || o.scheduledDate || d.deliveryDate || d.delivery_date || '').slice(0,10);

    return '<tr data-dx-status="'+esc(s)+'" data-dx-priority="'+esc(p)+'" data-dx-city="'+esc(rowCity)+'" data-dx-rider="'+esc(rowRider)+'" data-dx-date="'+esc(rowDate)+'">' +'''

if old_vars in html:
    html = html.replace(old_vars, new_vars, 1)
    changed += 1
else:
    print("Row data attribute target not found or already patched.")

patch = r'''
<script id="delivery-filter-smooth-calendar-v2">
(function(){
  if(window.__deliveryFilterSmoothCalendarV2) return;
  window.__deliveryFilterSmoothCalendarV2 = true;

  var filterTimer = null;

  window.dxFilterState = window.dxFilterState || {
    q:'',
    status:'all',
    priority:'all',
    city:'all',
    date:'all',
    rider:'all'
  };

  function lower(v){
    return String(v == null ? '' : v).toLowerCase();
  }

  function debounceApply(){
    clearTimeout(filterTimer);
    filterTimer = setTimeout(function(){
      if(typeof window.dxApplyRowFilters === 'function'){
        window.dxApplyRowFilters();
      }
    }, 80);
  }

  function normalizeDateValue(v){
    v = String(v || '');
    if(!v || v === 'all') return 'all';
    if(v === 'today' || v === 'tomorrow') return v;
    return v.slice(0,10);
  }

  function todayISO(offset){
    var d = new Date();
    d.setDate(d.getDate() + (offset || 0));
    return d.toISOString().slice(0,10);
  }

  window.dxApplyRowFilters = function(){
    var st = window.dxFilterState || {};
    var totalVisible = 0;

    document.querySelectorAll('.dx-section').forEach(function(section){
      var visible = 0;

      section.querySelectorAll('tbody tr').forEach(function(row){
        var text = lower(row.textContent || '');
        var show = true;

        var status = row.getAttribute('data-dx-status') || '';
        var priority = row.getAttribute('data-dx-priority') || '';
        var city = row.getAttribute('data-dx-city') || '';
        var rider = row.getAttribute('data-dx-rider') || '';
        var date = row.getAttribute('data-dx-date') || '';

        if(st.q && text.indexOf(lower(st.q)) === -1) show = false;
        if(st.status && st.status !== 'all' && status !== st.status) show = false;
        if(st.priority && st.priority !== 'all' && priority !== st.priority) show = false;
        if(st.city && st.city !== 'all' && city !== st.city) show = false;

        if(st.rider === 'assigned' && !rider) show = false;
        if(st.rider === 'unassigned' && rider) show = false;
        if(st.rider && st.rider !== 'all' && st.rider !== 'assigned' && st.rider !== 'unassigned' && rider !== st.rider) show = false;

        if(st.date === 'today' && date !== todayISO(0)) show = false;
        else if(st.date === 'tomorrow' && date !== todayISO(1)) show = false;
        else if(st.date && st.date !== 'all' && st.date !== 'today' && st.date !== 'tomorrow' && date !== st.date) show = false;

        row.style.display = show ? '' : 'none';

        if(show){
          visible++;
          totalVisible++;
        }
      });

      var head = section.querySelector('.dx-section-head span');
      if(head && !head.getAttribute('data-original-title')){
        head.setAttribute('data-original-title', head.textContent.replace(/\s*\(\d+\)\s*$/,''));
      }

      if(head){
        var base = head.getAttribute('data-original-title') || head.textContent;
        base = base.replace(/\s*\(\d+\)\s*$/,'');
        head.textContent = base + ' (' + visible + ')';
      }
    });

    var footer = document.querySelector('#deliveryExcelRoot > .dx-muted:last-child');
    if(footer){
      footer.textContent = 'Showing ' + totalVisible + ' filtered delivery rows';
    }
  };

  function enhanceDateFilter(){
    var row = document.querySelector('#deliveryExcelRoot .dx-filter-row');
    if(!row || row.__calendarEnhancedV2) return;

    var selects = Array.from(row.querySelectorAll('select.dx-select'));
    var dateSelect = selects.find(function(sel){
      return (sel.textContent || '').indexOf('Delivery Date') !== -1;
    });

    if(!dateSelect) return;

    var wrap = document.createElement('div');
    wrap.style.display = 'flex';
    wrap.style.gap = '6px';
    wrap.style.alignItems = 'center';
    wrap.style.flex = '1';

    var dateInput = document.createElement('input');
    dateInput.type = 'date';
    dateInput.className = 'dx-select';
    dateInput.style.minWidth = '150px';
    dateInput.value = (window.dxFilterState.date && !['all','today','tomorrow'].includes(window.dxFilterState.date)) ? window.dxFilterState.date : '';
    dateInput.onchange = function(){
      window.dxFilterState.date = this.value || 'all';
      debounceApply();
    };

    var clearBtn = document.createElement('button');
    clearBtn.type = 'button';
    clearBtn.className = 'dx-chip';
    clearBtn.textContent = 'All Dates';
    clearBtn.onclick = function(){
      window.dxFilterState.date = 'all';
      dateInput.value = '';
      debounceApply();
    };

    wrap.appendChild(dateInput);
    wrap.appendChild(clearBtn);
    dateSelect.replaceWith(wrap);

    row.__calendarEnhancedV2 = true;
  }

  // Smooth filters: do not rebuild the whole table.
  window.dxFilterSearch = function(v){ dxFilterState.q = v; debounceApply(); };
  window.dxFilterSetStatus = function(v){ dxFilterState.status = v; debounceApply(); };
  window.dxFilterPriority = function(v){ dxFilterState.priority = v; debounceApply(); };
  window.dxFilterCity = function(v){ dxFilterState.city = v; debounceApply(); };
  window.dxFilterDate = function(v){ dxFilterState.date = normalizeDateValue(v); debounceApply(); };
  window.dxFilterRider = function(v){ dxFilterState.rider = v; debounceApply(); };
  window.dxFilterRush = function(){
    dxFilterState.priority = dxFilterState.priority === 'rush' ? 'all' : 'rush';
    debounceApply();
  };

  function afterRender(){
    enhanceDateFilter();
    setTimeout(function(){
      if(typeof window.dxApplyRowFilters === 'function') window.dxApplyRowFilters();
    }, 0);
  }

  function wrapRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__smoothCalendarV2) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var result = old.apply(this, arguments);
      afterRender();
      return result;
    };

    window.renderDeliveryExcel.__smoothCalendarV2 = true;
    return true;
  }

  setTimeout(wrapRender, 300);
  setTimeout(wrapRender, 1000);
  setTimeout(wrapRender, 2500);

  setTimeout(afterRender, 600);
})();
</script>
'''

if "delivery-filter-smooth-calendar-v2" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    changed += 1

p.write_text(html, encoding="utf-8")
print(f"DONE: smooth filters + calendar date patch added. Changes: {changed}")
