from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

# Replace the simple renderer's riderTimer function so active timers have data-start
old = r'''  function riderTimer(d,o,s){
    var rider = o.rider || o.riderName || d.rider || d.riderName || '';

    if(s === 'waiting'){
      return '<span class="dx-muted">Not assigned<br>-</span>';
    }

    if(s === 'delivered'){
      return esc(rider || '-') + '<br><span class="dx-timer">Delivered</span>';
    }

    return esc(rider || '-') + '<br><span class="dx-timer">Running</span>';
  }'''

new = r'''  function riderTimer(d,o,s){
    var rider = o.rider || o.riderName || d.rider || d.riderName || '';

    if(s === 'waiting'){
      return '<span class="dx-muted">Not assigned<br>-</span>';
    }

    var start =
      Number(o.outForDeliveryAt || o.deliveryOutAt || o.assignedAt || d.outAt || d.startedAt || d.assignedAt || 0);

    var deliveredAt = Number(o.deliveredAt || o.deliveryDeliveredAt || d.deliveredAt || 0);

    if(s === 'delivered'){
      var finalText = 'Delivered';
      if(start && deliveredAt && deliveredAt > start){
        finalText = 'Delivered in ' + dxFormatDuration(deliveredAt - start);
      }
      return esc(rider || '-') + '<br><span class="dx-timer">' + esc(finalText) + '</span>';
    }

    return esc(rider || '-') +
      '<br><span class="dx-timer dx-live-timer" data-start="' + esc(start || Date.now()) + '">Running</span>';
  }'''

if old not in html:
    print("WARNING: riderTimer block not found. Maybe already patched.")
else:
    html = html.replace(old, new, 1)

patch = r'''
<script id="delivery-live-timer-v7">
(function(){
  if(window.__deliveryLiveTimerV7) return;
  window.__deliveryLiveTimerV7 = true;

  window.dxFormatDuration = window.dxFormatDuration || function(ms){
    ms = Math.max(0, Number(ms || 0));
    var totalSeconds = Math.floor(ms / 1000);
    var h = Math.floor(totalSeconds / 3600);
    var m = Math.floor((totalSeconds % 3600) / 60);
    var s = totalSeconds % 60;

    if(h > 0){
      return h + 'h ' + String(m).padStart(2,'0') + 'm';
    }

    return m + 'm ' + String(s).padStart(2,'0') + 's';
  };

  function updateDeliveryLiveTimers(){
    document.querySelectorAll('.dx-live-timer[data-start]').forEach(function(el){
      var start = Number(el.getAttribute('data-start') || 0);
      if(!start) return;

      el.textContent = 'Running ' + window.dxFormatDuration(Date.now() - start);
    });
  }

  setInterval(updateDeliveryLiveTimers, 1000);
  document.addEventListener('DOMContentLoaded', function(){
    setTimeout(updateDeliveryLiveTimers, 500);
  });
})();
</script>
'''

if "delivery-live-timer-v7" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]

p.write_text(html, encoding="utf-8")
print("DONE: Delivery live timer patch added.")
