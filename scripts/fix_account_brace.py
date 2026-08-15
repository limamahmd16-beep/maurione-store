from pathlib import Path

p=Path('index.html')
s=p.read_text()
old="function account(){try{return JSON.parse(localStorage.getItem('MauriOne_account')||'{}')}catch{return {}}\n"
new="function account(){try{return JSON.parse(localStorage.getItem('MauriOne_account')||'{}')}catch{return {}}}\n"
if old not in s:
    raise SystemExit('broken account function marker not found')
s=s.replace(old,new,1)
p.write_text(s)
print('fixed missing account function brace')
