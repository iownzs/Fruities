from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

old = r'''    try{
      if(action === 'assign'){
        if(typeof quickAssignRider === 'function'){
          quickAssignRider(delId || id);
        }else{
          alert('quickAssignRider() not found.');
        }
        return;
      }

      if(action === 'done'){
        if(typeof dxSimpleDone === 'function'){
          dxSimpleDone(delId || id);
        }else if(typeof updDel === 'function'){
          updDel(delId || id, 'delivered');
        }else{
          alert('Done function not found.');
        }
        return;
      }'''

new = r'''    try{
      // Assign/Done are handled by delivery-assign-done-fix-v11.
      // Do not run the old handler because it can fail before the new handler works.
      if(action === 'assign' || action === 'done'){
        return;
      }'''

if old not in html:
    print("Old v10 assign/done block not found. It may already be patched.")
else:
    html = html.replace(old, new, 1)
    p.write_text(html, encoding="utf-8")
    print("DONE: old v10 assign/done handler disabled.")
