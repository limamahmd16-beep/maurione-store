from pathlib import Path

# ---------- storefront ----------
p=Path('index.html')
s=p.read_text(encoding='utf-8')

css_anchor='.order-review-btn{margin-top:8px;border:1px solid #eadfc9;background:#fffaf1;color:#8b6425;border-radius:9px;padding:7px 10px;font-size:9px;font-weight:800}'
css_add=css_anchor+'.product-rating{display:flex;align-items:center;gap:5px;margin-top:6px;font-size:9px}.product-rating .stars{color:var(--gold);letter-spacing:.5px}.product-rating .rating-count{color:var(--muted)}'
if '.product-rating{' not in s:
    assert css_anchor in s, 'storefront css anchor missing'
    s=s.replace(css_anchor,css_add,1)

state_old="let orderHistory=[],currentUser=null,customerOrdersUnsub=null,customerProfileUnsub=null,favoritesUnsub=null,favoriteIds=[],favoriteWriteBusy=false,reviewUnsub=null,reviewRows=[],reviewRating=0,reviewProductId='',reviewSaveBusy=false;"
state_new="let orderHistory=[],currentUser=null,customerOrdersUnsub=null,customerProfileUnsub=null,favoritesUnsub=null,favoriteIds=[],favoriteWriteBusy=false,reviewUnsub=null,reviewRows=[],allReviewRows=[],reviewRating=0,reviewProductId='',reviewSaveBusy=false;"
if 'allReviewRows=[]' not in s:
    assert state_old in s, 'storefront state anchor missing'
    s=s.replace(state_old,state_new,1)

func_anchor="function isFavorite(id){return favoriteIds.includes(String(id))}"
func_add=func_anchor+"\nfunction productReviewSummary(id){const rows=allReviewRows.filter(r=>String(r.productId)===String(id));if(!rows.length)return{count:0,avg:0};return{count:rows.length,avg:rows.reduce((a,r)=>a+Number(r.rating||0),0)/rows.length}}\nfunction productRatingHtml(id){const x=productReviewSummary(id);return x.count?`<div class=\"product-rating\"><span class=\"stars\">★</span><b>${x.avg.toFixed(1)}</b><span class=\"rating-count\">(${x.count})</span></div>`:'<div class=\"product-rating\"><span class=\"rating-count\">لا توجد تقييمات بعد</span></div>'}"
if 'function productReviewSummary' not in s:
    assert func_anchor in s, 'storefront function anchor missing'
    s=s.replace(func_anchor,func_add,1)

card_old='<small>${esc(p.meta)}</small><div class="price">${Number(p.price||0).toLocaleString()} MRU</div>'
card_new='<small>${esc(p.meta)}</small>${productRatingHtml(p.id)}<div class="price">${Number(p.price||0).toLocaleString()} MRU</div>'
if '${productRatingHtml(p.id)}' not in s:
    assert card_old in s, 'storefront card anchor missing'
    s=s.replace(card_old,card_new,1)

snap_anchor="onSnapshot(collection(db,'products'),snap=>{const live=snap.docs.map(d=>({id:d.id,...d.data()})).filter(p=>p.active!==false);products=live.length?live:demoProducts;cart=cart.filter(r=>products.some(p=>String(p.id)===String(r.id)));saveCart();renderStore();if(document.getElementById('cartPage').classList.contains('active'))renderCart()},err=>{console.error('Firestore products:',err);products=demoProducts;renderStore()});"
snap_new="onSnapshot(collection(db,'productReviews'),snap=>{allReviewRows=snap.docs.map(d=>({id:d.id,...d.data()}));renderStore()},e=>{console.warn('Public reviews:',e.code||e.message);allReviewRows=[];renderStore()});\n"+snap_anchor
if "Public reviews:" not in s:
    assert snap_anchor in s, 'storefront reviews snapshot anchor missing'
    s=s.replace(snap_anchor,snap_new,1)

p.write_text(s,encoding='utf-8')

# ---------- admin ----------
p=Path('admin.html')
a=p.read_text(encoding='utf-8')

css_admin_anchor='@media(max-width:390px){.grid{grid-template-columns:1fr}.full{grid-column:auto}.moreCards{grid-template-columns:1fr 1fr}.actionsRow{grid-template-columns:1fr}}'
css_admin_add='.reviewAdminCard{border:1px solid #e8e8eb;border-radius:14px;padding:13px;margin:10px 0;background:#fff}.reviewAdminHead{display:flex;justify-content:space-between;gap:10px;align-items:center}.reviewAdminStars{color:#d3a44d;direction:ltr;font-size:15px}.reviewAdminText{margin-top:9px;line-height:1.8;font-size:11px;color:#444;white-space:pre-wrap}.reviewAdminMeta{margin-top:8px;color:#888;font-size:9px;line-height:1.7}.reviewAdminActions{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:10px}.reviewAdminActions button,.reviewAdminActions a{border:1px solid #ddd;background:#fff;border-radius:10px;padding:9px;text-align:center;text-decoration:none;color:#111;font-size:9px}.reviewAdminActions .danger{color:#b42318;border-color:#f1c7c3}'
if '.reviewAdminCard{' not in a:
    assert css_admin_anchor in a, 'admin css anchor missing'
    a=a.replace(css_admin_anchor,css_admin_add+css_admin_anchor,1)

more_anchor='<button class="moreCard" onclick="openPage(\'settings\',\'navMore\')"><strong>الإعدادات</strong><span>التوصيل والتحويل البنكي وحالة المتجر.</span></button>'
more_add=more_anchor+'\n<button class="moreCard" onclick="openPage(\'reviewsAdmin\',\'navMore\')"><strong>التقييمات والمراجعات</strong><span>عرض تقييمات الزبائن وإدارة المراجعات المنشورة.</span></button>'
if "openPage('reviewsAdmin'" not in a:
    assert more_anchor in a, 'admin more anchor missing'
    a=a.replace(more_anchor,more_add,1)

nav_anchor='<nav class="nav">'
section='<section id="reviewsAdmin" class="page"><div class="panel"><div class="sectionTitle"><h2>التقييمات والمراجعات</h2><span id="reviewAdminCount" class="count">0</span></div><p class="adminHint">هذه التقييمات ظاهرة للزبائن والزوار. يمكنك فتح المنتج أو حذف أي مراجعة غير مناسبة.</p><div id="reviewAdminList"></div></div></section>\n'
if 'id="reviewsAdmin"' not in a:
    assert nav_anchor in a, 'admin nav anchor missing'
    a=a.replace(nav_anchor,section+nav_anchor,1)

imp_old="import{getFirestore,collection,doc,addDoc,onSnapshot,serverTimestamp,writeBatch,setDoc,runTransaction}from'https://www.gstatic.com/firebasejs/12.16.0/firebase-firestore.js';"
imp_new="import{getFirestore,collection,doc,addDoc,onSnapshot,serverTimestamp,writeBatch,setDoc,runTransaction,deleteDoc}from'https://www.gstatic.com/firebasejs/12.16.0/firebase-firestore.js';"
if 'runTransaction,deleteDoc' not in a:
    assert imp_old in a, 'admin import anchor missing'
    a=a.replace(imp_old,imp_new,1)

state_admin_old="let pub=[],priv={},products=[],orders=[],suppliers=[],customers=[],customerAccounts=[],editingProductId='',started=false;"
state_admin_new="let pub=[],priv={},products=[],orders=[],suppliers=[],customers=[],customerAccounts=[],reviews=[],editingProductId='',started=false;"
if 'reviews=[]' not in a:
    assert state_admin_old in a, 'admin state anchor missing'
    a=a.replace(state_admin_old,state_admin_new,1)

start_old="onSnapshot(collection(db,'customerAccounts'),s=>{customerAccounts=s.docs.map(d=>({id:d.id,...d.data()}));render()},e=>console.warn('Customer accounts:',e.code||e.message))}"
start_new="onSnapshot(collection(db,'customerAccounts'),s=>{customerAccounts=s.docs.map(d=>({id:d.id,...d.data()}));render()},e=>console.warn('Customer accounts:',e.code||e.message));onSnapshot(collection(db,'productReviews'),s=>{reviews=s.docs.map(d=>({id:d.id,...d.data()}));render()},e=>console.warn('Product reviews:',e.code||e.message))}"
if "collection(db,'productReviews')" not in a:
    assert start_old in a, 'admin start anchor missing'
    a=a.replace(start_old,start_new,1)

func_before='function render(){const active='
funcs="function reviewProductName(r){const p=products.find(x=>String(x.id)===String(r.productId));return p?.name||r.productId||'منتج'}\nfunction reviewDateAdmin(v){return v?.seconds?new Date(v.seconds*1000).toLocaleString('ar'):'—'}\nfunction renderReviewsAdmin(){const box=$('reviewAdminList'),count=$('reviewAdminCount');if(!box)return;const rows=[...reviews].sort((x,y)=>(y.updatedAt?.seconds||y.createdAt?.seconds||0)-(x.updatedAt?.seconds||x.createdAt?.seconds||0));if(count)count.textContent=rows.length;box.innerHTML=rows.length?rows.map(r=>{const rating=Math.max(1,Math.min(5,Number(r.rating)||1)),productName=reviewProductName(r);return`<div class=\"reviewAdminCard\"><div class=\"reviewAdminHead\"><b>${esc(productName)}</b><span class=\"reviewAdminStars\">${'★'.repeat(rating)}${'☆'.repeat(5-rating)}</span></div>${r.text?`<div class=\"reviewAdminText\">${esc(r.text)}</div>`:'<div class=\"reviewAdminText muted\">بدون تعليق نصي.</div>'}<div class=\"reviewAdminMeta\">شراء موثّق • ${esc(reviewDateAdmin(r.updatedAt||r.createdAt))}<br>معرّف الزبون: <span dir=\"ltr\">${esc(r.uid||'—')}</span></div><div class=\"reviewAdminActions\"><a href=\"/?product=${encodeURIComponent(r.productId||'')}\" target=\"_blank\" onclick=\"event.preventDefault();window.open('/','_blank')\">فتح المتجر</a><button class=\"danger\" onclick=\"deleteReview('${esc(r.id)}')\">حذف المراجعة</button></div></div>`}).join(''):'<div class=\"empty\">لا توجد تقييمات بعد.</div>'}\nwindow.deleteReview=async id=>{const r=reviews.find(x=>String(x.id)===String(id));if(!r)return;if(!confirm('حذف هذه المراجعة نهائيًا؟'))return;try{await deleteDoc(doc(db,'productReviews',String(id)))}catch(e){alert('تعذر حذف المراجعة: '+(e.message||e))}};\n"
if 'function renderReviewsAdmin' not in a:
    assert func_before in a, 'admin render function anchor missing'
    a=a.replace(func_before,funcs+func_before,1)

render_end_old="$('productList').innerHTML=products.length?products.map(p=>"
# inject renderReviewsAdmin early in render after counts and before product rendering using a safe anchor
render_anchor="$('customerList').innerHTML=customerCards();$('productPageCount').textContent=products.length;"
render_new="$('customerList').innerHTML=customerCards();renderReviewsAdmin();$('productPageCount').textContent=products.length;"
if 'renderReviewsAdmin();' not in a:
    assert render_anchor in a, 'admin render call anchor missing'
    a=a.replace(render_anchor,render_new,1)

p.write_text(a,encoding='utf-8')
