from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="delivery-filter-chips-v1">
/* Make delivery filters faster by using chips instead of dropdowns */
#deliveryFastFilters .delivery-chip-label{
  flex:0 0 auto;
  height:34px;
  display:inline-flex;
  align-items:center;
  padding:0 2px;
  font-size:11px;
  font-weight:900;
  color:var(--t3,#6b7280);
  white-space:nowrap;
}

#deliveryFastFilters .delivery-fast-filter[data-priority],
#deliveryFastFilters .delivery-fast-filter[data-rider]{
  min-width:auto;
}
</style>

<script id="delivery-filter-chips-v1">
(function(){
  if(window.__deliveryFilterChipsV1) return;
  window.__deliveryFilterChipsV1 = true;

  function waitForFastFilters(){
    return document.getElementById('deliveryFastFilters');
  }

  function patchBuildFilters(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__filterChipsV1) return true;

    var oldRender = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var result = oldRender.apply(this, arguments);
      setTimeout(convertFiltersToChips, 0);
      setTimeout(convertFiltersToChips, 120);
      return result;
    };

    window.renderDeliveryExcel.__filterChipsV1 = true;
    return true;
  }

  function getStateFromUI(){
    var root = waitForFastFilters();
    var state = {
      priority:'all',
      rider:'all'
    };

    if(!root) return state;

    var p = root.querySelector('[data-priority].on');
    var r = root.querySelector('[data-rider].on');

    if(p) state.priority = p.getAttribute('data-priority') || 'all';
    if(r) state.rider = r.getAttribute('data-rider') || 'all';

    return state;
  }

  function dispatchChange(el){
    if(!el) return;
    el.dispatchEvent(new Event('change', { bubbles:true }));
  }

  function convertFiltersToChips(){
    var root = waitForFastFilters();
    if(!root || root.__chipsConvertedV1) return;

    var row = root.querySelector('.delivery-fast-row');
    if(!row) return;

    var prioritySelect = row.querySelector('select[data-key="priority"]');
    var riderSelect = row.querySelector('select[data-key="rider"]');

    if(!prioritySelect || !riderSelect) return;

    var currentPriority = prioritySelect.value || 'all';
    var currentRider = riderSelect.value || 'all';

    var hiddenPriority = prioritySelect.cloneNode(true);
    hiddenPriority.style.display = 'none';
    hiddenPriority.setAttribute('data-hidden-priority-select','1');

    var hiddenRider = riderSelect.cloneNode(true);
    hiddenRider.style.display = 'none';
    hiddenRider.setAttribute('data-hidden-rider-select','1');

    function chip(label, key, value, current){
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'delivery-fast-filter' + (String(value) === String(current) ? ' on active' : '');
      b.textContent = label;
      b.setAttribute(key, value);
      return b;
    }

    var frag = document.createDocumentFragment();

    var pLabel = document.createElement('span');
    pLabel.className = 'delivery-chip-label';
    pLabel.textContent = 'Priority:';
    frag.appendChild(pLabel);

    [
      ['All','all'],
      ['Rush','rush'],
      ['Normal','normal'],
      ['Low','low']
    ].forEach(function(x){
      frag.appendChild(chip(x[0], 'data-priority', x[1], currentPriority));
    });

    var rLabel = document.createElement('span');
    rLabel.className = 'delivery-chip-label';
    rLabel.textContent = 'Rider:';
    frag.appendChild(rLabel);

    [
      ['All','all'],
      ['Assigned','assigned'],
      ['Not assigned','unassigned']
    ].forEach(function(x){
      frag.appendChild(chip(x[0], 'data-rider', x[1], currentRider));
    });

    prioritySelect.replaceWith(hiddenPriority);
    riderSelect.replaceWith(hiddenRider);

    var dateInput = row.querySelector('input[type="date"]');
    if(dateInput){
      row.insertBefore(frag, dateInput);
    }else{
      row.appendChild(frag);
    }

    row.addEventListener('click', function(e){
      var pBtn = e.target.closest('[data-priority]');
      var rBtn = e.target.closest('[data-rider]');

      if(pBtn){
        row.querySelectorAll('[data-priority]').forEach(function(b){
          b.classList.remove('on','active');
        });
        pBtn.classList.add('on','active');

        hiddenPriority.value = pBtn.getAttribute('data-priority') || 'all';
        dispatchChange(hiddenPriority);
      }

      if(rBtn){
        row.querySelectorAll('[data-rider]').forEach(function(b){
          b.classList.remove('on','active');
        });
        rBtn.classList.add('on','active');

        hiddenRider.value = rBtn.getAttribute('data-rider') || 'all';
        dispatchChange(hiddenRider);
      }
    });

    root.__chipsConvertedV1 = true;
  }

  function boot(){
    patchBuildFilters();
    convertFiltersToChips();
  }

  setTimeout(boot, 300);
  setTimeout(boot, 1000);
  setTimeout(boot, 2000);
})();
</script>
'''

if "delivery-filter-chips-v1" in html:
    print("Delivery filter chips already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Delivery priority/rider chips added.")
