from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="assign-summary-fix-v16">
.dx-assign-summary{
  display:grid !important;
  gap:7px !important;
}

.dx-as-row{
  display:flex !important;
  align-items:flex-start !important;
  gap:8px !important;
  font-size:13px !important;
  line-height:1.35 !important;
}

.dx-as-ico{
  width:20px;
  flex:0 0 20px;
  text-align:center;
}

.dx-as-text{
  min-width:0;
  flex:1;
}

.dx-as-text b{
  font-weight:900;
}

@media(max-width:700px){
  .dx-assign-summary{
    margin:10px 14px 8px !important;
    padding:12px !important;
  }

  .dx-as-row{
    font-size:12px !important;
  }
}
</style>

<script id="assign-summary-fix-v16">
(function(){
  if(window.__assignSummaryFixV16) return;
  window.__assignSummaryFixV16 = true;

  function esc(v){
    return String(v == null ? '' : v)
      .replaceAll('&','&amp;')
      .replaceAll('<','&lt;')
      .replaceAll('>','&gt;')
      .replaceAll('"','&quot;')
      .replaceAll("'","&#039;");
  }

  function getOrders(){
    return window.S && Array.isArray(S.orders) ? S.orders : [];
  }

  function getDeliveries(){
    return window.S && Array.isArray(S.deliveries) ? S.deliveries : [];
  }

  function findOrder(id){
    return getOrders().find(function(o){
      return String(o.id || o.orderNumber || o.orderId) === String(id);
    }) || {};
  }

  function findDelivery(delId, orderId){
    return getDeliveries().find(function(d){
      return (
        String(d.id || '') === String(delId || '') ||
        String(d.orderId || d.oid || d.order || '') === String(orderId || '')
      );
    }) || {};
  }

  function val(){
    for(var i=0;i<arguments.length;i++){
      if(arguments[i] !== undefined && arguments[i] !== null && String(arguments[i]).trim() !== ''){
        return arguments[i];
      }
    }
    return '-';
  }

  function customer(o,d){ return val(o.cust, o.customerName, o.name, d.cust, d.customerName); }
  function customerPhone(o,d){ return val(o.phone, o.customerPhone, o.customerNumber, d.phone, d.customerPhone); }
  function recipient(o,d){ return val(o.recipient, o.recipientName, d.recipient, d.recipientName, customer(o,d)); }
  function recipientPhone(o,d){ return val(o.recipientPhone, o.recipientNumber, d.recipientPhone, d.recipientNumber, customerPhone(o,d)); }
  function city(o,d){ return val(o.city, d.city, 'Other'); }
  function address(o,d){ return val(o.deliveryAddress, o.addr, o.address, d.deliveryAddress, d.addr, d.address); }

  function delivery(o,d){
    var date = val(o.deliveryDate, o.delivery_date, o.scheduledDate, d.deliveryDate, '');
    var time = val(o.deliveryTime, o.delivery_time, o.scheduledTime, d.deliveryTime, '');
    if(date === '-' && time === '-') return '-';
    if(time === '-') return date;
    if(date === '-') return time;
    return date + ' · ' + time;
  }

  function row(icon,label,value){
    return '<div class="dx-as-row"><span class="dx-as-ico">'+icon+'</span><span class="dx-as-text"><b>'+esc(label)+':</b> '+esc(value)+'</span></div>';
  }

  function rebuildSummary(sheet, delId, orderId){
    var summary = sheet && sheet.querySelector('.dx-assign-summary');
    if(!summary) return;

    var d = findDelivery(delId, orderId);
    var o = findOrder(orderId || d.orderId || d.oid);

    summary.innerHTML =
      row('👤','Customer', customer(o,d) + ' · ' + customerPhone(o,d)) +
      row('🎁','Recipient', recipient(o,d) + ' · ' + recipientPhone(o,d)) +
      row('📍','City', city(o,d)) +
      row('📅','Delivery', delivery(o,d)) +
      row('🏠','Address', address(o,d));
  }

  function enhance(){
    if(typeof window.dxOpenAssignSheet !== 'function') return false;
    if(window.dxOpenAssignSheet.__summaryFixV16) return true;

    var oldOpen = window.dxOpenAssignSheet;

    window.dxOpenAssignSheet = function(delId, orderId){
      var result = oldOpen.apply(this, arguments);

      setTimeout(function(){
        var sheet = document.getElementById('dxAssignSheet');
        if(sheet) rebuildSummary(sheet, delId, orderId);
      }, 100);

      setTimeout(function(){
        var sheet = document.getElementById('dxAssignSheet');
        if(sheet) rebuildSummary(sheet, delId, orderId);
      }, 300);

      return result;
    };

    window.dxOpenAssignSheet.__summaryFixV16 = true;
    return true;
  }

  setTimeout(enhance,300);
  setTimeout(enhance,1000);
  setTimeout(enhance,2500);
})();
</script>
'''

if "assign-summary-fix-v16" in html:
    print("Assign summary fix already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Assign summary fix added.")
