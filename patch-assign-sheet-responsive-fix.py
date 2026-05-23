from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="assign-sheet-responsive-fix-v15">
/* ===== Assign Rider responsive fix v15 ===== */

/* Default desktop/tablet */
.dx-assign-backdrop{
  align-items:center !important;
  padding:18px !important;
}

.dx-assign-sheet{
  width:min(620px, calc(100vw - 36px)) !important;
  max-height:86vh !important;
  border-radius:24px !important;
  display:flex !important;
  flex-direction:column !important;
  overflow:hidden !important;
  padding:0 !important;
}

.dx-assign-head{
  padding:18px 20px 12px !important;
}

.dx-assign-head h3{
  font-size:22px !important;
  line-height:1.1 !important;
}

.dx-assign-summary{
  margin:14px 20px 8px !important;
  padding:14px !important;
  border-radius:16px !important;
  background:#fbfdfb !important;
  border:1px solid #dcefe2 !important;
  font-size:14px !important;
}

.dx-assign-summary div{
  display:block !important;
  margin:3px 0 !important;
}

.dx-assign-label{
  margin:13px 20px 7px !important;
  font-size:11px !important;
}

.dx-rider-picks{
  margin:0 20px 8px !important;
  display:flex !important;
  gap:8px !important;
  flex-wrap:wrap !important;
}

.dx-rider-pick{
  min-width:78px !important;
  padding:9px 14px !important;
}

.dx-assign-input,
.dx-assign-notes{
  width:calc(100% - 40px) !important;
  margin-left:20px !important;
  margin-right:20px !important;
  box-sizing:border-box !important;
}

.dx-assign-input{
  height:48px !important;
}

.dx-assign-notes{
  min-height:64px !important;
  max-height:95px !important;
}

.dx-assign-actions{
  position:sticky !important;
  bottom:0 !important;
  background:var(--card,#fff) !important;
  padding:14px 20px 18px !important;
  margin-top:14px !important;
  border-top:1px solid #eef2f7 !important;
}

.dx-assign-actions button{
  height:48px !important;
  font-size:14px !important;
}

/* Mobile compact bottom sheet */
@media(max-width:700px){
  .dx-assign-backdrop{
    align-items:flex-end !important;
    padding:0 !important;
  }

  .dx-assign-sheet{
    width:100% !important;
    max-height:88vh !important;
    height:auto !important;
    border-radius:22px 22px 0 0 !important;
  }

  .dx-assign-head{
    padding:14px 16px 9px !important;
  }

  .dx-assign-head h3{
    font-size:18px !important;
  }

  .dx-assign-head > div > div{
    font-size:12px !important;
    white-space:nowrap !important;
    overflow:hidden !important;
    text-overflow:ellipsis !important;
    max-width:calc(100vw - 100px) !important;
  }

  .dx-assign-close{
    width:34px !important;
    height:34px !important;
    flex:0 0 auto !important;
  }

  .dx-assign-summary{
    margin:10px 14px 6px !important;
    padding:11px 12px !important;
    font-size:12px !important;
    line-height:1.35 !important;
  }

  .dx-assign-summary div{
    margin:2px 0 !important;
  }

  .dx-assign-label{
    margin:10px 14px 6px !important;
    font-size:10px !important;
  }

  .dx-rider-picks{
    margin:0 14px 7px !important;
    gap:7px !important;
    flex-wrap:nowrap !important;
    overflow-x:auto !important;
    padding-bottom:5px !important;
    -webkit-overflow-scrolling:touch !important;
  }

  .dx-rider-pick{
    min-width:68px !important;
    padding:8px 12px !important;
    font-size:13px !important;
    flex:0 0 auto !important;
  }

  .dx-assign-input,
  .dx-assign-notes{
    width:calc(100% - 28px) !important;
    margin-left:14px !important;
    margin-right:14px !important;
    font-size:14px !important;
  }

  .dx-assign-input{
    height:44px !important;
  }

  .dx-assign-notes{
    min-height:52px !important;
    max-height:70px !important;
  }

  .dx-assign-actions{
    padding:12px 14px 14px !important;
    gap:8px !important;
  }

  .dx-assign-actions button{
    height:46px !important;
    border-radius:13px !important;
    font-size:13px !important;
  }
}
</style>

<script id="assign-sheet-responsive-fix-v15">
(function(){
  if(window.__assignSheetResponsiveFixV15) return;
  window.__assignSheetResponsiveFixV15 = true;

  function esc(v){
    return String(v == null ? '' : v)
      .replaceAll('&','&amp;')
      .replaceAll('<','&lt;')
      .replaceAll('>','&gt;')
      .replaceAll('"','&quot;')
      .replaceAll("'","&#039;");
  }

  function compactSummary(sheet){
    var summary = sheet && sheet.querySelector('.dx-assign-summary');
    if(!summary || summary.__compactV15) return;

    var rows = Array.from(summary.querySelectorAll('div')).map(function(div){
      return (div.textContent || '').trim();
    });

    var customer = rows.find(function(x){return x.toLowerCase().startsWith('customer:');}) || '';
    var recipient = rows.find(function(x){return x.toLowerCase().startsWith('recipient:');}) || '';
    var city = rows.find(function(x){return x.toLowerCase().startsWith('city:');}) || '';
    var delivery = rows.find(function(x){return x.toLowerCase().startsWith('delivery:');}) || '';
    var address = rows.find(function(x){return x.toLowerCase().startsWith('address:');}) || '';

    summary.innerHTML =
      '<div>👤 <b>' + esc(customer.replace(/^Customer:\s*/i,'')) + '</b></div>' +
      '<div>🎁 <b>' + esc(recipient.replace(/^Recipient:\s*/i,'')) + '</b></div>' +
      '<div>📍 ' + esc(city.replace(/^City:\s*/i,'')) + ' · 📅 ' + esc(delivery.replace(/^Delivery:\s*/i,'')) + '</div>' +
      '<div>🏠 ' + esc(address.replace(/^Address:\s*/i,'')) + '</div>';

    summary.__compactV15 = true;
  }

  function disableMobileAutoFocus(){
    var input = document.getElementById('dxAssignRiderInput');
    if(!input) return;

    if(window.matchMedia && window.matchMedia('(max-width: 700px)').matches){
      try{ input.blur(); }catch(e){}
    }
  }

  function enhanceOpenSheet(){
    if(typeof window.dxOpenAssignSheet !== 'function') return false;
    if(window.dxOpenAssignSheet.__responsiveFixV15) return true;

    var oldOpen = window.dxOpenAssignSheet;

    window.dxOpenAssignSheet = function(){
      var result = oldOpen.apply(this, arguments);

      setTimeout(function(){
        var sheet = document.getElementById('dxAssignSheet');
        if(!sheet) return;

        compactSummary(sheet);
        disableMobileAutoFocus();
      }, 80);

      setTimeout(disableMobileAutoFocus, 180);

      return result;
    };

    window.dxOpenAssignSheet.__responsiveFixV15 = true;
    return true;
  }

  setTimeout(enhanceOpenSheet, 300);
  setTimeout(enhanceOpenSheet, 1000);
  setTimeout(enhanceOpenSheet, 2500);
})();
</script>
'''

if "assign-sheet-responsive-fix-v15" in html:
    print("Responsive assign sheet fix already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: responsive assign sheet fix added.")
