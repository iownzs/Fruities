from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

old1 = "  setInterval(runExcel, 3000);"
new1 = "  // Disabled old runExcel interval to prevent horizontal scroll reset."

old2 = "  setInterval(boot,3000);"
new2 = "  // Disabled old boot interval to prevent horizontal scroll reset."

changed = 0

if old1 in html:
    html = html.replace(old1, new1)
    changed += 1

if old2 in html:
    html = html.replace(old2, new2)
    changed += 1

p.write_text(html, encoding="utf-8")
print(f"DONE: disabled {changed} old delivery refresh interval(s).")
