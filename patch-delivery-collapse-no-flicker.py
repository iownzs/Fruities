from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="delivery-collapse-no-flicker-v2">
/* Prevent Delivered History flicker on first Delivery tab load */
#deliveryExcelRoot .dx-section:has(.dx-section-head){
  transition:none !important;
}

/* JS will add this class immediately after render */
#deliveryExcelRoot .dx-section.dx-delivered-hidden-first .dx-scroll,
#deliveryExcelRoot .dx-section.dx-delivered-hidden-first .dx-empty{
  display:none !important;
}
</style>

<script id="delivery-collapse-no-flicker-v2">
(function(){
  if(window.__deliveryCollapseNoFlickerV2) return;
  window.__deliveryCollapseNoFlickerV2 = true;

  function hideDeliveredFast(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    root.querySelectorAll('.dx-section').forEach(function(section){
      var head = section.querySelector('.dx-section-head');
      if(!head) return;

      var text = (head.textContent || '').toLowerCase();
      if(text.indexOf('delivered') !== -1 && !window.dxDeliveredHistoryOpen){
        section.classList.add('dx-delivered-hidden-first');
        section.classList.add('dx-delivered-collapsed');
      }
    });
  }

  function syncWithCollapsePatch(){
    hideDeliveredFast();

    setTimeout(function(){
      document.querySelectorAll('#deliveryExcelRoot .dx-section.dx-delivered-hidden-first').forEach(function(section){
        if(window.dxDeliveredHistoryOpen){
          section.classList.remove('dx-delivered-hidden-first');
        }
      });
    }, 80);
  }

  function wrapRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__collapseNoFlickerV2) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var result = old.apply(this, arguments);

      hideDeliveredFast();
      setTimeout(syncWithCollapsePatch, 0);
      setTimeout(syncWithCollapsePatch, 60);
      setTimeout(syncWithCollapsePatch, 160);

      return result;
    };

    window.renderDeliveryExcel.__collapseNoFlickerV2 = true;
    return true;
  }

  setTimeout(function(){
    wrapRender();
    hideDeliveredFast();
  }, 100);

  setTimeout(function(){
    wrapRender();
    hideDeliveredFast();
  }, 500);

  setTimeout(function(){
    wrapRender();
    hideDeliveredFast();
  }, 1200);
})();
</script>
'''

if "delivery-collapse-no-flicker-v2" in html:
    print("No-flicker collapse patch already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Delivered History no-flicker patch added.")
