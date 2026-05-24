from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

replacements = {
    "data-delivery-status": "data-dx-status",
    "data-delivery-priority": "data-dx-priority",
    "data-delivery-date": "data-dx-date",
    "data-delivery-rider": "data-dx-rider",
}

changed = 0
for old, new in replacements.items():
    count = html.count(old)
    if count:
        html = html.replace(old, new)
        changed += count

p.write_text(html, encoding="utf-8")
print("DONE: fixed simple filter attribute names.")
print("Replacements:", changed)
