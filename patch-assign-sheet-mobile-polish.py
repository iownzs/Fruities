from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="assign-sheet-mobile-polish-v14">
/* Mobile polish for Assign Rider sheet */
.dx-assign-sheet{
  display:flex;
  flex-direction:column;
  max-height:82vh;
  padding:0 !important;
  overflow:hidden !important;
}

.dx-assign-head{
  position:sticky;
  top:0;
  z-index:2;
  background:var(--card,#fff);
  padding:18px 18px 12px;
  margin-bottom:0 !important;
  border-bottom:1px solid #eef2f7;
}

.dx-assign-sheet > .dx-assign-summary,
.dx-assign-sheet > .dx-assign-label,
.dx-assign-sheet > .dx-rider-picks,
.dx-assign-sheet > .dx-assign-input,
.dx-assign-sheet > .dx-assign-notes{
  margin-left:18px;
  margin-right:18px;
}

.dx-assign-summary{
  margin-top:14px;
  background:#fbfdfb !important;
  border-color:#dcefe2 !important;
  line-height:1.5;
}

.dx-assign-summary div{
  display:flex;
  gap:6px;
  align-items:flex-start;
}

.dx-assign-label{
  margin-top:14px !important;
  margin-bottom:7px !important;
}

.dx-rider-picks{
  margin-bottom:8px !important;
  overflow-x:auto;
  flex-wrap:nowrap !important;
  padding-bottom:4px;
  -webkit-overflow-scrolling:touch;
}

.dx-rider-pick{
  flex:0 0 auto;
  min-width:74px;
  position:relative;
}

.dx-rider-pick.on::after{
  content:"✓";
  position:absolute;
  right:-4px;
  top:-5px;
  width:18px;
  height:18px;
  border-radius:999px;
  background:#15803d;
  color:#fff;
  font-size:12px;
  display:flex;
  align-items:center;
  justify-content:center;
}

.dx-assign-input{
  height:48px;
}

.dx-assign-notes{
  min-height:58px !important;
  max-height:90px;
}

.dx-assign-actions{
  position:sticky;
  bottom:0;
  z-index:3;
  background:var(--card,#fff);
  padding:14px 18px 18px;
  margin-top:14px !important;
  border-top:1px solid #eef2f7;
}

.dx-assign-submit{
  background:#15803d !important;
}

.dx-assign-cancel{
  background:#f3f4f6 !important;
}

@media(max-width:700px){
  .dx-assign-backdrop{
    align-items:flex-end !important;
  }

  .dx-assign-sheet{
    max-height:80vh;
    border-radius:24px 24px 0 0 !important;
  }

  .dx-assign-head h3{
    font-size:19px;
  }

  .dx-assign-summary{
    font-size:13px;
  }

  .dx-assign-actions button{
    padding:14px 10px !important;
  }
}
</style>

<script id="assign-sheet-mobile-polish-v14">
(function(){
  if(window.__assignSheetMobilePolishV14) return;
  window.__assignSheetMobilePolishV14 = true;

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
    }) || null;
  }

  function findDelivery(delId, orderId){
    return getDeliveries().find(function(d){
      return (
        String(d.id || '') === String(delId || '') ||
        String(d.orderId || d.oid || d.order || '') === String(orderId || '')
      );
    }) || null;
  }

  function priorityOf(o,d){
    var p = String((o && o.priority) || (d && d.priority) || 'normal').toLowerCase();
    if(p === 'rush') return '🔴 Rush';
    if(p === 'low') return '⚪ Low';
    return '🟢 Normal';
  }

  function enhanceOpenSheet(){
    if(typeof window.dxOpenAssignSheet !== 'function') return false;
    if(window.dxOpenAssignSheet.__mobilePolishV14) return true;

    var oldOpen = window.dxOpenAssignSheet;

    window.dxOpenAssignSheet = function(delId, orderId){
      var result = oldOpen.apply(this, arguments);

      setTimeout(function(){
        var sheet = document.getElementById('dxAssignSheet');
        if(!sheet) return;

        var d = findDelivery(delId, orderId) || {};
        var o = findOrder(orderId || d.orderId || d.oid) || {};

        var sub = sheet.querySelector('.dx-assign-head div div');
        if(sub && !sub.textContent.includes('Rush') && !sub.textContent.includes('Normal') && !sub.textContent.includes('Low')){
          sub.innerHTML = esc((o.id || o.orderNumber || d.orderId || d.oid || d.id || orderId || delId || '-')) +
            ' · ' + esc(priorityOf(o,d)) +
            ' · Waiting for Rider';
        }

        var summary = sheet.querySelector('.dx-assign-summary');
        if(summary && !summary.__iconsAdded){
          summary.innerHTML = summary.innerHTML
            .replace('<b>Customer:</b>', '👤 <b>Customer:</b>')
            .replace('<b>Recipient:</b>', '🎁 <b>Recipient:</b>')
            .replace('<b>City:</b>', '📍 <b>City:</b>')
            .replace('<b>Delivery:</b>', '📅 <b>Delivery:</b>')
            .replace('<b>Address:</b>', '🏠 <b>Address:</b>');
          summary.__iconsAdded = true;
        }
      }, 60);

      return result;
    };

    window.dxOpenAssignSheet.__mobilePolishV14 = true;
    return true;
  }

  setTimeout(enhanceOpenSheet, 300);
  setTimeout(enhanceOpenSheet, 1000);
  setTimeout(enhanceOpenSheet, 2500);
})();
</script>
'''

if "assign-sheet-mobile-polish-v14" in html:
    print("Assign sheet mobile polish already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Assign sheet mobile polish added.")
