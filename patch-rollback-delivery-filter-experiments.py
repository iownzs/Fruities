from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

ids = [
    "delivery-real-filters-v1",
    "delivery-filter-smooth-calendar-v2",
    "delivery-filter-ui-fix-v3",
    "delivery-filter-cleanup-v4",
    "delivery-filter-no-flicker-v5",
    "delivery-filter-hide-until-ready-v6",
    "delivery-orders-style-filters-v7",
    "delivery-filter-no-search-preserve-scroll-v8",
    "delivery-compact-filter-click-fix-v9",
    "delivery-final-compact-filter-v10",
]

removed = 0

for sid in ids:
    html, c1 = re.subn(
        r'\s*<style id="' + re.escape(sid) + r'">.*?</style>\s*',
        '\n',
        html,
        flags=re.S
    )
    html, c2 = re.subn(
        r'\s*<script id="' + re.escape(sid) + r'">.*?</script>\s*',
        '\n',
        html,
        flags=re.S
    )
    removed += c1 + c2

p.write_text(html, encoding="utf-8")
print("DONE: rolled back delivery filter experiment patches.")
print("Removed blocks:", removed)
