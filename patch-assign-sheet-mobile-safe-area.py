from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="assign-sheet-mobile-safe-area-v17">
/* Fix Assign Rider sheet fighting Android/browser nav bar */
@media(max-width:700px){
  .dx-assign-backdrop{
    align-items:flex-end !important;
    padding:0 !important;
  }

  .dx-assign-sheet{
    max-height:calc(100dvh - 72px) !important;
    height:auto !important;
    overflow-y:auto !important;
    -webkit-overflow-scrolling:touch !important;
    padding-bottom:0 !important;
  }

  .dx-assign-actions{
    position:sticky !important;
    bottom:0 !important;
    padding-bottom:calc(18px + env(safe-area-inset-bottom, 0px)) !important;
    background:var(--card,#fff) !important;
    box-shadow:0 -8px 18px rgba(0,0,0,.06) !important;
  }

  .dx-assign-notes{
    min-height:48px !important;
    max-height:62px !important;
  }

  .dx-assign-summary{
    max-height:150px !important;
    overflow:auto !important;
  }

  body:has(#dxAssignSheet){
    overflow:hidden !important;
  }
}
</style>

<script id="assign-sheet-mobile-safe-area-v17">
(function(){
  if(window.__assignSheetMobileSafeAreaV17) return;
  window.__assignSheetMobileSafeAreaV17 = true;

  function fixSheetHeight(){
    var sheet = document.querySelector('#dxAssignSheet .dx-assign-sheet');
    if(!sheet) return;

    var h = window.innerHeight || document.documentElement.clientHeight || 700;
    var max = Math.max(420, h - 72);
    sheet.style.maxHeight = max + 'px';
  }

  window.addEventListener('resize', fixSheetHeight);
  window.addEventListener('orientationchange', function(){
    setTimeout(fixSheetHeight, 250);
  });

  function enhanceOpenSheet(){
    if(typeof window.dxOpenAssignSheet !== 'function') return false;
    if(window.dxOpenAssignSheet.__safeAreaV17) return true;

    var oldOpen = window.dxOpenAssignSheet;

    window.dxOpenAssignSheet = function(){
      var result = oldOpen.apply(this, arguments);
      setTimeout(fixSheetHeight, 60);
      setTimeout(fixSheetHeight, 250);
      return result;
    };

    window.dxOpenAssignSheet.__safeAreaV17 = true;
    return true;
  }

  setTimeout(enhanceOpenSheet, 300);
  setTimeout(enhanceOpenSheet, 1000);
  setTimeout(enhanceOpenSheet, 2500);
})();
</script>
'''

if "assign-sheet-mobile-safe-area-v17" in html:
    print("Assign sheet safe-area patch already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Assign sheet mobile safe-area patch added.")
