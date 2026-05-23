from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<script id="delivery-excel-runner-v4">
(function(){
  if(window.__deliveryExcelRunnerV4) return;
  window.__deliveryExcelRunnerV4 = true;

  function onDeliveryPage(){
    var v = document.getElementById('view-delivery');
    if(!v) return false;

    return (
      location.search.indexOf('v=delivery') !== -1 ||
      window.curV === 'delivery' ||
      v.classList.contains('on') ||
      v.offsetParent !== null
    );
  }

  function runExcel(){
    try{
      if(onDeliveryPage() && typeof window.renderDeliveryExcel === 'function'){
        window.renderDeliveryExcel();
      }
    }catch(e){
      console.error('delivery excel runner error', e);
      var root = document.getElementById('deliveryExcelRoot');
      if(root){
        root.innerHTML = '<div class="dx-empty">Delivery Excel failed to load. Check console.</div>';
      }
    }
  }

  window.addEventListener('load', function(){
    setTimeout(runExcel, 300);
    setTimeout(runExcel, 1000);
    setTimeout(runExcel, 2500);
    setTimeout(runExcel, 5000);
  });

  document.addEventListener('DOMContentLoaded', function(){
    setTimeout(runExcel, 300);
    setTimeout(runExcel, 1000);
    setTimeout(runExcel, 2500);
  });

  document.addEventListener('click', function(e){
    if(e.target.closest('[data-v="delivery"]') || e.target.closest('#view-delivery') || e.target.closest('[onclick*="renderDeliveryExcel"]')){
      setTimeout(runExcel, 100);
      setTimeout(runExcel, 600);
      setTimeout(runExcel, 1500);
    }
  });

  setInterval(runExcel, 3000);
})();
</script>
'''

if "delivery-excel-runner-v4" in html:
    print("Runner patch already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Delivery Excel runner patch added.")
