from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="kitchen-tabs-compact-mobile-v2">
@media(max-width:768px){
  #view-kitchen .kitchen-tabs-bar{
    gap:6px !important;
    padding:8px !important;
  }

  #view-kitchen .kitchen-tab-btn{
    min-width:auto !important;
    padding:10px 12px !important;
    font-size:0 !important;
    gap:6px !important;
  }

  #view-kitchen .kitchen-tab-btn[data-ktab="all"]::before{
    content:"All";
    font-size:15px;
    font-weight:900;
  }

  #view-kitchen .kitchen-tab-btn[data-ktab="new"]::before{
    content:"New";
    font-size:15px;
    font-weight:900;
  }

  #view-kitchen .kitchen-tab-btn[data-ktab="preparing"]::before{
    content:"Prep";
    font-size:15px;
    font-weight:900;
  }

  #view-kitchen .kitchen-tab-btn[data-ktab="ready"]::before{
    content:"Ready";
    font-size:15px;
    font-weight:900;
  }

  #view-kitchen .kitchen-tab-count{
    font-size:13px !important;
    min-width:25px !important;
    height:25px !important;
    margin-left:6px !important;
  }
}
</style>
'''

if "kitchen-tabs-compact-mobile-v2" in html:
    print("Kitchen compact mobile tabs already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Kitchen compact mobile tabs added.")
