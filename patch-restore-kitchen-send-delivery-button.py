from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

before = html

# Remove old patch that was hiding/removing Send Delivery button
html, count = re.subn(
    r'\s*<script id="hard-remove-send-delivery-card-v1">.*?</script>\s*',
    '\n',
    html,
    flags=re.S
)

p.write_text(html, encoding="utf-8")

print("DONE: removed hard-remove-send-delivery-card-v1 scripts:", count)
print("Changed:", before != html)
