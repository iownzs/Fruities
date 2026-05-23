from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

changed = 0

old = r'''  document.addEventListener('click', function(e){
    if(e.target.closest('[data-v="delivery"]') || e.target.closest('#view-delivery') || e.target.closest('[onclick*="renderDeliveryExcel"]')){
      setTimeout(runExcel, 100);
      setTimeout(runExcel, 600);
      setTimeout(runExcel, 1500);
    }
  });'''

new = r'''  // Disabled: clicking inside delivery table should not re-render and reset horizontal scroll.
  document.addEventListener('click', function(e){
    if(e.target.closest('[data-v="delivery"]')){
      setTimeout(runExcel, 300);
    }
  });'''

if old in html:
    html = html.replace(old, new, 1)
    changed += 1

patch = r'''
<script id="delivery-scroll-preserve-final-v8">
(function(){
  if(window.__deliveryScrollPreserveFinalV8) return;
  window.__deliveryScrollPreserveFinalV8 = true;

  function saveDxScroll(){
    return Array.from(document.querySelectorAll('.dx-scroll')).map(function(el){
      return { left: el.scrollLeft || 0, top: el.scrollTop || 0 };
    });
  }

  function restoreDxScroll(pos){
    requestAnimationFrame(function(){
      document.querySelectorAll('.dx-scroll').forEach(function(el, i){
        if(pos[i]){
          el.scrollLeft = pos[i].left || 0;
          el.scrollTop = pos[i].top || 0;
        }
      });
    });
  }

  function wrapFinalRenderer(){
    if(typeof window.renderDeliveryExcel !== 'function') return;
    if(window.renderDeliveryExcel.__preserveScrollFinalV8) return;

    var original = window.renderDeliveryExcel;

    window.renderDeliveryExcel = function(){
      var pos = saveDxScroll();
      var result = original.apply(this, arguments);
      restoreDxScroll(pos);
      return result;
    };

    window.renderDeliveryExcel.__preserveScrollFinalV8 = true;
  }

  setTimeout(wrapFinalRenderer, 300);
  setTimeout(wrapFinalRenderer, 1000);
  setTimeout(wrapFinalRenderer, 2500);
  setTimeout(wrapFinalRenderer, 5000);

  document.addEventListener('click', function(e){
    if(e.target.closest && e.target.closest('.dx-scroll')){
      e.stopPropagation();
    }
  }, true);
})();
</script>
'''

if "delivery-scroll-preserve-final-v8" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    changed += 1

p.write_text(html, encoding="utf-8")
print(f"DONE: click scroll fix applied. Changes: {changed}")
