from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

removed = 0

# Remove older collapse/no-flicker patches that conflict
for sid in [
    "delivery-collapse-history-v1",
    "delivery-collapse-no-flicker-v2"
]:
    html, c1 = re.subn(
        r'\s*<style id="' + re.escape(sid) + r'">.*?</style>\s*',
        '\n',
        html,
        flags=re.S
    )
    html, c2 = re.subn(
        r'\s*<script id="' + re.escape(sid) + r'">.*?</script>\s*',
        '\n',
        html,
        flags=re.S
    )
    removed += c1 + c2

patch = r'''
<style id="delivery-history-toggle-fix-v3">
/* Clean Delivered History collapse */
#deliveryExcelRoot .dx-section.dx-history-collapsed .dx-scroll,
#deliveryExcelRoot .dx-section.dx-history-collapsed .dx-empty{
  display:none !important;
}

#deliveryExcelRoot .dx-section.dx-history-section .dx-section-head{
  cursor:pointer !important;
  user-select:none !important;
}

#deliveryExcelRoot .dx-history-toggle{
  margin-left:auto;
  font-size:11px;
  font-weight:900;
  color:var(--t3,#6b7280);
}
</style>

<script id="delivery-history-toggle-fix-v3">
(function(){
  if(window.__deliveryHistoryToggleFixV3) return;
  window.__deliveryHistoryToggleFixV3 = true;

  window.dxDeliveredHistoryOpen = false;

  function isDeliveredSection(section){
    var head = section && section.querySelector ? section.querySelector('.dx-section-head') : null;
    var txt = head ? (head.textContent || '').toLowerCase() : '';
    return txt.indexOf('delivered history') !== -1 || txt.indexOf('delivered') !== -1;
  }

  function applyHistoryState(){
    var root = document.getElementById('deliveryExcelRoot');
    if(!root) return;

    root.querySelectorAll('.dx-section').forEach(function(section){
      if(!isDeliveredSection(section)) return;

      section.classList.add('dx-history-section');
      section.classList.toggle('dx-history-collapsed', !window.dxDeliveredHistoryOpen);

      var head = section.querySelector('.dx-section-head');
      if(!head) return;

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
    if(window.renderDeliveryExcel.__historyToggleFixV3) return true;

    var old = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var result = old.apply(this, arguments);
      applyHistoryState();
      setTimeout(applyHistoryState, 0);
      setTimeout(applyHistoryState, 100);
      return result;
    };

    window.renderDeliveryExcel.__historyToggleFixV3 = true;
    return true;
  }

  document.addEventListener('click', function(e){
    var head = e.target && e.target.closest ? e.target.closest('#deliveryExcelRoot .dx-section-head') : null;
    if(!head) return;

    var section = head.closest('.dx-section');
    if(!section || !isDeliveredSection(section)) return;

    e.preventDefault();
    e.stopPropagation();

    window.dxDeliveredHistoryOpen = !window.dxDeliveredHistoryOpen;
    applyHistoryState();
  }, true);

  setTimeout(function(){
    wrapRender();
    applyHistoryState();
  }, 200);

  setTimeout(function(){
    wrapRender();
    applyHistoryState();
  }, 800);

  setTimeout(function(){
    wrapRender();
    applyHistoryState();
  }, 1600);
})();
</script>
'''

if "delivery-history-toggle-fix-v3" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]

p.write_text(html, encoding="utf-8")
print("DONE: installed clean Delivered History toggle.")
print("Removed old conflict blocks:", removed)
