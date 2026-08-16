from pathlib import Path

# Storefront
p=Path('index.html')
s=p.read_text(encoding='utf-8')

css_anchor='.detail-favorite{width:100%;margin-top:9px;padding:12px;border:1px solid var(--line);border-radius:12px;background:#fff;font-weight:800}.detail-favorite.on{color:#b4233a;border-color:#f1c7cf;background:#fff7f8}'
css_new=css_anchor+'.detail-share{width:100%;margin-top:9px;padding:12px;border:1px solid #d9e1e8;border-radius:12px;background:#f8fbfd;color:var(--navy);font-weight:800}'
if '.detail-share{' not in s:
    assert css_anchor in s, 'share css anchor missing'
    s=s.replace(css_anchor,css_new,1)

html_anchor='<button id="detailFavorite" class="detail-favorite" onclick="toggleFavorite(selectedProductId)">♡ حفظ في المفضلة</button><button id="detailAdd" class="detail-add" onclick="addDetailToCart()">أضف للسلة</button>'
html_new='<button id="detailFavorite" class="detail-favorite" onclick="toggleFavorite(selectedProductId)">♡ حفظ في المفضلة</button><button id="detailShare" class="detail-share" onclick="shareProduct()">↗ مشاركة المنتج</button><button id="detailAdd" class="detail-add" onclick="addDetailToCart()">أضف للسلة</button>'
if 'id="detailShare"' not in s:
    assert html_anchor in s, 'share html anchor missing'
    s=s.replace(html_anchor,html_new,1)

back_old='<button class="detail-back" onclick="openStore(\'home\',\'navHome\')" aria-label="رجوع">×</button>'
back_new='<button class="detail-back" onclick="closeProduct()" aria-label="رجوع">×</button>'
if 'onclick="closeProduct()"' not in s:
    assert back_old in s, 'detail back anchor missing'
    s=s.replace(back_old,back_new,1)

open_old="let selectedProductId='',selectedProductImage=0;\nwindow.openProduct=id=>{selectedProductId=String(id);selectedProductImage=0;reviewRating=0;watchProductReviews(selectedProductId);renderProductDetail();openStore('productDetailPage','navHome')};"
open_new="let selectedProductId='',selectedProductImage=0,deepLinkHandled=false;\nfunction showProduct(id,updateUrl=true){const pid=String(id||'');if(!pid||!products.some(p=>String(p.id)===pid))return false;selectedProductId=pid;selectedProductImage=0;reviewRating=0;watchProductReviews(selectedProductId);renderProductDetail();openStore('productDetailPage','navHome');if(updateUrl){const u=new URL(location.href);u.searchParams.set('product',pid);history.pushState({product:pid},'',u.pathname+u.search)}return true}\nwindow.openProduct=id=>showProduct(id,true);\nwindow.closeProduct=()=>{const u=new URL(location.href);u.searchParams.delete('product');history.pushState({},'',u.pathname+u.search);openStore('home','navHome')};\nfunction handleProductDeepLink(){if(deepLinkHandled)return;const pid=new URLSearchParams(location.search).get('product');if(!pid){deepLinkHandled=true;return}if(showProduct(pid,false))deepLinkHandled=true}\nwindow.addEventListener('popstate',()=>{const pid=new URLSearchParams(location.search).get('product');if(pid&&showProduct(pid,false))return;openStore('home','navHome')});"
if 'function showProduct(' not in s:
    assert open_old in s, 'open product anchor missing'
    s=s.replace(open_old,open_new,1)

add_anchor="window.addDetailToCart=()=>{if(selectedProductId)addCart(selectedProductId)};"
share_func=add_anchor+"\nwindow.shareProduct=async()=>{const p=products.find(x=>String(x.id)===String(selectedProductId));if(!p)return;const u=new URL(location.origin+location.pathname);u.searchParams.set('product',String(p.id));const url=u.toString(),text=`${p.name||'MauriOne'} — ${Number(p.price||0).toLocaleString()} MRU`;try{if(navigator.share){await navigator.share({title:p.name||'MauriOne',text,url});return}if(navigator.clipboard?.writeText){await navigator.clipboard.writeText(url);alert('تم نسخ رابط المنتج.');return}}catch(e){if(e?.name==='AbortError')return}prompt('انسخ رابط المنتج:',url)};"
if 'window.shareProduct=async' not in s:
    assert add_anchor in s, 'share function anchor missing'
    s=s.replace(add_anchor,share_func,1)

products_anchor="onSnapshot(collection(db,'products'),snap=>{const live=snap.docs.map(d=>({id:d.id,...d.data()})).filter(p=>p.active!==false);products=live.length?live:demoProducts;cart=cart.filter(r=>products.some(p=>String(p.id)===String(r.id)));saveCart();renderStore();if(document.getElementById('cartPage').classList.contains('active'))renderCart()},err=>{console.error('Firestore products:',err);products=demoProducts;renderStore()});"
products_new="onSnapshot(collection(db,'products'),snap=>{const live=snap.docs.map(d=>({id:d.id,...d.data()})).filter(p=>p.active!==false);products=live.length?live:demoProducts;cart=cart.filter(r=>products.some(p=>String(p.id)===String(r.id)));saveCart();renderStore();handleProductDeepLink();if(document.getElementById('cartPage').classList.contains('active'))renderCart()},err=>{console.error('Firestore products:',err);products=demoProducts;renderStore();handleProductDeepLink()});"
if 'renderStore();handleProductDeepLink();' not in s:
    assert products_anchor in s, 'products snapshot anchor missing'
    s=s.replace(products_anchor,products_new,1)

p.write_text(s,encoding='utf-8')

# Admin: make review product link open the exact product deep-link.
p=Path('admin.html')
a=p.read_text(encoding='utf-8')
old='<a href="/?product=${encodeURIComponent(r.productId||\'\')}" target="_blank" onclick="event.preventDefault();window.open(\'/\',\'_blank\')">فتح المتجر</a>'
new='<a href="/?product=${encodeURIComponent(r.productId||\'\')}" target="_blank">فتح المنتج</a>'
if old in a:
    a=a.replace(old,new,1)
p.write_text(a,encoding='utf-8')
