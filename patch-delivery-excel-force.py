from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<script id="delivery-excel-force-v2">
(function(){
  if(window.__deliveryExcelForceV2) return;
  window.__deliveryExcelForceV2 = true;

  function forceDeliveryExcel(){
    try{
      if(typeof window.renderDeliveryExcel === "function"){
        window.renderDeliveryExcel();
      }
    }catch(e){
      console.error("forceDeliveryExcel failed", e);
    }
  }

  var oldGo = window.go;
  if(typeof oldGo === "function" && !oldGo.__deliveryExcelForceV2){
    window.go = function(view){
      var res = oldGo.apply(this, arguments);

      if(String(view) === "delivery"){
        setTimeout(forceDeliveryExcel, 100);
        setTimeout(forceDeliveryExcel, 500);
        setTimeout(forceDeliveryExcel, 1200);
      }

      return res;
    };
    window.go.__deliveryExcelForceV2 = true;
  }

  document.addEventListener("click", function(e){
    var nav = e.target.closest('[data-v="delivery"], .mni[data-v="delivery"]');
    if(nav){
      setTimeout(forceDeliveryExcel, 100);
      setTimeout(forceDeliveryExcel, 500);
      setTimeout(forceDeliveryExcel, 1200);
    }
  });

  document.addEventListener("DOMContentLoaded", function(){
    setTimeout(function(){
      var isDelivery =
        location.hash.includes("delivery") ||
        document.querySelector('[data-v="delivery"].on') ||
        document.querySelector('.mni[data-v="delivery"].on');

      if(isDelivery) forceDeliveryExcel();
    }, 1000);
  });
})();
</script>
'''

if "delivery-excel-force-v2" in html:
    print("Force patch already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Delivery Excel force patch added.")
