from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

css_anchor='.review-empty{padding:16px 0;text-align:center;color:var(--muted);font-size:10px}'
css_add=css_anchor+'.order-review-btn{margin-top:8px;border:1px solid #eadfc9;background:#fffaf1;color:#8b6425;border-radius:9px;padding:7px 10px;font-size:9px;font-weight:800}'
if '.order-review-btn{' not in s:
    if css_anchor not in s: raise SystemExit('CSS anchor not found')
    s=s.replace(css_anchor,css_add,1)

old="function renderOrderItems(items){return (Array.isArray(items)?items:[]).map(item=>`<div class=\"customer-order-item\">${item.image?`<img src=\"${esc(item.image)}\" alt=\"\">`:`<div class=\"no-img\">${esc(ct('noImageLabel'))}</div>`}<div><strong>${esc(item.name||ct('genericProductText'))}</strong><small>${Number(item.qty||1)} × ${Number(item.price||0).toLocaleString()} MRU</small></div></div>`).join('')}"
new="function renderOrderItems(items,orderStatus){return (Array.isArray(items)?items:[]).map(item=>`<div class=\"customer-order-item\">${item.image?`<img src=\"${esc(item.image)}\" alt=\"\">`:`<div class=\"no-img\">${esc(ct('noImageLabel'))}</div>`}<div><strong>${esc(item.name||ct('genericProductText'))}</strong><small>${Number(item.qty||1)} × ${Number(item.price||0).toLocaleString()} MRU</small>${orderStatus==='delivered'&&item.productId?`<button class=\"order-review-btn\" onclick=\"openProductReview('${esc(item.productId)}')\">⭐ قيّم المنتج</button>`:''}</div></div>`).join('')}"
if old not in s: raise SystemExit('renderOrderItems anchor not found')
s=s.replace(old,new,1)

old_call='${renderOrderItems(o.items)}'
new_call='${renderOrderItems(o.items,o.status)}'
if old_call not in s: raise SystemExit('renderMyOrders call anchor not found')
s=s.replace(old_call,new_call,1)

anchor="window.openProduct=id=>{selectedProductId=String(id);selectedProductImage=0;reviewRating=0;watchProductReviews(selectedProductId);renderProductDetail();openStore('productDetailPage','navHome')};"
add=anchor+"\nwindow.openProductReview=id=>{window.openProduct(id);setTimeout(()=>document.getElementById('productReviews')?.scrollIntoView({behavior:'smooth',block:'start'}),180)};"
if 'window.openProductReview=' not in s:
    if anchor not in s: raise SystemExit('openProduct anchor not found')
    s=s.replace(anchor,add,1)

p.write_text(s,encoding='utf-8')
