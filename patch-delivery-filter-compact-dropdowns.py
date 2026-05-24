from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

removed = 0

# Remove chips experiment if installed
for sid in ["delivery-filter-chips-v1"]:
    html, c1 = re.subn(r'\s*<style id="'+re.escape(sid)+r'">.*?</style>\s*', '\n', html, flags=re.S)
    html, c2 = re.subn(r'\s*<script id="'+re.escape(sid)+r'">.*?</script>\s*', '\n', html, flags=re.S)
    removed += c1 + c2

patch = r'''
<style id="delivery-filter-compact-dropdowns-v1">
/* Compact delivery filter layout: status buttons + dropdown filters */
#deliveryFastFilters{
  padding:10px 12px !important;
  margin:0 0 12px !important;
  background:var(--w,#fff) !important;
  border:1px solid var(--b,#e5e7eb) !important;
  border-radius:18px !important;
}

#deliveryFastFilters .delivery-fast-row{
  display:flex !important;
  flex-wrap:nowrap !important;
  gap:7px !important;
  overflow-x:auto !important;
  -webkit-overflow-scrolling:touch !important;
  scrollbar-width:none !important;
  padding-bottom:2px !important;
}

#deliveryFastFilters .delivery-fast-row::-webkit-scrollbar{
  display:none !important;
}

#deliveryFastFilters .delivery-fast-filter{
  flex:0 0 auto !important;
  height:34px !important;
  min-width:86px !important;
  max-width:155px !important;
  padding:7px 10px !important;
  border-radius:999px !important;
  font-size:12px !important;
  font-weight:800 !important;
  white-space:nowrap !important;
}

#deliveryFastFilters select.delivery-fast-filter{
  min-width:118px !important;
}

#deliveryFastFilters input[type="date"].delivery-fast-filter{
  min-width:142px !important;
}

#deliveryFastFilters [data-reset]{
  min-width:78px !important;
}

#deliveryFastFilters .delivery-fast-filter.on,
#deliveryFastFilters .delivery-fast-filter.active{
  border-color:var(--green,#15803d) !important;
  background:var(--gl,#e9f7ef) !important;
  color:var(--gd,#166534) !important;
}

@media(max-width:768px){
  #deliveryFastFilters{
    margin-left:-2px !important;
    margin-right:-2px !important;
  }

  #deliveryFastFilters .delivery-fast-filter{
    min-width:82px !important;
  }

  #deliveryFastFilters select.delivery-fast-filter{
    min-width:112px !important;
  }

  #deliveryFastFilters input[type="date"].delivery-fast-filter{
    min-width:135px !important;
  }
}
</style>

<script id="delivery-filter-compact-dropdowns-v1">
(function(){
  if(window.__deliveryFilterCompactDropdownsV1) return;
  window.__deliveryFilterCompactDropdownsV1 = true;

  function cleanupChipArtifacts(){
    var root = document.getElementById('deliveryFastFilters');
    if(!root) return;

    root.querySelectorAll('.delivery-chip-label,[data-priority],[data-rider]').forEach(function(el){
      // Only remove chip experiment buttons/labels, not normal selects.
      if(el.tagName !== 'SELECT'){
        el.remove();
      }
    });

    root.querySelectorAll('[data-hidden-priority-select],[data-hidden-rider-select]').forEach(function(sel){
      sel.style.display = '';
      sel.classList.add('delivery-fast-filter');
    });
  }

  function relabelDropdowns(){
    var root = document.getElementById('deliveryFastFilters');
    if(!root) return;

    var p = root.querySelector('select[data-key="priority"]');
    if(p && p.options.length){
      p.options[0].textContent = 'Priority';
    }

    var r = root.querySelector('select[data-key="rider"]');
    if(r && r.options.length){
      r.options[0].textContent = 'Rider';
    }
  }

  function wrapRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__compactDropdownsV1) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var result = old.apply(this, arguments);
      setTimeout(function(){
        cleanupChipArtifacts();
        relabelDropdowns();
      }, 0);
      setTimeout(function(){
        cleanupChipArtifacts();
        relabelDropdowns();
      }, 100);
      return result;
    };

    window.renderDeliveryExcel.__compactDropdownsV1 = true;
    return true;
  }

  setTimeout(function(){
    cleanupChipArtifacts();
    relabelDropdowns();
    wrapRender();
  }, 300);

  setTimeout(function(){
    cleanupChipArtifacts();
    relabelDropdowns();
    wrapRender();
  }, 1200);
})();
</script>
'''

if "delivery-filter-compact-dropdowns-v1" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]

p.write_text(html, encoding="utf-8")
print("DONE: compact dropdown filter layout added.")
print("Removed chip blocks:", removed)
