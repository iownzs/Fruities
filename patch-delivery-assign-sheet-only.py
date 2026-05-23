from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

changed = 0

old = '''return '<button type="button" class="dx-action assign" data-dx-action="assign" data-del-id="'+delId+'" data-order-id="'+orderId+'">Assign</button>';'''
new = '''return '<button type="button" class="dx-action assign" data-dx-action="assign-sheet" data-del-id="'+delId+'" data-order-id="'+orderId+'">Assign</button>';'''

if old in html:
    html = html.replace(old, new, 1)
    changed += 1
else:
    print("Assign button pattern not found or already patched.")

patch = r'''
<script id="delivery-assign-sheet-only-v13">
(function(){
  if(window.__deliveryAssignSheetOnlyV13) return;
  window.__deliveryAssignSheetOnlyV13 = true;

  document.addEventListener('click', function(e){
    var btn = e.target && e.target.closest ? e.target.closest('[data-dx-action="assign-sheet"]') : null;
    if(!btn) return;

    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();

    var delId = btn.getAttribute('data-del-id') || '';
    var orderId = btn.getAttribute('data-order-id') || '';

    if(typeof window.dxOpenAssignSheet === 'function'){
      window.dxOpenAssignSheet(delId, orderId);
    }else if(typeof window.dxExcelAssignRider === 'function'){
      window.dxExcelAssignRider(delId, orderId);
    }else{
      alert('Assign rider sheet not found.');
    }
  }, true);
})();
</script>
'''

if "delivery-assign-sheet-only-v13" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    changed += 1

p.write_text(html, encoding="utf-8")
print(f"DONE: assign sheet only patch applied. Changes: {changed}")
