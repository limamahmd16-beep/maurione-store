from pathlib import Path

admin_path = Path('admin.html')
index_path = Path('index.html')
admin = admin_path.read_text()
index = index_path.read_text()

# ADMIN: add public product detail fields.
old = '<div class="field full"><label>المواصفات</label><input id="pMeta"></div><div class="field full"><label>صور المنتج — حتى 6</label><input id="pImages" type="file" accept="image/*" multiple>'
new = '<div class="field full"><label>المواصفات المختصرة</label><input id="pMeta"></div><div class="field"><label>العلامة التجارية</label><input id="pBrand" placeholder="Apple, Samsung..."></div><div class="field"><label>الضمان</label><input id="pWarranty" placeholder="مثال: 12 شهر"></div><div class="field full"><label>الوصف الكامل</label><textarea id="pDescription" placeholder="اكتب وصفًا واضحًا للمنتج ومميزاته"></textarea></div><div class="field full"><label>صور المنتج — حتى 6</label><input id="pImages" type="file" accept="image/*" multiple>'
if old not in admin:
    raise SystemExit('admin product fields marker not found')
admin = admin.replace(old, new, 1)

old = "b.set(ref,{name,category:$('pCat').value,meta:$('pMeta').value.trim(),price,stock:Number($('pStock').value||0),min:Number($('pMin').value||0),images,active:true,createdAt:serverTimestamp(),updatedAt:serverTimestamp()});"
new = "b.set(ref,{name,category:$('pCat').value,meta:$('pMeta').value.trim(),brand:$('pBrand').value.trim(),warranty:$('pWarranty').value.trim(),description:$('pDescription').value.trim(),price,stock:Number($('pStock').value||0),min:Number($('pMin').value||0),images,active:true,createdAt:serverTimestamp(),updatedAt:serverTimestamp()});"
if old not in admin:
    raise SystemExit('admin save product marker not found')
admin = admin.replace(old, new, 1)

old = "$('pName').value=$('pCost').value=$('pPrice').value=$('pMeta').value='';"
new = "$('pName').value=$('pCost').value=$('pPrice').value=$('pMeta').value=$('pBrand').value=$('pWarranty').value=$('pDescription').value='';"
if old not in admin:
    raise SystemExit('admin clear product marker not found')
admin = admin.replace(old, new, 1)

# STOREFRONT: product detail styling.
css_marker = '.page-head{padding:26px 15px 13px}'
css = '.product-img[role="button"],.product h3[role="button"]{cursor:pointer}.detail-page{padding:14px 13px 34px}.detail-back{border:0;background:var(--soft);border-radius:50%;width:38px;height:38px;font-size:20px;margin-bottom:12px}.detail-gallery{background:#fff;border:1px solid var(--line);border-radius:20px;padding:10px}.detail-main{height:340px;border-radius:16px;background:var(--soft);display:grid;place-items:center;overflow:hidden}.detail-main img{width:100%;height:100%;object-fit:contain;background:#fff}.detail-thumbs{display:flex;gap:8px;overflow:auto;margin-top:10px}.detail-thumb{flex:0 0 68px;height:68px;border:1px solid var(--line);border-radius:12px;background:#fff;padding:3px;overflow:hidden}.detail-thumb.active{border-color:var(--gold);box-shadow:0 0 0 1px var(--gold)}.detail-thumb img{width:100%;height:100%;object-fit:contain}.detail-info{margin-top:13px;background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px}.detail-category{font-size:10px;color:var(--muted)}.detail-info h1{font-size:25px;line-height:1.35;margin-top:6px}.detail-meta{margin-top:8px;color:var(--muted);font-size:11px;line-height:1.7}.detail-price{font-weight:900;font-size:24px;margin-top:15px}.detail-stock{font-size:11px;color:var(--green);margin-top:7px}.detail-stock.out{color:var(--red)}.detail-specs{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:17px}.detail-spec{background:var(--soft);border-radius:12px;padding:11px}.detail-spec small{display:block;color:var(--muted);font-size:8px}.detail-spec strong{display:block;margin-top:4px;font-size:11px}.detail-description{margin-top:18px;padding-top:16px;border-top:1px solid var(--line)}.detail-description h3{font-size:15px}.detail-description p{margin-top:8px;font-size:11px;color:#555;line-height:1.9;white-space:pre-wrap}.detail-add{width:100%;margin-top:18px;padding:14px;border:0;border-radius:12px;background:#111;color:#fff;font-weight:800}.detail-add:disabled{opacity:.45}'
if css_marker not in index:
    raise SystemExit('store css marker not found')
index = index.replace(css_marker, css + css_marker, 1)

# Product detail page.
page_marker = '<main id="categoriesPage" class="page">'
page = '<main id="productDetailPage" class="page"><div class="detail-page"><button class="detail-back" onclick="openStore(\'home\',\'navHome\')" aria-label="رجوع">×</button><div class="detail-gallery"><div id="detailMain" class="detail-main"></div><div id="detailThumbs" class="detail-thumbs"></div></div><div class="detail-info"><div id="detailCategory" class="detail-category"></div><h1 id="detailName"></h1><div id="detailMeta" class="detail-meta"></div><div id="detailPrice" class="detail-price"></div><div id="detailStock" class="detail-stock"></div><div class="detail-specs"><div class="detail-spec"><small>العلامة التجارية</small><strong id="detailBrand">—</strong></div><div class="detail-spec"><small>الضمان</small><strong id="detailWarranty">—</strong></div></div><div class="detail-description"><h3>تفاصيل المنتج</h3><p id="detailDescription"></p></div><button id="detailAdd" class="detail-add" onclick="addDetailToCart()">أضف للسلة</button></div></div></main>\n'
if page_marker not in index:
    raise SystemExit('store page marker not found')
index = index.replace(page_marker, page + page_marker, 1)

# Product detail JS.
js_marker = 'function productArt(p){'
js = '''let selectedProductId='',selectedProductImage=0;
window.openProduct=id=>{selectedProductId=String(id);selectedProductImage=0;renderProductDetail();openStore('productDetailPage','navHome')};
window.selectProductImage=i=>{selectedProductImage=Number(i)||0;renderProductDetail()};
window.addDetailToCart=()=>{if(selectedProductId)addCart(selectedProductId)};
function renderProductDetail(){const p=products.find(x=>String(x.id)===String(selectedProductId));if(!p)return;const imgs=Array.isArray(p.images)?p.images.filter(Boolean):[];if(selectedProductImage>=imgs.length)selectedProductImage=0;detailCategory.textContent=p.category||'';detailName.textContent=p.name||'منتج';detailMeta.textContent=p.meta||'';detailPrice.textContent=Number(p.price||0).toLocaleString()+' MRU';const available=Number(p.stock||0)>0;detailStock.textContent=available?'✓ متوفر — '+Number(p.stock||0)+' في المخزون':'نفد المخزون';detailStock.className='detail-stock'+(available?'':' out');detailBrand.textContent=p.brand||'غير محدد';detailWarranty.textContent=p.warranty||'غير محدد';detailDescription.textContent=p.description||p.meta||'لا يوجد وصف إضافي لهذا المنتج.';detailAdd.disabled=!available;if(imgs.length){detailMain.innerHTML=`<img src="${esc(imgs[selectedProductImage])}" alt="${esc(p.name||'')}">`;detailThumbs.innerHTML=imgs.map((u,i)=>`<button class="detail-thumb ${i===selectedProductImage?'active':''}" onclick="selectProductImage(${i})"><img src="${esc(u)}" alt=""></button>`).join('')}else{detailMain.innerHTML='<div class="mock"></div>';detailThumbs.innerHTML=''}}
'''
if js_marker not in index:
    raise SystemExit('store product JS marker not found')
index = index.replace(js_marker, js + js_marker, 1)

old = '''function cards(list){if(!list.length)return '<div class="empty">لا توجد منتجات مطابقة.</div>';return list.map(p=>`<div class="product"><div class="product-img">${productArt(p)}</div><small>${esc(p.category)}</small><h3>${esc(p.name)}</h3><small>${esc(p.meta)}</small><div class="price">${Number(p.price||0).toLocaleString()} MRU</div><div class="stock ${Number(p.stock||0)<=0?'out':''}">${Number(p.stock||0)>0?'✓ متوفر':'نفد المخزون'}</div><button class="add" ${Number(p.stock||0)<=0?'disabled':''} onclick="addCart('${esc(p.id)}')">أضف للسلة</button></div>`).join('')}'''
new = '''function cards(list){if(!list.length)return '<div class="empty">لا توجد منتجات مطابقة.</div>';return list.map(p=>`<div class="product"><div class="product-img" role="button" onclick="openProduct('${esc(p.id)}')">${productArt(p)}</div><small>${esc(p.category)}</small><h3 role="button" onclick="openProduct('${esc(p.id)}')">${esc(p.name)}</h3><small>${esc(p.meta)}</small><div class="price">${Number(p.price||0).toLocaleString()} MRU</div><div class="stock ${Number(p.stock||0)<=0?'out':''}">${Number(p.stock||0)>0?'✓ متوفر':'نفد المخزون'}</div><button class="add" ${Number(p.stock||0)<=0?'disabled':''} onclick="addCart('${esc(p.id)}')">أضف للسلة</button></div>`).join('')}'''
if old not in index:
    raise SystemExit('store cards marker not found')
index = index.replace(old, new, 1)

old = 'function renderStore(){productList.innerHTML=cards(products);renderSearch();updateBadge()}'
new = 'function renderStore(){productList.innerHTML=cards(products);renderSearch();updateBadge();if(selectedProductId)renderProductDetail()}'
if old not in index:
    raise SystemExit('store render marker not found')
index = index.replace(old, new, 1)

admin_path.write_text(admin)
index_path.write_text(index)
