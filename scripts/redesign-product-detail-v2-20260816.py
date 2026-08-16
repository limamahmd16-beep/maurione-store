from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Replace the product detail page with a cleaner commerce-first layout.
pattern=r'<main id="productDetailPage" class="page">.*?</main>\n<main id="categoriesPage"'
m=re.search(pattern,s,flags=re.S)
if not m:
    raise SystemExit('product detail page block not found')

new_detail='''<main id="productDetailPage" class="page"><div class="detail-page detail-v2"><div class="detail-topbar"><button class="detail-back" onclick="closeProduct()" aria-label="رجوع"><svg viewBox="0 0 24 24"><path d="m15 5-7 7 7 7"/></svg></button><div class="detail-topbrand"><div class="mark"><i class="a"></i><i class="b"></i></div><strong>Mauri<span>One</span></strong></div><button class="detail-topshare" onclick="shareProduct()" aria-label="مشاركة"><svg viewBox="0 0 24 24"><path d="M12 16V4M8 8l4-4 4 4M5 13v6h14v-6"/></svg></button></div><div class="detail-summary"><div id="detailCategory" class="detail-category"></div><h1 id="detailName"></h1><div id="detailMeta" class="detail-meta"></div><div class="detail-price-row"><div id="detailPrice" class="detail-price"></div><div id="detailStock" class="detail-stock"></div></div><button id="detailRatingJump" class="detail-rating-jump" onclick="document.getElementById('productReviews')?.scrollIntoView({behavior:'smooth',block:'start'})"><span id="detailRatingStars">☆</span><strong id="detailRatingQuick">لا توجد تقييمات بعد</strong><span>›</span></button></div><div class="detail-gallery"><div id="detailMain" class="detail-main"></div><div id="detailThumbs" class="detail-thumbs"></div></div><div class="detail-info"><div class="detail-specs"><div class="detail-spec"><small id="productBrandLabel">العلامة التجارية</small><strong id="detailBrand">—</strong></div><div class="detail-spec"><small id="productWarrantyLabel">الضمان</small><strong id="detailWarranty">—</strong></div></div><div class="detail-description"><h3 id="productDetailsTitle">تفاصيل المنتج</h3><p id="detailDescription"></p></div><div class="detail-secondary-actions"><button id="detailFavorite" class="detail-favorite" onclick="toggleFavorite(selectedProductId)">♡ حفظ في المفضلة</button><button id="detailShare" class="detail-share" onclick="shareProduct()">↗ مشاركة المنتج</button></div><section id="productReviews" class="review-section"><div class="review-head"><div><h3>تقييمات الزبائن</h3><div id="detailRatingCount" class="review-count">لا توجد تقييمات بعد</div></div><div class="review-score"><strong id="detailRatingAverage">—</strong><span>★</span></div></div><div id="reviewEligibility" class="review-eligibility">سجّل الدخول لعرض إمكانية كتابة تقييم موثّق.</div><div id="reviewComposer" class="review-composer"><strong>قيّم هذا المنتج</strong><div id="reviewStars" class="review-stars"><button class="review-star" onclick="setReviewRating(1)" aria-label="1 نجمة">★</button><button class="review-star" onclick="setReviewRating(2)" aria-label="2 نجمتان">★</button><button class="review-star" onclick="setReviewRating(3)" aria-label="3 نجوم">★</button><button class="review-star" onclick="setReviewRating(4)" aria-label="4 نجوم">★</button><button class="review-star" onclick="setReviewRating(5)" aria-label="5 نجوم">★</button></div><textarea id="reviewText" maxlength="1000" placeholder="اكتب تجربتك مع المنتج..."></textarea><button id="reviewSaveBtn" class="primary" onclick="saveProductReview()">نشر التقييم</button><div id="reviewStatus" class="notice" style="display:none"></div></div><div id="reviewsList" class="review-list"></div></section></div><div class="detail-buybar"><div><small>السعر</small><strong id="detailBuyPrice">—</strong></div><button id="detailAdd" class="detail-add" onclick="addDetailToCart()">أضف للسلة</button></div></div></main>\n<main id="categoriesPage"'''
s=s[:m.start()]+new_detail+s[m.end():]

# Add v2 detail styles before </style>.
css='''
/* MauriOne product detail v2 */
body.product-open{padding-bottom:92px;background:#f7f7f8}
body.product-open .bottom-nav{display:none}
body.product-open header{display:none}
.detail-v2{max-width:720px;margin:0 auto;padding:0 12px 118px;background:#f7f7f8;min-height:100vh}
.detail-topbar{height:64px;display:grid;grid-template-columns:42px 1fr 42px;align-items:center;gap:8px;position:sticky;top:0;z-index:25;background:rgba(247,247,248,.94);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)}
.detail-v2 .detail-back,.detail-topshare{width:40px;height:40px;margin:0;border:0;border-radius:50%;background:#fff;display:grid;place-items:center;box-shadow:0 3px 14px rgba(0,0,0,.05)}
.detail-v2 .detail-back svg,.detail-topshare svg{width:21px;height:21px;fill:none;stroke:#111;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.detail-topbrand{display:flex;align-items:center;justify-content:center;gap:6px;direction:ltr;font-size:14px}.detail-topbrand .mark{transform:scale(.72)}.detail-topbrand span{color:var(--gold)}
.detail-summary{background:#fff;border-radius:22px;padding:18px;margin-bottom:10px;border:1px solid #ececef}
.detail-v2 .detail-category{font-size:11px;color:var(--muted)}
.detail-v2 .detail-summary h1{font-size:24px;line-height:1.3;margin-top:5px;letter-spacing:-.25px}
.detail-v2 .detail-meta{font-size:11px;line-height:1.65;margin-top:7px;color:#777}
.detail-price-row{display:flex;justify-content:space-between;gap:12px;align-items:end;margin-top:15px}
.detail-v2 .detail-price{font-size:24px;font-weight:900;margin:0;direction:ltr;text-align:right}
.detail-v2 .detail-stock{font-size:10px;margin:0 0 3px;color:var(--green)}
.detail-rating-jump{width:100%;margin-top:13px;padding:10px 0 0;border:0;border-top:1px solid var(--line);background:transparent;display:flex;align-items:center;gap:7px;text-align:right;font-size:10px}.detail-rating-jump #detailRatingStars{color:var(--gold);font-size:16px}.detail-rating-jump strong{flex:1}.detail-rating-jump>span:last-child{font-size:19px;color:#aaa}
.detail-v2 .detail-gallery{background:#fff;border:1px solid #ececef;border-radius:22px;padding:10px;margin:0 0 10px}
.detail-v2 .detail-main{height:265px;border-radius:17px;background:#fafafa;overflow:hidden;display:grid;place-items:center}
.detail-v2 .detail-main img{width:100%;height:100%;object-fit:contain;background:#fafafa;transition:opacity .28s ease}
.detail-v2 .detail-thumbs{justify-content:center;margin-top:9px;padding:0 2px 2px;gap:7px}
.detail-v2 .detail-thumb{flex:0 0 54px;height:54px;border-radius:11px;background:#fafafa;border:1px solid #e9e9ec;padding:2px}
.detail-v2 .detail-thumb.active{border-color:var(--gold);box-shadow:0 0 0 1px var(--gold)}
.detail-v2 .detail-info{margin:0;background:#fff;border:1px solid #ececef;border-radius:22px;padding:16px}
.detail-v2 .detail-specs{margin-top:0;gap:9px}.detail-v2 .detail-spec{padding:12px;border-radius:13px}.detail-v2 .detail-spec small{font-size:9px}.detail-v2 .detail-spec strong{font-size:12px;margin-top:5px}
.detail-v2 .detail-description{margin-top:15px;padding-top:15px}.detail-v2 .detail-description h3{font-size:15px}.detail-v2 .detail-description p{font-size:11px;line-height:1.9}
.detail-secondary-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:15px}.detail-v2 .detail-favorite,.detail-v2 .detail-share{margin:0;padding:11px 8px;font-size:10px;border-radius:12px}
.detail-v2 .review-section{margin-top:18px;padding-top:17px}
.detail-buybar{position:fixed;left:0;right:0;bottom:0;z-index:160;background:rgba(255,255,255,.96);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-top:1px solid #e8e8eb;padding:10px 14px calc(10px + env(safe-area-inset-bottom));display:grid;grid-template-columns:auto minmax(180px,1fr);gap:12px;align-items:center;direction:rtl}
.detail-buybar>div{min-width:105px}.detail-buybar small{display:block;color:var(--muted);font-size:9px}.detail-buybar strong{display:block;margin-top:2px;font-size:14px;direction:ltr;text-align:right}.detail-v2 .detail-buybar .detail-add{margin:0;padding:13px 18px;border-radius:13px;font-size:13px}
@media(min-width:700px){.detail-buybar{left:50%;right:auto;width:720px;transform:translateX(-50%)}}
@media(max-width:390px){.detail-v2 .detail-main{height:235px}.detail-v2 .detail-summary h1{font-size:22px}.detail-v2 .detail-price{font-size:22px}}
'''
if '/* MauriOne product detail v2 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Ensure product page has its own app-like state and restore normal nav elsewhere.
old="window.openStore=(id,nav)=>{document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');document.querySelectorAll('.bottom-nav button').forEach(x=>x.classList.remove('active'));"
new="window.openStore=(id,nav)=>{document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');document.body.classList.toggle('product-open',id==='productDetailPage');document.querySelectorAll('.bottom-nav button').forEach(x=>x.classList.remove('active'));"
if old not in s:
    raise SystemExit('openStore anchor not found')
s=s.replace(old,new,1)

# Update the quick rating and sticky price whenever the product detail is rendered.
old_render="detailPrice.textContent=Number(p.price||0).toLocaleString()+' MRU';const available=Number(p.stock||0)>0;"
new_render="detailPrice.textContent=Number(p.price||0).toLocaleString()+' MRU';const buyPrice=document.getElementById('detailBuyPrice');if(buyPrice)buyPrice.textContent=Number(p.price||0).toLocaleString()+' MRU';const quick=productReviewSummary(p.id),quickText=document.getElementById('detailRatingQuick'),quickStars=document.getElementById('detailRatingStars');if(quickText)quickText.textContent=quick.count?quick.avg.toFixed(1)+' من 5 · '+quick.count+' تقييم':'لا توجد تقييمات بعد';if(quickStars)quickStars.textContent=quick.count?'★':'☆';const available=Number(p.stock||0)>0;"
if old_render not in s:
    raise SystemExit('renderProductDetail price anchor not found')
s=s.replace(old_render,new_render,1)

p.write_text(s,encoding='utf-8')
