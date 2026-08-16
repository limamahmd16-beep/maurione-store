from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old='''<div class="detail-gallery"><div class="detail-stage"><button id="detailPrev" class="detail-arrow prev" onclick="stepProductImage(-1)" aria-label="الصورة السابقة">‹</button><div id="detailMain" class="detail-main" onclick="openProductImage()" title="اضغط لعرض الصورة كاملة"></div><button id="detailNext" class="detail-arrow next" onclick="stepProductImage(1)" aria-label="الصورة التالية">›</button></div><div id="detailThumbs" class="detail-thumbs"></div></div>'''
new='''<div class="detail-gallery amazon-gallery"><div class="amazon-stage"><div id="detailMain" class="detail-main amazon-main" onclick="openProductImage()" title="اضغط لعرض الصورة كاملة"></div></div><div class="amazon-gallery-bottom"><div class="amazon-actions"><button class="amazon-icon-btn" onclick="shareProduct()" aria-label="مشاركة المنتج"><svg viewBox="0 0 24 24"><path d="M12 16V4M8 8l4-4 4 4M5 13v6h14v-6"/></svg></button><button id="galleryFavorite" class="amazon-icon-btn amazon-heart" onclick="toggleFavorite(selectedProductId)" aria-label="المفضلة">♡</button></div><div id="detailDots" class="detail-dots" aria-label="صور المنتج"></div></div><div id="detailThumbs" class="detail-thumbs" hidden></div></div>'''
if old not in s:
    raise SystemExit('gallery v5 anchor not found')
s=s.replace(old,new,1)

css='''
/* MauriOne product gallery v6 — Amazon-style mobile carousel */
.amazon-gallery{padding:0 12px 8px!important;background:#fff;border:1px solid #ececef!important;border-radius:18px!important;overflow:hidden}
.amazon-stage{height:clamp(330px,52vh,520px);display:flex;align-items:center;justify-content:center;background:#fff;overflow:hidden;touch-action:pan-y pinch-zoom}
.amazon-main{width:100%!important;height:100%!important;border-radius:0!important;background:#fff!important;display:flex!important;align-items:center!important;justify-content:center!important;overflow:hidden!important;cursor:zoom-in}
.amazon-main img{display:block!important;width:auto!important;height:auto!important;max-width:100%!important;max-height:100%!important;object-fit:contain!important;object-position:center!important;background:#fff!important}
.amazon-gallery .detail-thumbs{display:none!important}
.amazon-gallery-bottom{position:relative;min-height:52px;display:flex;align-items:center;justify-content:center;padding:6px 4px 2px;direction:ltr}
.amazon-actions{position:absolute;left:2px;display:flex;align-items:center;gap:14px}
.amazon-icon-btn{width:36px;height:36px;border:0;background:transparent;display:grid;place-items:center;padding:0;color:#111}
.amazon-icon-btn svg{width:25px;height:25px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.amazon-heart{font-size:31px;line-height:1;font-family:Arial,sans-serif}
.amazon-heart.on{color:#b4233a}
.detail-dots{display:flex;align-items:center;justify-content:center;gap:9px;min-height:24px;direction:ltr}
.detail-dot{width:8px;height:8px;border:0;border-radius:50%;background:#b9bbc0;padding:0;transition:transform .18s ease,background .18s ease}
.detail-dot.active{background:var(--navy);transform:scale(1.18)}
.detail-dot:only-child{display:none}
@media(max-width:390px){.amazon-stage{height:clamp(310px,49vh,440px)}.amazon-actions{gap:10px}.amazon-icon-btn{width:34px;height:34px}.amazon-icon-btn svg{width:23px;height:23px}.amazon-heart{font-size:29px}.detail-dots{gap:8px}}
'''
if '/* MauriOne product gallery v6 — Amazon-style mobile carousel */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

needle="const manyImages=imgs.length>1;document.getElementById('detailPrev')?.classList.toggle('show',manyImages);document.getElementById('detailNext')?.classList.toggle('show',manyImages);"
repl=needle+"const dots=document.getElementById('detailDots');if(dots)dots.innerHTML=imgs.length>1?imgs.map((_,i)=>`<button class=\"detail-dot ${i===selectedProductImage?'active':''}\" onclick=\"selectProductImage(${i})\" aria-label=\"الصورة ${i+1}\"></button>`).join(''):'';"
if needle not in s:
    raise SystemExit('render dots anchor not found')
s=s.replace(needle,repl,1)

favneedle="if(fav){const on=isFavorite(p.id);fav.textContent=on?'♥ محفوظ في المفضلة':'♡ حفظ في المفضلة';fav.className='detail-favorite'+(on?' on':'')}"
favrepl=favneedle+"const galleryFav=document.getElementById('galleryFavorite');if(galleryFav){const on=isFavorite(p.id);galleryFav.textContent=on?'♥':'♡';galleryFav.className='amazon-icon-btn amazon-heart'+(on?' on':'')}"
if favneedle not in s:
    raise SystemExit('favorite sync anchor not found')
s=s.replace(favneedle,favrepl,1)

old_display="function displayProductImage(url){const v=String(url||'');if(!v.includes('res.cloudinary.com')||!v.includes('/image/upload/'))return v;return v.includes('/image/upload/f_auto,q_auto:best/')?v:v.replace('/image/upload/','/image/upload/f_auto,q_auto:best/')}"
new_display="function displayProductImage(url){const v=String(url||'');if(!v.includes('res.cloudinary.com')||!v.includes('/image/upload/'))return v;if(v.includes('/image/upload/f_auto,q_auto:best,dpr_auto,w_1600,c_limit/'))return v;return v.replace('/image/upload/','/image/upload/f_auto,q_auto:best,dpr_auto,w_1600,c_limit/')}"
if old_display not in s:
    raise SystemExit('Cloudinary display function anchor not found')
s=s.replace(old_display,new_display,1)

old_open="window.openProductImage=()=>{const imgs=detailImages(),viewer=document.getElementById('productImageViewer');if(!imgs.length||!viewer)return;viewer.classList.add('open');viewer.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';syncImageViewer()};"
new_open="window.openProductImage=()=>{if(gallerySwiped){gallerySwiped=false;return}const imgs=detailImages(),viewer=document.getElementById('productImageViewer');if(!imgs.length||!viewer)return;viewer.classList.add('open');viewer.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';syncImageViewer()};"
if old_open not in s:
    raise SystemExit('fullscreen open anchor not found')
s=s.replace(old_open,new_open,1)

anchor="window.stepViewerImage=d=>{const imgs=detailImages();if(imgs.length<2)return;selectedProductImage=(selectedProductImage+Number(d||0)+imgs.length)%imgs.length;renderProductDetail();syncImageViewer()};"
swipe='''\nlet galleryTouchX=0,galleryTouchY=0,gallerySwiped=false,viewerTouchX=0,viewerTouchY=0;\nconst galleryEl=document.getElementById('detailMain');\ngalleryEl?.addEventListener('touchstart',e=>{const t=e.changedTouches?.[0];if(!t)return;galleryTouchX=t.clientX;galleryTouchY=t.clientY;gallerySwiped=false},{passive:true});\ngalleryEl?.addEventListener('touchend',e=>{const t=e.changedTouches?.[0];if(!t)return;const dx=t.clientX-galleryTouchX,dy=t.clientY-galleryTouchY;if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)*1.15){gallerySwiped=true;stepProductImage(dx<0?1:-1)}},{passive:true});\nconst viewerStage=document.querySelector('.image-viewer-stage');\nviewerStage?.addEventListener('touchstart',e=>{const t=e.changedTouches?.[0];if(!t)return;viewerTouchX=t.clientX;viewerTouchY=t.clientY},{passive:true});\nviewerStage?.addEventListener('touchend',e=>{const t=e.changedTouches?.[0];if(!t)return;const dx=t.clientX-viewerTouchX,dy=t.clientY-viewerTouchY;if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)*1.15)stepViewerImage(dx<0?1:-1)},{passive:true});\n'''
if anchor not in s:
    raise SystemExit('viewer step anchor not found')
s=s.replace(anchor,anchor+swipe,1)

p.write_text(s,encoding='utf-8')
