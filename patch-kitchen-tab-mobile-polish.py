from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="kitchen-tab-mobile-polish-v1">
/* Kitchen tab bar mobile polish */
#view-kitchen .kitchen-tabs-bar,
#view-kitchen [id*="kitchen-tabs"],
#view-kitchen .k-tabs,
#view-kitchen .kit-tabs{
  max-width:100% !important;
  overflow-x:auto !important;
  overflow-y:hidden !important;
  -webkit-overflow-scrolling:touch !important;
  scrollbar-width:none !important;
  flex-wrap:nowrap !important;
}

#view-kitchen .kitchen-tabs-bar::-webkit-scrollbar,
#view-kitchen [id*="kitchen-tabs"]::-webkit-scrollbar,
#view-kitchen .k-tabs::-webkit-scrollbar,
#view-kitchen .kit-tabs::-webkit-scrollbar{
  display:none !important;
}

#view-kitchen .kitchen-tab-btn,
#view-kitchen [data-ktab],
#view-kitchen .k-tab,
#view-kitchen .kit-tab{
  flex:0 0 auto !important;
  white-space:nowrap !important;
  min-height:44px !important;
}

#view-kitchen .kitchen-tab-count,
#view-kitchen [data-kcount]{
  display:inline-flex !important;
  align-items:center !important;
  justify-content:center !important;
  min-width:24px !important;
  height:24px !important;
}

/* reduce large empty gap under tabs */
#view-kitchen .kitchen-tabs-bar + *,
#view-kitchen [id*="kitchen-tabs"] + *{
  margin-top:12px !important;
}

@media(max-width:768px){
  #view-kitchen .kitchen-tabs-bar,
  #view-kitchen [id*="kitchen-tabs"],
  #view-kitchen .k-tabs,
  #view-kitchen .kit-tabs{
    margin-left:-2px !important;
    margin-right:-2px !important;
    padding:8px !important;
  }

  #view-kitchen .kitchen-tab-btn,
  #view-kitchen [data-ktab],
  #view-kitchen .k-tab,
  #view-kitchen .kit-tab{
    padding:10px 14px !important;
    font-size:14px !important;
  }
}
</style>
'''

if "kitchen-tab-mobile-polish-v1" in html:
    print("Kitchen tab mobile polish already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Kitchen tab mobile polish added.")
