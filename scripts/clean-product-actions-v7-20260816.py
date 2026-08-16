from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# 1) Keep only one share action on the product page: the gallery action.
old_top='''<button class="detail-topshare" onclick="shareProduct()" aria-label="مشاركة"><svg viewBox="0 0 24 24"><path d="M12 16V4M8 8l4-4 4 4M5 13v6h14v-6"/></svg></button>'''
if old_top in s:
    s=s.replace(old_top,'<span aria-hidden="true"></span>',1)

# 2) Remove duplicate favorite/share actions below product details.
old_secondary='''<div class="detail-secondary-actions"><button id="detailFavorite" class="detail-favorite" onclick="toggleFavorite(selectedProductId)">♡ حفظ في المفضلة</button><button id="detailShare" class="detail-share" onclick="shareProduct()">↗ مشاركة المنتج</button></div>'''
if old_secondary in s:
    s=s.replace(old_secondary,'',1)

# 3) Move Add to cart directly under the ad summary/rating, before product images.
old_summary_end='''<button id="detailRatingJump" class="detail-rating-jump" onclick="document.getElementById('productReviews')?.scrollIntoView({behavior:'smooth',block:'start'})"><span id="detailRatingStars">☆</span><strong id="detailRatingQuick">لا توجد تقييمات بعد</strong><span>›</span></button></div><div class="detail-gallery amazon-gallery">'''
new_summary_end='''<button id="detailRatingJump" class="detail-rating-jump" onclick="document.getElementById('productReviews')?.scrollIntoView({behavior:'smooth',block:'start'})"><span id="detailRatingStars">☆</span><strong id="detailRatingQuick">لا توجد تقييمات بعد</strong><span>›</span></button><button id="detailAdd" class="detail-add detail-inline-add" onclick="addDetailToCart()">أضف للسلة</button></div><div class="detail-gallery amazon-gallery">'''
if old_summary_end not in s:
    raise SystemExit('summary insertion anchor not found')
s=s.replace(old_summary_end,new_summary_end,1)

# 4) Remove the fixed purchase bar; price already appears in the ad summary.
old_buy='''<div class="detail-buybar"><div><small>السعر</small><strong id="detailBuyPrice">—</strong></div><button id="detailAdd" class="detail-add" onclick="addDetailToCart()">أضف للسلة</button></div>'''
if old_buy not in s:
    raise SystemExit('fixed buy bar anchor not found')
s=s.replace(old_buy,'',1)

css='''
/* MauriOne product actions v7 — single actions + inline cart */
body.product-open{padding-bottom:82px!important}
.detail-v2{padding-bottom:105px!important}
.detail-topbar{grid-template-columns:42px 1fr 42px}
.detail-inline-add{width:100%;margin:12px 0 0!important;padding:13px 16px!important;border:0!important;border-radius:12px!important;background:#111!important;color:#fff!important;font-size:13px!important;font-weight:700!important}
.detail-inline-add:disabled{opacity:.45}
.detail-buybar{display:none!important}
'''
if '/* MauriOne product actions v7 — single actions + inline cart */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

p.write_text(s,encoding='utf-8')
