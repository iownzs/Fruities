from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="kitchen-tabs-fit-mobile-v3">
@media(max-width:768px){
  #view-kitchen .kitchen-tabs-bar{
    justify-content:flex-start !important;
    gap:5px !important;
  }

  #view-kitchen .kitchen-tab-btn{
    padding:9px 10px !important;
    font-size:0 !important;
    gap:4px !important;
  }

  #view-kitchen .kitchen-tab-btn::before{
    font-size:14px !important;
  }

  #view-kitchen .kitchen-tab-count{
    min-width:22px !important;
    height:22px !important;
    font-size:12px !important;
    margin-left:4px !important;
  }
}
</style>
'''

if "kitchen-tabs-fit-mobile-v3" in html:
    print("Kitchen tabs fit mobile already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Kitchen tabs mobile fit added.")
