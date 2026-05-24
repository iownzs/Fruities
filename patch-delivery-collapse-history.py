from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="delivery-collapse-history-v1">
/* Collapse Delivered History by default */
#deliveryExcelRoot .dx-section.dx-delivered-collapsed .dx-scroll,
#deliveryExcelRoot .dx-section.dx-delivered-collapsed .dx-empty{
  display:none !important;
}

#deliveryExcelRoot .dx-section-head{
  cursor:pointer;
}

#deliveryExcelRoot .dx-history-toggle{
  font-size:11px;
  font-weight:900;
  opacity:.8;
  margin-left:auto;
}
</style>

<script id="delivery-collapse-history-v1">
(function(){
  if(window.__deliveryCollapseHistoryV1) return;
  window.__deliveryCollapseHistoryV1 = true;

  window.dxDeliveredHistoryOpen = window.dxDeliveredHistoryOpen || false;

  function applyDeliveredCollapse(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    root.querySelectorAll('.dx-section').forEach(function(section){
      var head = section.querySelector('.dx-section-head');
      if(!head) return;

      var title = (head.textContent || '').toLowerCase();
      var isDelivered = title.indexOf('delivered') !== -1;

      if(!isDelivered) return;

      section.classList.toggle('dx-delivered-collapsed', !window.dxDeliveredHistoryOpen);

      if(!head.__deliveryToggleInstalled){
        head.__deliveryToggleInstalled = true;

        head.addEventListener('click', function(e){
          e.preventDefault();
          window.dxDeliveredHistoryOpen = !window.dxDeliveredHistoryOpen;
          applyDeliveredCollapse();
        });
      }

      var toggle = head.querySelector('.dx-history-toggle');
      if(!toggle){
        toggle = document.createElement('span');
        toggle.className = 'dx-history-toggle';
        head.appendChild(toggle);
      }

      toggle.textContent = window.dxDeliveredHistoryOpen ? 'Tap to hide' : 'Tap to show';
    });
  }

  function wrapRender(){
    if(typeof window.renderDeliveryExcel !== 'function') return false;
    if(window.renderDeliveryExcel.__collapseHistoryV1) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var result = old.apply(this, arguments);
      setTimeout(applyDeliveredCollapse, 0);
      setTimeout(applyDeliveredCollapse, 120);
      return result;
    };

    window.renderDeliveryExcel.__collapseHistoryV1 = true;
    return true;
  }

  setTimeout(function(){
    wrapRender();
    applyDeliveredCollapse();
  }, 300);

  setTimeout(function(){
    wrapRender();
    applyDeliveredCollapse();
  }, 1200);
})();
</script>
'''

if "delivery-collapse-history-v1" in html:
    print("Delivered history collapse already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Delivered History collapse added.")
