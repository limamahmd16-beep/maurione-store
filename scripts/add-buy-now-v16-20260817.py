from pathlib import Path

p = Path('index.html')
html = p.read_text(encoding='utf-8')

old = '''<div class="stock ${Number(p.stock||0)<=0?'out':''}">${Number(p.stock||0)>0?esc(tpl('availableTemplate',{stock:Number(p.stock||0)})):esc(ct('outOfStockText'))}</div><button class="add" ${Number(p.stock||0)<=0?'disabled':''} onclick="addCart('${esc(p.id)}')">${esc(ct('addCartText'))}</button></div>'''
new = '''<div class="stock ${Number(p.stock||0)<=0?'out':''}">${Number(p.stock||0)>0?esc(tpl('availableTemplate',{stock:Number(p.stock||0)})):esc(ct('outOfStockText'))}</div><div class="product-actions-row"><button class="add" ${Number(p.stock||0)<=0?'disabled':''} onclick="addCart('${esc(p.id)}')">${esc(ct('addCartText'))}</button><button class="buy-now" ${Number(p.stock||0)<=0?'disabled':''} onclick="buyNow('${esc(p.id)}')">اشتري الآن</button></div></div>'''

if old not in html:
    raise SystemExit('cards anchor not found')
html = html.replace(old, new, 1)

anchor = "window.addCart=id=>{const p=products.find(x=>String(x.id)===String(id));if(!p||Number(p.stock||0)<=0)return;const row=cart.find(x=>String(x.id)===String(id));if(row){if(row.qty>=Number(p.stock||0))return alert(ct('stockLimitMessage'));row.qty++}else cart.push({id:String(id),qty:1});saveCart();updateBadge();openStore('cartPage','navCart')};"
insert = anchor + "\nwindow.buyNow=id=>{const p=products.find(x=>String(x.id)===String(id));if(!p||Number(p.stock||0)<=0)return;const row=cart.find(x=>String(x.id)===String(id));if(!row)cart.push({id:String(id),qty:1});saveCart();updateBadge();renderCart();checkout()};"
if anchor not in html:
    raise SystemExit('addCart anchor not found')
html = html.replace(anchor, insert, 1)

css = '''
/* MauriOne buy now v16 */
.product-actions-row{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:7px;
  margin-top:7px;
}
.product-actions-row .add{
  margin-top:0!important;
  min-width:0;
}
.buy-now{
  width:100%;
  min-width:0;
  padding:10px 6px;
  border:0;
  border-radius:11px;
  background:linear-gradient(135deg,#e6ba62,#c9943d);
  color:#fff;
  font-size:11px;
  font-weight:800;
}
.buy-now:disabled{
  opacity:.4;
}
@media(max-width:390px){
  .product-actions-row{gap:6px}
  .product-actions-row .add,.buy-now{font-size:10px;padding:9px 4px}
}
'''
marker = '/* MauriOne buy now v16 */'
if marker not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

p.write_text(html, encoding='utf-8')
assert marker in html
assert 'window.buyNow=id=>' in html
assert 'product-actions-row' in html
print('buy now button added')
