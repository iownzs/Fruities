from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="hide-kitchen-extra-header-v1">
/* Hide duplicate Kitchen Board title/subtitle inside Kitchen view */
#view-kitchen .sh{
  display:none !important;
}

/* Reduce top spacing after removing duplicate header */
#view-kitchen{
  padding-top:10px !important;
}
</style>
'''

if "hide-kitchen-extra-header-v1" in html:
    print("Kitchen extra header already hidden.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Kitchen extra header hidden.")
