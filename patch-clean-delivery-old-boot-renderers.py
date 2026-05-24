from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

remove_ids = [
    "delivery-excel-force-v2",
    "delivery-excel-boot-v3",
    "delivery-excel-runner-v4",
    "delivery-excel-simple-v5",
]

removed = 0

for sid in remove_ids:
    html, c = re.subn(
        r'\s*<script id="' + re.escape(sid) + r'">.*?</script>\s*',
        '\n',
        html,
        flags=re.S
    )
    removed += c

boot = r'''
<script id="delivery-integrated-boot-v1">
(function(){
  if(window.__deliveryIntegratedBootV1) return;
  window.__deliveryIntegratedBootV1 = true;

  function isDeliveryView(){
    var v = document.getElementById('view-delivery');
    return (
      window.curV === 'delivery' ||
      location.search.indexOf('v=delivery') !== -1 ||
      location.hash.indexOf('delivery') !== -1 ||
      (v && (v.classList.contains('on') || v.offsetParent !== null))
    );
  }

  function bootDelivery(){
    if(!isDeliveryView()) return;

    try{
      if(typeof window.renderDeliveryExcel === 'function'){
        window.renderDeliveryExcel();
      }
    }catch(e){
      console.error('delivery integrated boot failed', e);
    }
  }

  function bootSoon(){
    setTimeout(bootDelivery, 80);
    setTimeout(bootDelivery, 300);
    setTimeout(bootDelivery, 800);
  }

  var oldGo = window.go;
  if(typeof oldGo === 'function' && !oldGo.__deliveryIntegratedBootV1){
    window.go = function(view){
      var result = oldGo.apply(this, arguments);
      if(String(view) === 'delivery') bootSoon();
      return result;
    };
    window.go.__deliveryIntegratedBootV1 = true;
  }

  document.addEventListener('click', function(e){
    if(e.target.closest && e.target.closest('[data-v="delivery"], .mni[data-v="delivery"]')){
      bootSoon();
    }
  });

  window.addEventListener('load', bootSoon);
  document.addEventListener('DOMContentLoaded', bootSoon);
})();
</script>
'''

if "delivery-integrated-boot-v1" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + boot + "\n" + html[insert_at:]

p.write_text(html, encoding="utf-8")
print("DONE: removed old delivery boot/render layers and added clean integrated boot.")
print("Removed blocks:", removed)
