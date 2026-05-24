from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

removed = 0

# Remove the bad patch that blocks filter clicks
for sid in [
    "delivery-filter-no-search-preserve-scroll-v8",
    "delivery-filter-hide-until-ready-v6"
]:
    html, c1 = re.subn(r'\s*<style id="'+re.escape(sid)+r'">.*?</style>\s*', '\n', html, flags=re.S)
    html, c2 = re.subn(r'\s*<script id="'+re.escape(sid)+r'">.*?</script>\s*', '\n', html, flags=re.S)
    removed += c1 + c2

patch = r'''
<style id="delivery-compact-filter-click-fix-v9">
/* Hide old filter UI until Orders-style compact filter replaces it */
#deliveryExcelRoot .dx-top:not(.delivery-order-filter-card){
  opacity:0 !important;
  height:0 !important;
  overflow:hidden !important;
  margin:0 !important;
  padding:0 !important;
}

/* Remove search from compact filter */
#deliveryExcelRoot .delivery-mini-filter[data-dx-filter-key="q"]{
  display:none !important;
}

/* Make compact controls easier to tap */
#deliveryExcelRoot .delivery-filter-min-v7{
  pointer-events:auto !important;
}

#deliveryExcelRoot .delivery-mini-filter,
#deliveryExcelRoot .delivery-reset-btn-v7{
  pointer-events:auto !important;
  cursor:pointer !important;
}
</style>

<script id="delivery-compact-filter-click-fix-v9">
(function(){
  if(window.__deliveryCompactFilterClickFixV9) return;
  window.__deliveryCompactFilterClickFixV9 = true;

  function saveScroll(){
    return Array.from(document.querySelectorAll('#deliveryExcelRoot .dx-scroll')).map(function(el){
      return { el: el, left: el.scrollLeft || 0, top: el.scrollTop || 0 };
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

  function removeSearch(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    root.querySelectorAll('[data-dx-filter-key="q"]').forEach(function(el){
      el.remove();
    });
  }

  function wrapFn(name){
    var fn = window[name];
    if(typeof fn !== 'function') return false;
    if(fn.__compactClickFixV9) return true;

    window[name] = function(){
      var pos = saveScroll();
      var result = fn.apply(this, arguments);
      removeSearch();
      restoreScroll(pos);
      setTimeout(function(){ restoreScroll(pos); }, 60);
      return result;
    };

    window[name].__compactClickFixV9 = true;
    return true;
  }

  function wrapRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__compactClickFixV9) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var pos = saveScroll();
      var result = old.apply(this, arguments);

      setTimeout(function(){
        removeSearch();
        restoreScroll(pos);
      }, 0);

      setTimeout(function(){
        removeSearch();
        restoreScroll(pos);
      }, 100);

      return result;
    };

    window.renderDeliveryExcel.__compactClickFixV9 = true;
    return true;
  }

  function install(){
    removeSearch();
    wrapFn('dxDeliveryOrdersFilterSet');
    wrapFn('dxDeliveryOrdersFilterStatus');
    wrapFn('dxDeliveryOrdersFilterReset');
    wrapRender();
  }

  // Important: no stopPropagation here, so select/date/buttons remain clickable.
  setTimeout(install, 200);
  setTimeout(install, 700);
  setTimeout(install, 1500);
})();
</script>
'''

if "delivery-compact-filter-click-fix-v9" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]

p.write_text(html, encoding="utf-8")
print("DONE: removed bad filter click blocker and installed safe fix.")
print("Removed blocks:", removed)
