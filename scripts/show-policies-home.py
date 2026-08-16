from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

css='''.home-info{margin:34px 12px 30px;padding:20px;border-radius:20px;background:var(--navy);color:#fff}.home-info-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px}.home-info-head strong{font-size:17px}.home-info-head span{font-size:9px;color:#b7c1ca}.home-policy-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.home-policy-link{border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.08);color:#fff;border-radius:12px;padding:13px 10px;text-align:right;font-size:10px;font-weight:800}.home-policy-link:active{background:rgba(255,255,255,.15)}'''
if '.home-info{' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

section='''<section class="home-info" id="homePolicies"><div class="home-info-head"><div><strong>معلومات MauriOne</strong><br><span>سياسات واضحة قبل إتمام الشراء</span></div><div class="mark" aria-hidden="true"><i class="a" style="background:#fff"></i><i class="b"></i></div></div><div class="home-policy-grid"><button class="home-policy-link" onclick="openPolicy('returns')">سياسة الاسترجاع</button><button class="home-policy-link" onclick="openPolicy('shipping')">سياسة التوصيل</button><button class="home-policy-link" onclick="openPolicy('privacy')">سياسة الخصوصية</button><button class="home-policy-link" onclick="openPolicy('terms')">الشروط والأحكام</button></div></section>'''
if 'id="homePolicies"' not in s:
    m=re.search(r'(<main id="home"\s+class="page active">)(.*?)(</main>)',s,re.S)
    if not m:
        raise SystemExit('home main not found')
    body=m.group(2)
    s=s[:m.start()]+m.group(1)+body+section+m.group(3)+s[m.end():]

p.write_text(s,encoding='utf-8')
print('homepage policies visible')
