from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
pattern=r'(<section id="siteProductsSection" class="section">.*?</section>)(<section id="siteCategoriesSection" class="section">.*?</section>)'
m=re.search(pattern,s,flags=re.S)
if not m:
    raise SystemExit('Expected adjacent products/categories sections not found')
s=s[:m.start()]+m.group(2)+m.group(1)+s[m.end():]
p.write_text(s,encoding='utf-8')
