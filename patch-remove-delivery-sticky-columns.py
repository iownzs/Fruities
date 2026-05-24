from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

html2, count = re.subn(
    r'\s*<style id="delivery-sticky-columns-v1">.*?</style>\s*',
    '\n',
    html,
    flags=re.S
)

p.write_text(html2, encoding="utf-8")
print("DONE: removed sticky columns style blocks:", count)
