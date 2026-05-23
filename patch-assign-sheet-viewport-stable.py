from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

changed = 0

# Disable old auto-focus that can trigger mobile keyboard/nav bar jump
old_focus = """    setTimeout(function(){
      var input = document.getElementById('dxAssignRiderInput');
      if(input) input.focus();
    },100);"""

new_focus = """    // Mobile fix: do not auto-focus input on open.
    // User taps Rider Name manually, preventing browser nav/keyboard jump.
    setTimeout(function(){
      var input = document.getElementById('dxAssignRiderInput');
      if(input && !(window.matchMedia && window.matchMedia('(max-width: 700px)').matches)) input.focus();
    },100);"""

if old_focus in html:
    html = html.replace(old_focus, new_focus, 1)
    changed += 1
else:
    print("Auto-focus block not found or already patched.")

patch = r'''
<style id="assign-sheet-viewport-stable-v18">
@media(max-width:700px){
  .dx-assign-backdrop{
    position:fixed !important;
    inset:0 !important;
    height:var(--dx-vvh, 100dvh) !important;
    max-height:var(--dx-vvh, 100dvh) !important;
    align-items:flex-end !important;
    overflow:hidden !important;
  }

  .dx-assign-sheet{
    max-height:calc(var(--dx-vvh, 100dvh) - 42px) !important;
    height:auto !important;
    overflow-y:auto !important;
    overscroll-behavior:contain !important;
    transform:translateZ(0);
  }

  .dx-assign-actions{
    padding-bottom:calc(22px + env(safe-area-inset-bottom, 0px)) !important;
  }
}
</style>

<script id="assign-sheet-viewport-stable-v18">
(function(){
  if(window.__assignSheetViewportStableV18) return;
  window.__assignSheetViewportStableV18 = true;

  function setViewportHeight(){
    var h = window.innerHeight || document.documentElement.clientHeight || 700;

    if(window.visualViewport && window.visualViewport.height){
      h = Math.floor(window.visualViewport.height);
    }

    document.documentElement.style.setProperty('--dx-vvh', h + 'px');

    var sheet = document.querySelector('#dxAssignSheet .dx-assign-sheet');
    if(sheet && window.matchMedia && window.matchMedia('(max-width: 700px)').matches){
      sheet.style.maxHeight = Math.max(420, h - 42) + 'px';
    }
  }

  function stabilizeSheet(){
    setViewportHeight();

    // Mobile browser bars often settle after first paint.
    setTimeout(setViewportHeight, 60);
    setTimeout(setViewportHeight, 180);
    setTimeout(setViewportHeight, 420);
    setTimeout(setViewportHeight, 800);

    var input = document.getElementById('dxAssignRiderInput');
    if(input && window.matchMedia && window.matchMedia('(max-width: 700px)').matches){
      try{ input.blur(); }catch(e){}
    }
  }

  window.addEventListener('resize', setViewportHeight);
  window.addEventListener('orientationchange', function(){
    setTimeout(setViewportHeight, 250);
  });

  if(window.visualViewport){
    window.visualViewport.addEventListener('resize', setViewportHeight);
    window.visualViewport.addEventListener('scroll', setViewportHeight);
  }

  function enhanceOpenSheet(){
    if(typeof window.dxOpenAssignSheet !== 'function') return false;
    if(window.dxOpenAssignSheet.__viewportStableV18) return true;

    var oldOpen = window.dxOpenAssignSheet;

    window.dxOpenAssignSheet = function(){
      var result = oldOpen.apply(this, arguments);
      stabilizeSheet();
      return result;
    };

    window.dxOpenAssignSheet.__viewportStableV18 = true;
    return true;
  }

  setViewportHeight();
  setTimeout(enhanceOpenSheet,300);
  setTimeout(enhanceOpenSheet,1000);
  setTimeout(enhanceOpenSheet,2500);
})();
</script>
'''

if "assign-sheet-viewport-stable-v18" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    changed += 1

p.write_text(html, encoding="utf-8")
print(f"DONE: viewport stable patch applied. Changes: {changed}")
