from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="preview-modal-responsive-v18">
/* ===== Address / Items Preview Modal Responsive Fix ===== */

.dx-modal-backdrop{
  position:fixed !important;
  inset:0 !important;
  z-index:100000 !important;
  background:rgba(0,0,0,.45) !important;
  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  padding:18px !important;
}

.dx-modal{
  width:min(620px, calc(100vw - 36px)) !important;
  max-height:82vh !important;
  overflow:auto !important;
  background:#fff !important;
  color:#111827 !important;
  border-radius:22px !important;
  padding:20px !important;
  box-shadow:0 18px 60px rgba(0,0,0,.28) !important;
}

.dx-modal h3{
  margin:0 0 14px !important;
  font-size:20px !important;
  font-weight:950 !important;
}

.dx-modal button{
  margin-top:16px !important;
  width:100% !important;
  border:0 !important;
  border-radius:13px !important;
  padding:13px !important;
  background:#15803d !important;
  color:#fff !important;
  font-weight:950 !important;
  cursor:pointer !important;
}

.dx-modal pre{
  white-space:pre-wrap !important;
  font-family:inherit !important;
  line-height:1.5 !important;
  margin:0 !important;
}

/* Better item list spacing */
.dx-modal div[style*="border-bottom"]{
  padding:10px 0 !important;
}

/* Mobile keeps bottom-sheet behavior */
@media(max-width:700px){
  .dx-modal-backdrop{
    align-items:flex-end !important;
    justify-content:center !important;
    padding:0 !important;
  }

  .dx-modal{
    width:100% !important;
    max-height:78vh !important;
    border-radius:22px 22px 0 0 !important;
    padding:18px !important;
    box-shadow:0 -16px 45px rgba(0,0,0,.25) !important;
  }

  .dx-modal h3{
    font-size:18px !important;
  }

  .dx-modal button{
    position:sticky !important;
    bottom:0 !important;
    margin-top:14px !important;
    padding-bottom:calc(13px + env(safe-area-inset-bottom, 0px)) !important;
  }
}
</style>

<script id="preview-modal-responsive-v18">
(function(){
  if(window.__previewModalResponsiveV18) return;
  window.__previewModalResponsiveV18 = true;

  // Close preview when tapping dark backdrop, but not when tapping inside modal.
  document.addEventListener('click', function(e){
    var backdrop = e.target && e.target.id === 'dxPreviewSheet';
    if(backdrop){
      e.preventDefault();
      e.stopPropagation();
      e.target.remove();
    }
  }, true);
})();
</script>
'''

if "preview-modal-responsive-v18" in html:
    print("Preview modal responsive fix already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Preview modal responsive fix added.")
