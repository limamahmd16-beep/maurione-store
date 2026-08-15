from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old=s
s=s.replace('<div class="phone"></div>','')
s=re.sub(r'\.phone\{position:absolute;width:160px;height:310px;right:30px;bottom:-70px;border-radius:40px;border:4px solid #41444b;transform:rotate\(8deg\);background:radial-gradient\(circle at 35% 20%,#693dff,transparent 25%\),radial-gradient\(circle at 65% 68%,#006cff,transparent 34%\),#0d0f13\}', '', s)
if s==old:
    raise SystemExit('hero phone element/style not found')
p.write_text(s,encoding='utf-8')
print('Removed decorative hero phone')
