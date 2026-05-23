from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

old = r'''  function dxFindDeliveryArea(){
    var existing = document.getElementById('deliveryExcelRoot');
    if(existing) return existing;

    var headings = Array.from(document.querySelectorAll('h1,h2,h3'));
    var h = headings.find(function(x){ return /delivery tracker|delivery/i.test(x.textContent || ''); });
    var box = h ? (h.closest('.card') || h.parentElement) : null;

    if(!box){
      box = document.querySelector('[data-v="delivery"]') || document.body;
    }

    var root = document.createElement('div');
    root.id = 'deliveryExcelRoot';
    root.className = 'dx-wrap';

    box.innerHTML = '';
    box.appendChild(root);
    return root;
  }'''

new = r'''  function dxFindDeliveryArea(){
    var existing = document.getElementById('deliveryExcelRoot');
    if(existing) return existing;

    var view = document.getElementById('view-delivery');
    var box = view || document.body;

    box.innerHTML = `
      <div class="sh">
        <div>
          <h2>🚚 Delivery</h2>
          <div style="font-size:12px;color:var(--t3);margin-top:2px">Excel-style delivery dispatch board</div>
        </div>
      </div>
      <div id="deliveryExcelRoot" class="dx-wrap"></div>
    `;

    return document.getElementById('deliveryExcelRoot');
  }'''

if old not in html:
    print("Old dxFindDeliveryArea block not found. Showing nearby lines:")
    idx = html.find("function dxFindDeliveryArea")
    print(idx)
    raise SystemExit(1)

html = html.replace(old, new, 1)
p.write_text(html, encoding="utf-8")
print("DONE: Delivery Excel target fixed to #view-delivery.")
