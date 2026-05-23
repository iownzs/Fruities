from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<script id="delivery-excel-boot-v3">
(function(){
  if(window.__deliveryExcelBootV3) return;
  window.__deliveryExcelBootV3 = true;

  function isDeliveryView(){
    return (
      location.search.includes('v=delivery') ||
      location.hash.includes('delivery') ||
      (window.curV === 'delivery') ||
      document.getElementById('view-delivery')?.classList.contains('on') ||
      document.getElementById('view-delivery')?.style.display !== 'none'
    );
  }

  function bootDeliveryExcel(){
    try{
      if(typeof window.renderDeliveryExcel === 'function'){
        window.renderDeliveryExcel();
      }
    }catch(e){
      console.error('Delivery Excel boot failed:', e);
    }
  }

  function bootMany(){
    setTimeout(bootDeliveryExcel, 100);
    setTimeout(bootDeliveryExcel, 400);
    setTimeout(bootDeliveryExcel, 900);
    setTimeout(bootDeliveryExcel, 1600);
    setTimeout(bootDeliveryExcel, 2500);
  }

  window.addEventListener('load', function(){
    if(isDeliveryView()) bootMany();
  });

  document.addEventListener('DOMContentLoaded', function(){
    if(isDeliveryView()) bootMany();
  });

  document.addEventListener('click', function(e){
    if(e.target.closest('[data-v="delivery"]') || e.target.closest('[onclick*="delivery"]')){
      bootMany();
    }
  });

  var oldGo = window.go;
  if(typeof oldGo === 'function'){
    window.go = function(v){
      var result = oldGo.apply(this, arguments);
      if(String(v) === 'delivery') bootMany();
      return result;
    };
  }

  setInterval(function(){
    if(isDeliveryView() && !document.getElementById('deliveryExcelRoot')){
      bootDeliveryExcel();
    }
  }, 1500);
})();
</script>
'''

if "delivery-excel-boot-v3" in html:
    print("Boot patch already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Delivery Excel boot patch added.")
