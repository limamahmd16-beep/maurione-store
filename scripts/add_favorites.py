from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# CSS
s=s.replace('.product{border:1px solid var(--line);', '.product{position:relative;border:1px solid var(--line);', 1)
needle='.home-policy-link:active{background:rgba(255,255,255,.15)}\n'
css='''.favorite-btn{position:absolute;top:14px;left:14px;z-index:3;width:34px;height:34px;border:1px solid var(--line);border-radius:50%;background:rgba(255,255,255,.94);display:grid;place-items:center;font-size:19px;box-shadow:0 5px 16px rgba(0,0,0,.07)}.favorite-btn.on{color:#b4233a;border-color:#f1c7cf;background:#fff7f8}.detail-favorite{width:100%;margin-top:9px;padding:12px;border:1px solid var(--line);border-radius:12px;background:#fff;font-weight:800}.detail-favorite.on{color:#b4233a;border-color:#f1c7cf;background:#fff7f8}.favorites-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}.favorites-head h2{font-size:16px}.favorites-count{font-size:9px;background:var(--soft);padding:5px 8px;border-radius:20px;color:var(--muted)}\n'''
if css.strip() not in s:
    if needle not in s: raise SystemExit('CSS anchor missing')
    s=s.replace(needle, needle+css, 1)

# Product detail favorite control
old='<button id="detailAdd" class="detail-add" onclick="addDetailToCart()">أضف للسلة</button>'
new='<button id="detailFavorite" class="detail-favorite" onclick="toggleFavorite(selectedProductId)">♡ حفظ في المفضلة</button><button id="detailAdd" class="detail-add" onclick="addDetailToCart()">أضف للسلة</button>'
if old in s and 'id="detailFavorite"' not in s:
    s=s.replace(old,new,1)

# Favorites section in account
anchor='</div></div><div class="box policy-menu"><h2>سياسات MauriOne</h2>'
fav_html='''</div></div><div class="box"><div class="favorites-head"><h2>المفضلة</h2><span id="favoritesCount" class="favorites-count">0</span></div><div id="favoritesList" class="products" style="margin-top:0;padding-bottom:0"></div></div><div class="box policy-menu"><h2>سياسات MauriOne</h2>'''
if anchor in s and 'id="favoritesList"' not in s:
    s=s.replace(anchor,fav_html,1)

# State
old_state='let orderHistory=[],currentUser=null,customerOrdersUnsub=null,customerProfileUnsub=null;'
new_state='let orderHistory=[],currentUser=null,customerOrdersUnsub=null,customerProfileUnsub=null,favoritesUnsub=null,favoriteIds=[],favoriteWriteBusy=false;'
if old_state in s:
    s=s.replace(old_state,new_state,1)

# openStore account render
old_open="if(id==='accountPage')loadAccount();window.scrollTo(0,0)"
new_open="if(id==='accountPage'){loadAccount();renderFavorites()}window.scrollTo(0,0)"
if old_open in s:
    s=s.replace(old_open,new_open,1)

# Replace product detail renderer
start=s.index('function renderProductDetail(){')
end=s.index('\nfunction productArt', start)
new_detail="""function renderProductDetail(){const p=products.find(x=>String(x.id)===String(selectedProductId));if(!p)return;const imgs=Array.isArray(p.images)?p.images.filter(Boolean):[];if(selectedProductImage>=imgs.length)selectedProductImage=0;detailCategory.textContent=displayCategory(p.category||'');detailName.textContent=p.name||ct('genericProductText');detailMeta.textContent=p.meta||'';detailPrice.textContent=Number(p.price||0).toLocaleString()+' MRU';const available=Number(p.stock||0)>0;detailStock.textContent=available?tpl('availableTemplate',{stock:Number(p.stock||0)}):ct('outOfStockText');detailStock.className='detail-stock'+(available?'':' out');detailBrand.textContent=p.brand||ct('unspecifiedText');detailWarranty.textContent=p.warranty||ct('unspecifiedText');detailDescription.textContent=p.description||p.meta||ct('noDescriptionText');detailAdd.textContent=ct('addCartText');detailAdd.disabled=!available;const fav=document.getElementById('detailFavorite');if(fav){const on=isFavorite(p.id);fav.textContent=on?'♥ محفوظ في المفضلة':'♡ حفظ في المفضلة';fav.className='detail-favorite'+(on?' on':'')}if(imgs.length){detailMain.innerHTML=`<img src=\"${esc(imgs[selectedProductImage])}\" alt=\"${esc(p.name||'')}\">`;detailThumbs.innerHTML=imgs.map((u,i)=>`<button class=\"detail-thumb ${i===selectedProductImage?'active':''}\" onclick=\"selectProductImage(${i})\"><img src=\"${esc(u)}\" alt=\"\"></button>`).join('')}else{detailMain.innerHTML='<div class=\"mock\"></div>';detailThumbs.innerHTML=''}}"""
s=s[:start]+new_detail+s[end:]

# Replace cards + renderStore
start=s.index('function cards(list){')
end=s.index('\nwindow.renderSearch=', start)
new_cards="""function isFavorite(id){return favoriteIds.includes(String(id))}
function cards(list){if(!list.length)return `<div class=\"empty\">${esc(ct('noProductsMessage'))}</div>`;return list.map(p=>`<div class=\"product\"><button class=\"favorite-btn ${isFavorite(p.id)?'on':''}\" onclick=\"toggleFavorite('${esc(p.id)}')\" aria-label=\"المفضلة\">${isFavorite(p.id)?'♥':'♡'}</button><div class=\"product-img\" role=\"button\" onclick=\"openProduct('${esc(p.id)}')\">${productArt(p)}</div><small>${esc(displayCategory(p.category||''))}</small><h3 role=\"button\" onclick=\"openProduct('${esc(p.id)}')\">${esc(p.name||ct('genericProductText'))}</h3><small>${esc(p.meta)}</small><div class=\"price\">${Number(p.price||0).toLocaleString()} MRU</div><div class=\"stock ${Number(p.stock||0)<=0?'out':''}\">${Number(p.stock||0)>0?esc(tpl('availableTemplate',{stock:Number(p.stock||0)})):esc(ct('outOfStockText'))}</div><button class=\"add\" ${Number(p.stock||0)<=0?'disabled':''} onclick=\"addCart('${esc(p.id)}')\">${esc(ct('addCartText'))}</button></div>`).join('')}
function renderFavorites(){const box=document.getElementById('favoritesList'),count=document.getElementById('favoritesCount');if(!box)return;if(!currentUser){if(count)count.textContent='0';box.innerHTML='<div class=\"empty\">سجّل الدخول لتظهر المنتجات المحفوظة في حسابك.</div>';return}const list=favoriteIds.map(id=>products.find(p=>String(p.id)===String(id))).filter(Boolean);if(count)count.textContent=String(list.length);box.innerHTML=list.length?cards(list):'<div class=\"empty\">لم تضف أي منتج إلى المفضلة بعد.</div>'}
window.toggleFavorite=async id=>{id=String(id||'');if(!id)return;if(!currentUser){openStore('accountPage','navAccount');setTimeout(()=>alert('سجّل الدخول إلى MauriOne أولًا لحفظ المفضلة.'),60);return}if(favoriteWriteBusy)return;const before=[...favoriteIds],next=isFavorite(id)?favoriteIds.filter(x=>x!==id):[...favoriteIds,id];if(next.length>200)return alert('وصلت إلى الحد الأقصى للمفضلة.');favoriteWriteBusy=true;favoriteIds=next;renderStore();try{await setDoc(doc(db,'customerFavorites',currentUser.uid),{uid:currentUser.uid,productIds:next,updatedAt:serverTimestamp()})}catch(e){console.error('Favorites:',e);favoriteIds=before;renderStore();alert(e?.code==='permission-denied'?'يجب نشر قواعد Firestore الجديدة لتفعيل المفضلة.':'تعذر حفظ المفضلة. حاول مرة أخرى.')}finally{favoriteWriteBusy=false}};
function renderStore(){productList.innerHTML=cards(products);renderSearch();renderFavorites();updateBadge();if(selectedProductId)renderProductDetail()}"""
s=s[:start]+new_cards+s[end:]

# Add favorites watcher before orders watcher
anchor='function watchCustomerOrders(){'
watch="""function watchFavorites(){if(favoritesUnsub){favoritesUnsub();favoritesUnsub=null}favoriteIds=[];renderFavorites();if(!currentUser){renderStore();return}const uid=currentUser.uid;favoritesUnsub=onSnapshot(doc(db,'customerFavorites',uid),snap=>{if(!currentUser||currentUser.uid!==uid)return;const d=snap.data()||{},ids=Array.isArray(d.productIds)?d.productIds:[];favoriteIds=[...new Set(ids.map(String))].slice(0,200);renderStore()},e=>{console.warn('Favorites:',e.code||e.message);if(currentUser&&currentUser.uid===uid){favoriteIds=[];renderStore()}})}
"""
if anchor in s and 'function watchFavorites()' not in s:
    s=s.replace(anchor,watch+anchor,1)

# Auth callback invokes favorites watcher
old="watchCustomerProfile();watchCustomerOrders();if(document.getElementById('accountPage')?.classList.contains('active'))loadAccount()"
new="watchCustomerProfile();watchFavorites();watchCustomerOrders();if(document.getElementById('accountPage')?.classList.contains('active'))loadAccount()"
if old in s:
    s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')

# Firestore rules
rp=Path('firestore.rules')
r=rp.read_text(encoding='utf-8')
if 'match /customerFavorites/{userId}' not in r:
    anchor='''    match /categories/{categoryId} {\n'''
    block='''    match /customerFavorites/{userId} {\n      allow read: if isAdmin()\n        || (signedIn() && request.auth.uid == userId);\n\n      allow create, update: if signedIn()\n        && request.auth.uid == userId\n        && request.resource.data.keys().hasAll([\n          'uid',\n          'productIds',\n          'updatedAt'\n        ])\n        && request.resource.data.keys().hasOnly([\n          'uid',\n          'productIds',\n          'updatedAt'\n        ])\n        && request.resource.data.uid == request.auth.uid\n        && request.resource.data.productIds is list\n        && request.resource.data.productIds.size() <= 200\n        && request.resource.data.updatedAt == request.time;\n\n      allow delete: if isAdmin()\n        || (signedIn() && request.auth.uid == userId);\n    }\n\n'''
    if anchor not in r: raise SystemExit('rules anchor missing')
    r=r.replace(anchor,block+anchor,1)
rp.write_text(r,encoding='utf-8')

# Basic assertions
out=p.read_text(encoding='utf-8')
assert 'customerFavorites' in out
assert 'id="favoritesList"' in out
assert 'function watchFavorites()' in out
assert 'toggleFavorite' in out
assert 'id="detailFavorite"' in out
assert 'match /customerFavorites/{userId}' in rp.read_text(encoding='utf-8')
print('favorites patch applied')
