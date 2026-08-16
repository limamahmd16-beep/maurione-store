from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Load IBM Plex Sans Arabic from Google Fonts.
font_links='''<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">\n'''
if 'family=IBM+Plex+Sans+Arabic' not in s:
    s=s.replace('<style>', font_links+'<style>', 1)

old='body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Tahoma,Arial,sans-serif;background:var(--bg);color:var(--text);padding-bottom:82px}'
new='body{font-family:"IBM Plex Sans Arabic",-apple-system,BlinkMacSystemFont,"Segoe UI",Tahoma,Arial,sans-serif;background:var(--bg);color:var(--text);padding-bottom:82px;font-weight:400;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}'
if old not in s:
    raise SystemExit('body font anchor not found')
s=s.replace(old,new,1)

# Refine the visual hierarchy without changing layout.
css='''
/* MauriOne typography */
h1,h2,h3,.section h2,.detail-related-head h2{font-weight:700}
.product h3,.category strong,.trust-card strong,.detail-spec strong,.review-head h3{font-weight:600}
.price,.detail-price,.detail-buybar strong,.customer-order-no,.order-total strong{font-weight:700}
button,.search,input,select,textarea{font-family:inherit}
.brand-name,.detail-topbrand{font-weight:700;letter-spacing:-.15px}
'''
if '/* MauriOne typography */' not in s:
    s=s.replace('</style>', css+'\n</style>', 1)

p.write_text(s,encoding='utf-8')
