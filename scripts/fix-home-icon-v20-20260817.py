from pathlib import Path
import json

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="default">\n<meta name="apple-mobile-web-app-title" content="MauriOne">\n<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=2">\n<link rel="icon" type="image/png" sizes="512x512" href="/favicon.png?v=2">\n<link rel="manifest" href="/site.webmanifest?v=2">'''
new='''<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="default">\n<meta name="apple-mobile-web-app-title" content="MauriOne">\n<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=3">\n<link rel="apple-touch-icon-precomposed" sizes="180x180" href="/apple-touch-icon.png?v=3">\n<link rel="icon" type="image/png" sizes="192x192" href="/maurione-icon-192.png?v=3">\n<link rel="icon" type="image/png" sizes="512x512" href="/maurione-icon-512.png?v=3">\n<link rel="manifest" href="/site.webmanifest?v=3">'''
if old not in s:
    raise SystemExit('icon head anchor not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

m=Path('site.webmanifest')
data=json.loads(m.read_text(encoding='utf-8'))
data['id']='/'
data['start_url']='/'
data['name']='MauriOne'
data['short_name']='MauriOne'
data['icons']=[
    {'src':'/maurione-icon-192.png?v=3','sizes':'192x192','type':'image/png','purpose':'any'},
    {'src':'/maurione-icon-512.png?v=3','sizes':'512x512','type':'image/png','purpose':'any'}
]
m.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print('home icon metadata updated')
