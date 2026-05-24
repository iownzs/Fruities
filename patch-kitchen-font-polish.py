from pathlib import Path

p = Path("index.html")
html = p.read_text(encoding="utf-8")

patch = r'''
<style id="kitchen-font-polish-v1">
/* Kitchen typography polish: mobile + desktop */
#view-kitchen{
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}

/* Main Kitchen tabs */
#view-kitchen .kitchen-tab-btn{
  letter-spacing:-.01em !important;
  font-weight:900 !important;
}

#view-kitchen .kitchen-tab-count{
  font-weight:950 !important;
}

/* Section title: New Orders / Preparing / Ready */
#view-kitchen h3,
#view-kitchen .k-section-title,
#view-kitchen [class*="section"] h3{
  font-size:20px !important;
  line-height:1.15 !important;
  letter-spacing:-.02em !important;
  font-weight:950 !important;
}

/* Kitchen cards */
#view-kitchen .card,
#view-kitchen [class*="kit-card"],
#view-kitchen [class*="kitchen-card"]{
  letter-spacing:-.01em !important;
}

/* Order number */
#view-kitchen .card strong:first-child,
#view-kitchen [class*="order-id"],
#view-kitchen [class*="order-no"]{
  font-size:13px !important;
  line-height:1.1 !important;
  letter-spacing:.08em !important;
  font-weight:950 !important;
  color:var(--t3,#6b7280) !important;
}

/* Customer name */
#view-kitchen .card h3,
#view-kitchen .card h4,
#view-kitchen [class*="customer"],
#view-kitchen [class*="cust"]{
  font-size:21px !important;
  line-height:1.15 !important;
  letter-spacing:-.025em !important;
  font-weight:950 !important;
  color:var(--t,#111827) !important;
}

/* Price */
#view-kitchen .price,
#view-kitchen [class*="total"],
#view-kitchen .card b{
  font-size:20px !important;
  line-height:1.05 !important;
  letter-spacing:-.02em !important;
  font-weight:950 !important;
}

/* Time/date text */
#view-kitchen .muted,
#view-kitchen .sub,
#view-kitchen small,
#view-kitchen [class*="time"]{
  font-size:13px !important;
  line-height:1.25 !important;
  font-weight:700 !important;
  color:var(--t3,#6b7280) !important;
}

/* Badges: Rush / Pickup / Delivery / channel */
#view-kitchen .tg,
#view-kitchen .badge,
#view-kitchen [class*="badge"],
#view-kitchen [class*="chip"]{
  font-size:13px !important;
  line-height:1.15 !important;
  font-weight:900 !important;
  letter-spacing:-.01em !important;
}

/* Items and notes */
#view-kitchen .card li,
#view-kitchen .card p,
#view-kitchen .card div{
  line-height:1.32 !important;
}

/* Action buttons */
#view-kitchen .btn,
#view-kitchen button{
  font-size:15px !important;
  font-weight:900 !important;
  letter-spacing:-.01em !important;
}

/* Mobile refinements */
@media(max-width:768px){
  #view-kitchen{
    font-size:15px !important;
  }

  #view-kitchen .kitchen-tab-btn{
    font-size:0 !important;
  }

  #view-kitchen .kitchen-tab-btn::before{
    font-size:15px !important;
    letter-spacing:-.02em !important;
    font-weight:950 !important;
  }

  #view-kitchen .kitchen-tab-count{
    font-size:12px !important;
  }

  #view-kitchen h3,
  #view-kitchen .k-section-title,
  #view-kitchen [class*="section"] h3{
    font-size:19px !important;
  }

  #view-kitchen .card{
    border-radius:22px !important;
  }

  #view-kitchen .card h3,
  #view-kitchen .card h4,
  #view-kitchen [class*="customer"],
  #view-kitchen [class*="cust"]{
    font-size:20px !important;
  }

  #view-kitchen .price,
  #view-kitchen [class*="total"],
  #view-kitchen .card b{
    font-size:19px !important;
  }

  #view-kitchen .muted,
  #view-kitchen .sub,
  #view-kitchen small,
  #view-kitchen [class*="time"]{
    font-size:12px !important;
  }

  #view-kitchen .tg,
  #view-kitchen .badge,
  #view-kitchen [class*="badge"],
  #view-kitchen [class*="chip"]{
    font-size:12px !important;
  }

  #view-kitchen .btn,
  #view-kitchen button{
    font-size:15px !important;
    min-height:44px !important;
  }
}

/* Desktop refinements */
@media(min-width:769px){
  #view-kitchen{
    font-size:14px !important;
  }

  #view-kitchen .card h3,
  #view-kitchen .card h4,
  #view-kitchen [class*="customer"],
  #view-kitchen [class*="cust"]{
    font-size:18px !important;
  }

  #view-kitchen .price,
  #view-kitchen [class*="total"],
  #view-kitchen .card b{
    font-size:18px !important;
  }

  #view-kitchen .btn,
  #view-kitchen button{
    font-size:13px !important;
  }
}
</style>
'''

if "kitchen-font-polish-v1" in html:
    print("Kitchen font polish already installed.")
else:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        insert_at = html.rfind("</html>")
    html = html[:insert_at] + patch + "\n" + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    print("DONE: Kitchen font polish added.")
