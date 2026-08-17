from pathlib import Path
p=Path('index.html')
html=p.read_text(encoding='utf-8')
old="const demoProducts=[{id:'demo1',name:'iPhone 15 Pro Max',category:'الهواتف',meta:'256GB • Titanium',price:46900,stock:5},{id:'demo2',name:'Galaxy S24 Ultra',category:'الهواتف',meta:'256GB • Phantom Black',price:38900,stock:2},{id:'demo3',name:'AirPods Pro 2',category:'السماعات',meta:'USB-C',price:6900,stock:0}];"
new="const demoProducts=[];"
if old not in html:
    raise SystemExit('demoProducts anchor not found')
html=html.replace(old,new,1)
p.write_text(html,encoding='utf-8')
assert 'iPhone 15 Pro Max' not in html
assert 'Galaxy S24 Ultra' not in html
assert 'AirPods Pro 2' not in html
assert 'const demoProducts=[];' in html
print('demo products removed')
