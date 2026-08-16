from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Add related products section inside the product page before the sticky buy bar.
anchor='<div class="detail-buybar"><div><small>السعر</small><strong id="detailBuyPrice">—</strong></div><button id="detailAdd" class="detail-add" onclick="addDetailToCart()">أضف للسلة</button></div>'
related='''<section class="detail-related"><div class="detail-related-head"><div><small>اكتشف المزيد</small><h2>منتجات قد تعجبك</h2></div><button onclick="showAllProducts()">عرض الكل</button></div><div id="relatedProducts" class="products detail-related-grid"></div></section>'''
if 'id="relatedProducts"' not in s:
    if anchor not in s:
        raise SystemExit('buy bar anchor not found')
    s=s.replace(anchor, related+anchor, 1)

# Restore the normal MauriOne chrome and keep the buy bar above bottom navigation.
css='''
/* MauriOne product detail v3 — embedded in platform */
body.product-open{padding-bottom:160px;background:#fff}
body.product-open header{display:block}
body.product-open .bottom-nav{display:grid}
.detail-v2{padding:0 12px 190px;background:#fff;min-height:auto}
.detail-topbar{height:54px;position:relative;top:auto;background:#fff;backdrop-filter:none;-webkit-backdrop-filter:none}
.detail-topbrand{font-size:13px;color:#333}
.detail-summary,.detail-v2 .detail-gallery,.detail-v2 .detail-info{box-shadow:none}
.detail-related{margin-top:12px;background:#fff;border:1px solid #ececef;border-radius:22px;padding:16px}
.detail-related-head{display:flex;align-items:end;justify-content:space-between;gap:12px;margin-bottom:12px}
.detail-related-head small{display:block;color:var(--muted);font-size:9px;margin-bottom:3px}
.detail-related-head h2{font-size:19px;line-height:1.3}
.detail-related-head button{border:0;background:transparent;color:var(--muted);font-size:10px;padding:5px 0}
.detail-related-grid{margin-top:0;padding-bottom:0;gap:9px}
.detail-related-grid .product{border-radius:16px;padding:7px}
.detail-related-grid .product-img{height:125px;border-radius:12px}
.detail-related-grid .product h3{font-size:11.5px;min-height:34px}
.detail-related-grid .price{font-size:13px}
.detail-related-grid .add{font-size:10px;padding:9px}
.detail-buybar{bottom:calc(58px + env(safe-area-inset-bottom));z-index:95;border-radius:18px 18px 0 0;box-shadow:0 -8px 24px rgba(0,0,0,.05)}
@media(min-width:700px){.detail-buybar{bottom:72px}}
'''
if '/* MauriOne product detail v3 — embedded in platform */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Render related products: same category first, then other products, excluding current product.
old="if(imgs.length){detailMain.innerHTML=`<img src=\"${esc(imgs[selectedProductImage])}\" alt=\"${esc(p.name||'')}\">`;detailThumbs.innerHTML=imgs.map((u,i)=>`<button class=\"detail-thumb ${i===selectedProductImage?'active':''}\" onclick=\"selectProductImage(${i})\"><img src=\"${esc(u)}\" alt=\"\"></button>`).join('')}else{detailMain.innerHTML='<div class=\"mock\"></div>';detailThumbs.innerHTML=''}}"
new="if(imgs.length){detailMain.innerHTML=`<img src=\"${esc(imgs[selectedProductImage])}\" alt=\"${esc(p.name||'')}\">`;detailThumbs.innerHTML=imgs.map((u,i)=>`<button class=\"detail-thumb ${i===selectedProductImage?'active':''}\" onclick=\"selectProductImage(${i})\"><img src=\"${esc(u)}\" alt=\"\"></button>`).join('')}else{detailMain.innerHTML='<div class=\"mock\"></div>';detailThumbs.innerHTML=''}const relatedBox=document.getElementById('relatedProducts');if(relatedBox){const others=products.filter(x=>String(x.id)!==String(p.id));const same=others.filter(x=>x.category===p.category),rest=others.filter(x=>x.category!==p.category);relatedBox.innerHTML=cards([...same,...rest].slice(0,6))}}"
if old not in s:
    raise SystemExit('renderProductDetail end anchor not found')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
