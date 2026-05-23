from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

old_addr = r"""      '<td style="min-width:180px">'+esc(shortAddr)+'<br><span class="dx-muted">'+esc(cityOf(o,d))+'</span></td>' +"""
new_addr = r"""      '<td style="min-width:180px">'+esc(shortAddr)+'<br><span class="dx-muted">'+esc(cityOf(o,d))+'</span><br><button class="dx-link" onclick="event.stopPropagation();dxPreviewAddress(\\''+esc(id)+'\\')">[View]</button></td>' +"""

old_items = r"""      '<td style="min-width:110px">'+itemText(o,d)+'</td>' +"""
new_items = r"""      '<td style="min-width:110px">'+itemText(o,d)+'<br><button class="dx-link" onclick="event.stopPropagation();dxPreviewItems(\\''+esc(id)+'\\')">[View]</button></td>' +"""

changed = 0

if old_addr in html:
    html = html.replace(old_addr, new_addr, 1)
    changed += 1
else:
    print("Address cell pattern not found.")

if old_items in html:
    html = html.replace(old_items, new_items, 1)
    changed += 1
else:
    print("Items cell pattern not found.")

patch = r'''
<script id="delivery-preview-buttons-v9">
(function(){
  if(window.__deliveryPreviewButtonsV9) return;
  window.__deliveryPreviewButtonsV9 = true;

  function esc(v){
    return String(v == null ? '' : v)
      .replaceAll('&','&amp;')
      .replaceAll('<','&lt;')
      .replaceAll('>','&gt;')
      .replaceAll('"','&quot;')
      .replaceAll("'","&#039;");
  }

  function money(v){
    var n = Number(v || 0);
    return '₱' + n.toLocaleString('en-PH',{maximumFractionDigits:2});
  }

  function getOrders(){
    return window.S && Array.isArray(S.orders) ? S.orders : [];
  }

  function getDeliveries(){
    if(window.S && Array.isArray(S.deliveries)) return S.deliveries;
    return [];
  }

  function findDelivery(id){
    return getDeliveries().find(function(d){
      return String(d.id || d.orderId || d.oid) === String(id);
    }) || null;
  }

  function findOrder(id, d){
    var orderId = (d && (d.orderId || d.oid || d.order)) || id;
    return getOrders().find(function(o){
      return String(o.id || o.orderNumber || o.orderId) === String(orderId);
    }) || {};
  }

  function getAddress(o,d){
    return o.deliveryAddress || o.addr || o.address || d.deliveryAddress || d.addr || d.address || '-';
  }

  function getCity(o,d){
    return o.city || d.city || 'Other';
  }

  function getDateTime(o,d){
    var date = o.deliveryDate || o.delivery_date || o.scheduledDate || d.deliveryDate || '';
    var time = o.deliveryTime || o.delivery_time || o.scheduledTime || d.deliveryTime || '';
    return (date || '-') + (time ? ' · ' + time : '');
  }

  function getItems(o,d){
    return Array.isArray(o.items) ? o.items : (Array.isArray(d.items) ? d.items : []);
  }

  function openSheet(title, bodyHtml){
    var old = document.getElementById('dxPreviewSheet');
    if(old) old.remove();

    var div = document.createElement('div');
    div.id = 'dxPreviewSheet';
    div.className = 'dx-modal-backdrop';
    div.innerHTML =
      '<div class="dx-modal">' +
        '<h3>' + esc(title) + '</h3>' +
        '<div style="font-size:14px;line-height:1.55">' + bodyHtml + '</div>' +
        '<button onclick="document.getElementById(\\'dxPreviewSheet\\').remove()">Close</button>' +
      '</div>';

    document.body.appendChild(div);
  }

  window.dxPreviewAddress = function(id){
    var d = findDelivery(id) || {};
    var o = findOrder(id, d);

    openSheet('Address Details',
      '<b>Order:</b><br>' + esc(o.id || o.orderNumber || d.id || id) + '<br><br>' +
      '<b>Full Address:</b><br>' + esc(getAddress(o,d)) + '<br><br>' +
      '<b>City:</b><br>' + esc(getCity(o,d)) + '<br><br>' +
      '<b>Delivery Date / Time:</b><br>' + esc(getDateTime(o,d))
    );
  };

  window.dxPreviewItems = function(id){
    var d = findDelivery(id) || {};
    var o = findOrder(id, d);
    var items = getItems(o,d);

    var itemsHtml = items.length
      ? items.map(function(it){
          var q = it.q || it.qty || it.quantity || 1;
          var name = it.n || it.name || it.productName || 'Item';
          var price = Number(it.p || it.price || 0);
          return '<div style="display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid #eee;padding:8px 0">' +
            '<span>' + esc(q + 'x ' + name) + '</span>' +
            '<b>' + esc(price ? money(price * q) : '') + '</b>' +
          '</div>';
        }).join('')
      : '<span class="dx-muted">No item list found.</span>';

    openSheet('Items / Total',
      '<b>Order:</b><br>' + esc(o.id || o.orderNumber || d.id || id) + '<br><br>' +
      itemsHtml +
      '<div style="display:flex;justify-content:space-between;margin-top:12px;font-size:16px">' +
        '<b>Total</b><b>' + esc(money(o.total || d.total || 0)) + '</b>' +
      '</div>'
    );
  };
})();
</script>
'''

if "delivery-preview-buttons-v9" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    changed += 1

p.write_text(html, encoding="utf-8")
print(f"DONE: preview buttons patch applied. Changes: {changed}")
