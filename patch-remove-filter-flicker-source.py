from pathlib import Path
import re

p = Path("index.html")
html = p.read_text(encoding="utf-8")

before = html
changed = 0

# 1) Remove Rush chip from old/original delivery renderer strings
patterns = [
    r"\s*'\s*<button[^']*dxToggleRush\(\)[^']*Rush</button>'\s*\+\s*",
    r"\s*'<button[^']*dxFilterRush\(\)[^']*Rush</button>'\s*\+\s*",
]

for pat in patterns:
    html2, count = re.subn(pat, "\n", html, flags=re.S)
    if count:
        html = html2
        changed += count

# 2) Disable creation of the All Dates button inside smooth calendar patch
old_clear_block = r'''    var clearBtn = document.createElement('button');
    clearBtn.type = 'button';
    clearBtn.className = 'dx-chip';
    clearBtn.textContent = 'All Dates';
    clearBtn.onclick = function(){
      window.dxFilterState.date = 'all';
      dateInput.value = '';
      debounceApply();
    };

    wrap.appendChild(dateInput);
    wrap.appendChild(clearBtn);'''

new_clear_block = r'''    wrap.appendChild(dateInput);'''

if old_clear_block in html:
    html = html.replace(old_clear_block, new_clear_block, 1)
    changed += 1

# 3) Remove any old Rush chip that may exist in the simple renderer literal
html2, count = re.subn(
    r"\s*'\s*<button type=\"button\" class=\"dx-chip [^']*dxFilterRush\(\)[^']*Rush</button>'\s*\+\s*",
    "\n",
    html,
    flags=re.S
)
if count:
    html = html2
    changed += count

# 4) Make reset visible and date input full width after removing All Dates
extra_css = r'''
<style id="delivery-filter-no-flicker-v5">
#deliveryExcelRoot .dx-chip-row .dx-chip{
  min-height:44px;
}
#deliveryExcelRoot .dx-date-wrap{
  display:block !important;
}
#deliveryExcelRoot .dx-date-wrap input[type="date"]{
  width:100% !important;
}
#deliveryExcelRoot .dx-date-wrap button,
#deliveryExcelRoot .dx-date-clear{
  display:none !important;
}
</style>
'''

if "delivery-filter-no-flicker-v5" not in html:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + extra_css + "\n" + html[insert_at:]
    changed += 1

p.write_text(html, encoding="utf-8")

print("DONE: removed Rush/All Dates flicker at source.")
print("Changes:", changed)
print("Changed file:", before != html)
