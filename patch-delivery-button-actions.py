from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

changed = 0

old_action = r'''  function action(d,o,s){
    var id = esc(d.id || d.orderId || o.id || o.orderNumber || '');
    if(s === 'out'){
      return '<button class="dx-action" onclick="dxSimpleDone(\''+id+'\')">Done</button>';
    }
    if(s === 'delivered'){
      return '<button class="dx-action view">View</button>';
    }
    return '<button class="dx-action assign" onclick="quickAssignRider(\''+id+'\')">Assign</button>';
  }'''

new_action = r'''  function action(d,o,s){
    var delId = esc(d.id || '');
    var orderId = esc(o.id || o.orderNumber || d.orderId || d.oid || d.order || d.id || '');

    if(s === 'out'){
      return '<button type="button" class="dx-action" data-dx-action="done" data-del-id="'+delId+'" data-order-id="'+orderId+'">Done</button>';
    }

    if(s === 'delivered'){
      return '<button type="button" class="dx-action view" data-dx-action="view" data-del-id="'+delId+'" data-order-id="'+orderId+'">View</button>';
    }

    return '<button type="button" class="dx-action assign" data-dx-action="assign" data-del-id="'+delId+'" data-order-id="'+orderId+'">Assign</button>';
  }'''

if old_action in html:
    html = html.replace(old_action, new_action, 1)
    changed += 1
else:
    print("action() block not found or already changed.")

# Replace preview buttons with data-action buttons too
old_addr = """<button class="dx-link" onclick="event.stopPropagation();dxPreviewAddress(\\''+esc(id)+'\\')">[View]</button>"""
new_addr = """<button type="button" class="dx-link" data-dx-action="address" data-del-id="'+esc(d.id || '')+'" data-order-id="'+esc(o.id || o.orderNumber || d.orderId || d.oid || d.order || d.id || '')+'">[View]</button>"""

old_items = """<button class="dx-link" onclick="event.stopPropagation();dxPreviewItems(\\''+esc(id)+'\\')">[View]</button>"""
new_items = """<button type="button" class="dx-link" data-dx-action="items" data-del-id="'+esc(d.id || '')+'" data-order-id="'+esc(o.id || o.orderNumber || d.orderId || d.oid || d.order || d.id || '')+'">[View]</button>"""

if old_addr in html:
    html = html.replace(old_addr, new_addr, 1)
    changed += 1
else:
    print("Address inline preview button not found or already changed.")

if old_items in html:
    html = html.replace(old_items, new_items, 1)
    changed += 1
else:
    print("Items inline preview button not found or already changed.")

patch = r'''
<script id="delivery-button-actions-v10">
(function(){
  if(window.__deliveryButtonActionsV10) return;
  window.__deliveryButtonActionsV10 = true;

  function getBtn(e){
    return e.target && e.target.closest ? e.target.closest('[data-dx-action]') : null;
  }

  document.addEventListener('click', function(e){
    var btn = getBtn(e);
    if(!btn) return;

    e.preventDefault();
    e.stopPropagation();

    var action = btn.getAttribute('data-dx-action');
    var delId = btn.getAttribute('data-del-id') || '';
    var orderId = btn.getAttribute('data-order-id') || '';
    var id = delId || orderId;

    try{
      if(action === 'assign'){
        if(typeof quickAssignRider === 'function'){
          quickAssignRider(delId || id);
        }else{
          alert('quickAssignRider() not found.');
        }
        return;
      }

      if(action === 'done'){
        if(typeof dxSimpleDone === 'function'){
          dxSimpleDone(delId || id);
        }else if(typeof updDel === 'function'){
          updDel(delId || id, 'delivered');
        }else{
          alert('Done function not found.');
        }
        return;
      }

      if(action === 'view'){
        if(typeof dxPreviewItems === 'function'){
          dxPreviewItems(delId || id);
        }
        return;
      }

      if(action === 'address'){
        if(typeof dxPreviewAddress === 'function'){
          dxPreviewAddress(delId || id);
        }
        return;
      }

      if(action === 'items'){
        if(typeof dxPreviewItems === 'function'){
          dxPreviewItems(delId || id);
        }
        return;
      }
    }catch(err){
      console.error('Delivery button action failed:', err);
      alert('Action failed. Check console.');
    }
  }, true);
})();
</script>
'''

if "delivery-button-actions-v10" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    changed += 1

p.write_text(html, encoding="utf-8")
print(f"DONE: delivery button actions patch applied. Changes: {changed}")
