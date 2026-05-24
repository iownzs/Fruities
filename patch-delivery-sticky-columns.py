from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="delivery-sticky-columns-v1">
/* Sticky Delivery Excel columns */
.dx-table th:first-child,
.dx-table td:first-child{
  position:sticky;
  left:0;
  z-index:4;
  background:var(--card,#fff);
  box-shadow:2px 0 8px rgba(0,0,0,.06);
}

.dx-table th:first-child{
  z-index:6;
  background:#f8fafc;
}

.dx-table th:last-child,
.dx-table td:last-child{
  position:sticky;
  right:0;
  z-index:4;
  background:var(--card,#fff);
  box-shadow:-2px 0 8px rgba(0,0,0,.06);
}

.dx-table th:last-child{
  z-index:6;
  background:#f8fafc;
}

/* Keep action buttons readable while sticky */
.dx-table td:last-child{
  min-width:96px;
}

.dx-table th:first-child,
.dx-table td:first-child{
  min-width:112px;
}

@media(max-width:700px){
  .dx-table th:first-child,
  .dx-table td:first-child{
    min-width:104px;
  }

  .dx-table td:last-child{
    min-width:88px;
  }

  .dx-action{
    padding:8px 10px !important;
    min-width:70px !important;
    font-size:12px !important;
  }
}
</style>
'''

if "delivery-sticky-columns-v1" in html:
    print("Sticky columns already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Delivery sticky columns added.")
