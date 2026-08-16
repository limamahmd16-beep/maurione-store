from pathlib import Path

index_path = Path('index.html')
rules_path = Path('firestore.rules')
index = index_path.read_text(encoding='utf-8')
rules = rules_path.read_text(encoding='utf-8')

if 'id="productReviews"' not in index:
    css = '''\n.review-section{margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}.review-head{display:flex;justify-content:space-between;align-items:center;gap:12px}.review-head h3{font-size:16px}.review-score{display:flex;align-items:center;gap:6px}.review-score strong{font-size:19px}.review-score span{color:var(--gold);font-size:17px}.review-count{font-size:9px;color:var(--muted);margin-top:3px}.review-eligibility{margin-top:12px;padding:10px 12px;border-radius:11px;background:var(--soft);font-size:9px;color:var(--muted);line-height:1.7}.review-composer{display:none;margin-top:12px;padding:13px;border:1px solid var(--line);border-radius:14px;background:#fff}.review-composer.show{display:block}.review-stars{display:flex;gap:4px;direction:ltr;margin:8px 0 10px}.review-star{border:0;background:transparent;font-size:27px;color:#c7c7ca;padding:0 2px}.review-star.on{color:var(--gold)}.review-composer textarea{width:100%;min-height:92px;resize:vertical;padding:11px;border:1px solid var(--line);border-radius:11px;outline:0}.review-list{margin-top:13px}.review-card{padding:13px 0;border-top:1px solid var(--line)}.review-card:first-child{border-top:0}.review-card-head{display:flex;justify-content:space-between;gap:10px;align-items:center}.review-card-stars{color:var(--gold);font-size:13px;direction:ltr}.verified-badge{font-size:8px;font-weight:800;color:var(--green);background:#edf8f1;border-radius:20px;padding:5px 8px}.review-card p{margin-top:8px;font-size:10px;line-height:1.8;color:#444;white-space:pre-wrap}.review-card small{display:block;margin-top:7px;color:var(--muted);font-size:8px}.review-empty{padding:16px 0;text-align:center;color:var(--muted);font-size:10px}\n'''
    index = index.replace('</style>', css + '</style>', 1)

    old_detail = '''<button id="detailFavorite" class="detail-favorite" onclick="toggleFavorite(selectedProductId)">♡ حفظ في المفضلة</button><button id="detailAdd" class="detail-add" onclick="addDetailToCart()">أضف للسلة</button></div></div></main>'''
    new_detail = '''<button id="detailFavorite" class="detail-favorite" onclick="toggleFavorite(selectedProductId)">♡ حفظ في المفضلة</button><button id="detailAdd" class="detail-add" onclick="addDetailToCart()">أضف للسلة</button><section id="productReviews" class="review-section"><div class="review-head"><div><h3>تقييمات الزبائن</h3><div id="detailRatingCount" class="review-count">لا توجد تقييمات بعد</div></div><div class="review-score"><strong id="detailRatingAverage">—</strong><span>★</span></div></div><div id="reviewEligibility" class="review-eligibility">سجّل الدخول لعرض إمكانية كتابة تقييم موثّق.</div><div id="reviewComposer" class="review-composer"><strong>قيّم هذا المنتج</strong><div id="reviewStars" class="review-stars"><button class="review-star" onclick="setReviewRating(1)" aria-label="1 نجمة">★</button><button class="review-star" onclick="setReviewRating(2)" aria-label="2 نجمتان">★</button><button class="review-star" onclick="setReviewRating(3)" aria-label="3 نجوم">★</button><button class="review-star" onclick="setReviewRating(4)" aria-label="4 نجوم">★</button><button class="review-star" onclick="setReviewRating(5)" aria-label="5 نجوم">★</button></div><textarea id="reviewText" maxlength="1000" placeholder="اكتب تجربتك مع المنتج..."></textarea><button id="reviewSaveBtn" class="primary" onclick="saveProductReview()">نشر التقييم</button><div id="reviewStatus" class="notice" style="display:none"></div></div><div id="reviewsList" class="review-list"></div></section></div></div></main>'''
    if old_detail not in index:
        raise SystemExit('detail marker not found')
    index = index.replace(old_detail, new_detail, 1)

    old_import = "import { getFirestore, collection, onSnapshot, doc, serverTimestamp, setDoc, query, where, runTransaction } from 'https://www.gstatic.com/firebasejs/12.16.0/firebase-firestore.js';"
    new_import = "import { getFirestore, collection, onSnapshot, doc, serverTimestamp, setDoc, getDoc, query, where, runTransaction } from 'https://www.gstatic.com/firebasejs/12.16.0/firebase-firestore.js';"
    if old_import not in index:
        raise SystemExit('firestore import marker not found')
    index = index.replace(old_import, new_import, 1)

    old_state = "let orderHistory=[],currentUser=null,customerOrdersUnsub=null,customerProfileUnsub=null,favoritesUnsub=null,favoriteIds=[],favoriteWriteBusy=false;"
    new_state = "let orderHistory=[],currentUser=null,customerOrdersUnsub=null,customerProfileUnsub=null,favoritesUnsub=null,favoriteIds=[],favoriteWriteBusy=false,reviewUnsub=null,reviewRows=[],reviewRating=0,reviewProductId='',reviewSaveBusy=false;"
    if old_state not in index:
        raise SystemExit('state marker not found')
    index = index.replace(old_state, new_state, 1)

    old_open = "window.openProduct=id=>{selectedProductId=String(id);selectedProductImage=0;renderProductDetail();openStore('productDetailPage','navHome')};"
    new_open = "window.openProduct=id=>{selectedProductId=String(id);selectedProductImage=0;reviewRating=0;watchProductReviews(selectedProductId);renderProductDetail();openStore('productDetailPage','navHome')};"
    if old_open not in index:
        raise SystemExit('open product marker not found')
    index = index.replace(old_open, new_open, 1)

    marker = 'function renderStore(){productList.innerHTML=cards(products);renderSearch();renderFavorites();updateBadge();if(selectedProductId)renderProductDetail()}'
    if marker not in index:
        raise SystemExit('renderStore marker not found')

    review_js = r'''function deliveredOrderForProduct(productId){const pid=String(productId||'');return orderHistory.find(o=>o.status==='delivered'&&(((o.inventory&&Number(o.inventory[pid]||0)>0))||(Array.isArray(o.items)&&o.items.some(i=>String(i.productId||'')===pid))))||null}
function ownReviewForProduct(productId){return reviewRows.find(r=>r.uid===currentUser?.uid&&String(r.productId)===String(productId))||null}
function reviewDate(v){if(!v)return '';if(v?.seconds)return new Date(v.seconds*1000).toLocaleDateString('ar');return ''}
function renderReviewStars(){document.querySelectorAll('#reviewStars .review-star').forEach((b,i)=>b.classList.toggle('on',i<reviewRating))}
window.setReviewRating=n=>{reviewRating=Math.max(1,Math.min(5,Number(n)||1));renderReviewStars()};
function renderReviews(){const avgEl=document.getElementById('detailRatingAverage'),countEl=document.getElementById('detailRatingCount'),listEl=document.getElementById('reviewsList'),elig=document.getElementById('reviewEligibility'),composer=document.getElementById('reviewComposer'),textEl=document.getElementById('reviewText');if(!avgEl||!countEl||!listEl||!elig||!composer)return;const pid=String(selectedProductId||'');const rows=reviewRows.filter(r=>String(r.productId)===pid);const avg=rows.length?rows.reduce((s,r)=>s+Number(r.rating||0),0)/rows.length:0;avgEl.textContent=rows.length?avg.toFixed(1):'—';countEl.textContent=rows.length?`${rows.length} تقييم موثّق`:'لا توجد تقييمات بعد';const sorted=[...rows].sort((a,b)=>(b.updatedAt?.seconds||b.createdAt?.seconds||0)-(a.updatedAt?.seconds||a.createdAt?.seconds||0));listEl.innerHTML=sorted.length?sorted.map(r=>`<div class="review-card"><div class="review-card-head"><span class="review-card-stars">${'★'.repeat(Math.max(1,Math.min(5,Number(r.rating)||1)))}${'☆'.repeat(5-Math.max(1,Math.min(5,Number(r.rating)||1)))}</span><span class="verified-badge">شراء موثّق</span></div>${r.text?`<p>${esc(r.text)}</p>`:''}<small>${r.uid===currentUser?.uid?'تقييمك • ':''}${esc(reviewDate(r.updatedAt||r.createdAt))}</small></div>`).join(''):'<div class="review-empty">لا توجد مراجعات لهذا المنتج حتى الآن.</div>';if(!currentUser){elig.textContent='سجّل الدخول إلى MauriOne لكتابة تقييم بعد استلام المنتج.';composer.classList.remove('show');return}const order=deliveredOrderForProduct(pid);if(!order){elig.textContent='يمكن كتابة التقييم بعد أن تصبح حالة طلب هذا المنتج «تم التسليم».';composer.classList.remove('show');return}elig.textContent='✓ شراء موثّق — يمكنك كتابة أو تعديل تقييمك لهذا المنتج.';composer.classList.add('show');const own=ownReviewForProduct(pid);if(own&&reviewRating===0){reviewRating=Number(own.rating||0);if(textEl)textEl.value=own.text||''}renderReviewStars()}
function watchProductReviews(productId){if(reviewUnsub){try{reviewUnsub()}catch{}reviewUnsub=null}reviewRows=[];reviewProductId=String(productId||'');renderReviews();if(!reviewProductId)return;const pid=reviewProductId,qReviews=query(collection(db,'productReviews'),where('productId','==',pid));reviewUnsub=onSnapshot(qReviews,snap=>{if(String(selectedProductId)!==pid)return;reviewRows=snap.docs.map(d=>({id:d.id,...d.data()}));renderReviews()},e=>{console.warn('Product reviews:',e.code||e.message);reviewRows=[];renderReviews()})}
window.saveProductReview=async()=>{const pid=String(selectedProductId||'');const status=document.getElementById('reviewStatus'),btn=document.getElementById('reviewSaveBtn'),textEl=document.getElementById('reviewText');if(!currentUser)return;if(!reviewRating){status.style.display='block';status.className='notice';status.textContent='اختر عدد النجوم أولًا.';return}const delivered=deliveredOrderForProduct(pid);if(!delivered){status.style.display='block';status.className='notice';status.textContent='يمكن التقييم فقط بعد استلام المنتج.';return}if(reviewSaveBusy)return;reviewSaveBusy=true;btn.disabled=true;status.style.display='block';status.className='notice';status.textContent='جاري حفظ التقييم...';try{const ref=doc(db,'productReviews',currentUser.uid+'_'+pid),snap=await getDoc(ref),existing=snap.exists()?snap.data():null;const payload={uid:currentUser.uid,productId:pid,orderId:existing?.orderId||delivered.id,rating:Number(reviewRating),text:String(textEl?.value||'').trim().slice(0,1000),createdAt:existing?.createdAt||serverTimestamp(),updatedAt:serverTimestamp()};await setDoc(ref,payload);status.className='notice success';status.textContent='تم حفظ تقييمك.'}catch(e){console.error('Review save:',e);status.className='notice';status.textContent=e?.code==='permission-denied'?'يجب نشر قواعد Firestore الخاصة بالتقييمات أولًا.':'تعذر حفظ التقييم. حاول مرة أخرى.'}finally{reviewSaveBusy=false;btn.disabled=false}};
'''
    index = index.replace(marker, review_js + marker, 1)

    old_orders = "orderHistory=snap.docs.map(d=>({id:d.id,...d.data()})).sort((a,b)=>(b.createdAt?.seconds||0)-(a.createdAt?.seconds||0));renderMyOrders();connectTracking()"
    new_orders = "orderHistory=snap.docs.map(d=>({id:d.id,...d.data()})).sort((a,b)=>(b.createdAt?.seconds||0)-(a.createdAt?.seconds||0));renderMyOrders();connectTracking();renderReviews()"
    if old_orders not in index:
        raise SystemExit('orders callback marker not found')
    index = index.replace(old_orders, new_orders, 1)

    old_auth = "watchCustomerProfile();watchFavorites();watchCustomerOrders();if(document.getElementById('accountPage')?.classList.contains('active'))loadAccount()"
    new_auth = "watchCustomerProfile();watchFavorites();watchCustomerOrders();renderReviews();if(document.getElementById('accountPage')?.classList.contains('active'))loadAccount()"
    if old_auth not in index:
        raise SystemExit('auth marker not found')
    index = index.replace(old_auth, new_auth, 1)

    index_path.write_text(index, encoding='utf-8')

if 'match /productReviews/{reviewId}' not in rules:
    function_marker = '''    function validTrackingOrder(trackingId, orderNo) {
      let order = getAfter(
        /databases/$(database)/documents/orders/$(trackingId)
      ).data;

      return signedIn()
        && order.customerUid == request.auth.uid
        && order.orderNo == orderNo;
    }
'''
    review_function = function_marker + '''
    function validReviewPurchase(orderId, productId) {
      let order = get(
        /databases/$(database)/documents/orders/$(orderId)
      ).data;

      return signedIn()
        && order.customerUid == request.auth.uid
        && order.status == 'delivered'
        && order.inventory is map
        && order.inventory.get(productId, 0) > 0;
    }
'''
    if function_marker not in rules:
        raise SystemExit('rules function marker not found')
    rules = rules.replace(function_marker, review_function, 1)

    rules_marker = '''    match /categories/{categoryId} {
      allow read: if true;
      allow write: if isAdmin();
    }
'''
    review_rules = '''    match /productReviews/{reviewId} {
      allow read: if true;

      allow create: if signedIn()
        && request.resource.data.keys().hasAll([
          'uid',
          'productId',
          'orderId',
          'rating',
          'text',
          'createdAt',
          'updatedAt'
        ])
        && request.resource.data.keys().hasOnly([
          'uid',
          'productId',
          'orderId',
          'rating',
          'text',
          'createdAt',
          'updatedAt'
        ])
        && request.resource.data.uid == request.auth.uid
        && request.resource.data.productId is string
        && request.resource.data.productId.size() > 0
        && request.resource.data.productId.size() <= 200
        && request.resource.data.orderId is string
        && request.resource.data.orderId.size() > 0
        && request.resource.data.orderId.size() <= 200
        && reviewId == request.auth.uid + '_' + request.resource.data.productId
        && request.resource.data.rating is int
        && request.resource.data.rating >= 1
        && request.resource.data.rating <= 5
        && request.resource.data.text is string
        && request.resource.data.text.size() <= 1000
        && request.resource.data.createdAt == request.time
        && request.resource.data.updatedAt == request.time
        && validReviewPurchase(
          request.resource.data.orderId,
          request.resource.data.productId
        );

      allow update: if signedIn()
        && resource.data.uid == request.auth.uid
        && request.resource.data.keys().hasOnly([
          'uid',
          'productId',
          'orderId',
          'rating',
          'text',
          'createdAt',
          'updatedAt'
        ])
        && request.resource.data.uid == resource.data.uid
        && request.resource.data.productId == resource.data.productId
        && request.resource.data.orderId == resource.data.orderId
        && reviewId == request.auth.uid + '_' + resource.data.productId
        && request.resource.data.rating is int
        && request.resource.data.rating >= 1
        && request.resource.data.rating <= 5
        && request.resource.data.text is string
        && request.resource.data.text.size() <= 1000
        && request.resource.data.createdAt == resource.data.createdAt
        && request.resource.data.updatedAt == request.time
        && validReviewPurchase(
          resource.data.orderId,
          resource.data.productId
        );

      allow delete: if isAdmin()
        || (signedIn() && resource.data.uid == request.auth.uid);
    }

''' + rules_marker
    if rules_marker not in rules:
        raise SystemExit('rules categories marker not found')
    rules = rules.replace(rules_marker, review_rules, 1)
    rules_path.write_text(rules, encoding='utf-8')

print('product reviews patch applied')
