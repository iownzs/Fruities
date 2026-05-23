from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

before = html

# Fix over-escaped quotes inside JS string-built onclick handlers
html = html.replace("dxPreviewAddress(\\\\''+esc(id)+'\\\\')", "dxPreviewAddress(\\''+esc(id)+'\\')")
html = html.replace("dxPreviewItems(\\\\''+esc(id)+'\\\\')", "dxPreviewItems(\\''+esc(id)+'\\')")

# Fix over-escaped quote in preview sheet close button if present
html = html.replace("document.getElementById(\\\\'dxPreviewSheet\\\\').remove()", "document.getElementById(\\'dxPreviewSheet\\').remove()")

p.write_text(html, encoding="utf-8")

print("DONE")
print("Changed:", before != html)
