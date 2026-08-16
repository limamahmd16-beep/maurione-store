from pathlib import Path

p = Path('admin.html')
s = p.read_text(encoding='utf-8')

old_label = '<div class="stat"><small>المبيعات المكتملة</small><b id="sales">0</b></div>'
new_label = '<div class="stat"><small>مبيعات المنتجات المكتملة</small><b id="sales">0</b></div>'
if old_label not in s:
    raise SystemExit('sales label anchor missing')
s = s.replace(old_label, new_label, 1)

old = "salesTotal=done.reduce((s,o)=>s+Number(o.total||0),0),profitTotal=done.reduce((s,o)=>s+(Array.isArray(o.items)?o.items:[]).reduce((t,i)=>t+(Number(i.price||0)-itemCost(i))*Number(i.qty||1),0),0),margin=salesTotal>0?profitTotal/salesTotal*100:0;"
new = "salesTotal=done.reduce((s,o)=>{const productSales=o.subtotal!==undefined&&o.subtotal!==null?Number(o.subtotal||0):Math.max(0,Number(o.total||0)-Number(o.deliveryFee||0));return s+productSales},0),profitTotal=done.reduce((s,o)=>s+(Array.isArray(o.items)?o.items:[]).reduce((t,i)=>t+(Number(i.price||0)-itemCost(i))*Number(i.qty||1),0),0),margin=salesTotal>0?profitTotal/salesTotal*100:0;"
if old not in s:
    raise SystemExit('financial metrics anchor missing')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('financial metrics patched')
