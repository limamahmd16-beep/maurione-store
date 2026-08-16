from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old_gallery='<div class="detail-gallery"><div id="detailMain" class="detail-main"></div><div id="detailThumbs" class="detail-thumbs"></div></div>'
new_gallery='''<div class="detail-gallery"><div class="detail-stage"><button id="detailPrev" class="detail-arrow prev" onclick="stepProductImage(-1)" aria-label="الصورة السابقة">‹</button><div id="detailMain" class="detail-main" onclick="openProductImage()" title="اضغط لعرض الصورة كاملة"></div><button id="detailNext" class="detail-arrow next" onclick="stepProductImage(1)" aria-label="الصورة التالية">›</button></div><div id="detailThumbs" class="detail-thumbs"></div></div>'''
if old_gallery not in s:
    raise SystemExit('detail gallery anchor not found')
s=s.replace(old_gallery,new_gallery,1)

viewer='''<div id="productImageViewer" class="image-viewer" onclick="imageViewerBackdrop(event)" aria-hidden="true"><button class="image-viewer-close" onclick="closeProductImage()" aria-label="إغلاق">×</button><button id="viewerPrev" class="image-viewer-arrow prev" onclick="stepViewerImage(-1)" aria-label="الصورة السابقة">‹</button><div class="image-viewer-stage"><img id="productViewerImage" alt="صورة المنتج كاملة"></div><button id="viewerNext" class="image-viewer-arrow next" onclick="stepViewerImage(1)" aria-label="الصورة التالية">›</button><div id="productViewerCount" class="image-viewer-count"></div></div>'''
anchor='<a id="whatsappSupport"'
if 'id="productImageViewer"' not in s:
    if anchor not in s:
        raise SystemExit('viewer insertion anchor not found')
    s=s.replace(anchor,viewer+anchor,1)

css='''
/* MauriOne product gallery v5 */
.detail-stage{position:relative;border-radius:14px;overflow:hidden;background:#fff}
.detail-v2 .detail-main{cursor:zoom-in;background:#fff!important}
.detail-v2 .detail-main img{width:100%!important;height:100%!important;object-fit:contain!important;object-position:center!important;background:#fff!important;display:block}
.detail-arrow{display:none;position:absolute;top:50%;transform:translateY(-50%);z-index:7;width:36px;height:36px;border:1px solid rgba(0,0,0,.08);border-radius:50%;background:rgba(255,255,255,.94);box-shadow:0 4px 18px rgba(0,0,0,.13);font-size:27px;line-height:1;align-items:center;justify-content:center;padding:0}
.detail-arrow.show{display:flex}.detail-arrow.prev{left:9px}.detail-arrow.next{right:9px}
.detail-v2 .detail-thumbs{scrollbar-width:none}.detail-v2 .detail-thumbs::-webkit-scrollbar{display:none}
.detail-v2 .detail-thumb img{width:100%;height:100%;object-fit:contain;background:#fff}
.image-viewer{display:none;position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,.96);align-items:center;justify-content:center;padding:calc(64px + env(safe-area-inset-top)) 16px calc(58px + env(safe-area-inset-bottom));direction:ltr}
.image-viewer.open{display:flex}.image-viewer-stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center;overflow:hidden;touch-action:pinch-zoom}
.image-viewer-stage img{display:block;max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;user-select:none;-webkit-user-select:none}
.image-viewer-close{position:absolute;top:calc(12px + env(safe-area-inset-top));right:14px;z-index:4;width:42px;height:42px;border:0;border-radius:50%;background:rgba(255,255,255,.14);color:#fff;font-size:30px;line-height:1}
.image-viewer-arrow{display:none;position:absolute;top:50%;transform:translateY(-50%);z-index:4;width:44px;height:44px;border:0;border-radius:50%;background:rgba(255,255,255,.16);color:#fff;font-size:32px;line-height:1;align-items:center;justify-content:center}.image-viewer-arrow.show{display:flex}.image-viewer-arrow.prev{left:12px}.image-viewer-arrow.next{right:12px}
.image-viewer-count{position:absolute;bottom:calc(16px + env(safe-area-inset-bottom));left:50%;transform:translateX(-50%);padding:6px 11px;border-radius:20px;background:rgba(255,255,255,.13);color:#fff;font-size:11px;direction:ltr}
@media(max-width:390px){.detail-arrow{width:34px;height:34px}.image-viewer-arrow{width:40px;height:40px}}
'''
if '/* MauriOne product gallery v5 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

old_select="window.selectProductImage=i=>{selectedProductImage=Number(i)||0;renderProductDetail()};"
new_select="""function detailImages(){const p=products.find(x=>String(x.id)===String(selectedProductId));return Array.isArray(p?.images)?p.images.filter(Boolean):[]}\nfunction displayProductImage(url){const v=String(url||'');if(!v.includes('res.cloudinary.com')||!v.includes('/image/upload/'))return v;return v.includes('/image/upload/f_auto,q_auto:best/')?v:v.replace('/image/upload/','/image/upload/f_auto,q_auto:best/')}\nfunction syncImageViewer(){const imgs=detailImages(),viewer=document.getElementById('productImageViewer'),img=document.getElementById('productViewerImage'),count=document.getElementById('productViewerCount'),prev=document.getElementById('viewerPrev'),next=document.getElementById('viewerNext');if(!viewer||!img||!imgs.length)return;img.src=displayProductImage(imgs[selectedProductImage]||imgs[0]);if(count)count.textContent=(selectedProductImage+1)+' / '+imgs.length;const many=imgs.length>1;prev?.classList.toggle('show',many);next?.classList.toggle('show',many)}\nwindow.selectProductImage=i=>{const imgs=detailImages();if(!imgs.length)return;selectedProductImage=Math.max(0,Math.min(imgs.length-1,Number(i)||0));renderProductDetail();if(document.getElementById('productImageViewer')?.classList.contains('open'))syncImageViewer()};\nwindow.stepProductImage=d=>{const imgs=detailImages();if(imgs.length<2)return;selectedProductImage=(selectedProductImage+Number(d||0)+imgs.length)%imgs.length;renderProductDetail()};\nwindow.openProductImage=()=>{const imgs=detailImages(),viewer=document.getElementById('productImageViewer');if(!imgs.length||!viewer)return;viewer.classList.add('open');viewer.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';syncImageViewer()};\nwindow.closeProductImage=()=>{const viewer=document.getElementById('productImageViewer');if(!viewer)return;viewer.classList.remove('open');viewer.setAttribute('aria-hidden','true');document.body.style.overflow=''};\nwindow.imageViewerBackdrop=e=>{if(e.target?.id==='productImageViewer')closeProductImage()};\nwindow.stepViewerImage=d=>{const imgs=detailImages();if(imgs.length<2)return;selectedProductImage=(selectedProductImage+Number(d||0)+imgs.length)%imgs.length;renderProductDetail();syncImageViewer()};\ndocument.addEventListener('keydown',e=>{const open=document.getElementById('productImageViewer')?.classList.contains('open');if(!open)return;if(e.key==='Escape')closeProductImage();else if(e.key==='ArrowLeft')stepViewerImage(-1);else if(e.key==='ArrowRight')stepViewerImage(1)});"""
if old_select not in s:
    raise SystemExit('selectProductImage anchor not found')
s=s.replace(old_select,new_select,1)

old_imgs="const imgs=Array.isArray(p.images)?p.images.filter(Boolean):[];if(selectedProductImage>=imgs.length)selectedProductImage=0;"
new_imgs="const imgs=Array.isArray(p.images)?p.images.filter(Boolean):[];if(selectedProductImage>=imgs.length)selectedProductImage=0;const manyImages=imgs.length>1;document.getElementById('detailPrev')?.classList.toggle('show',manyImages);document.getElementById('detailNext')?.classList.toggle('show',manyImages);"
if old_imgs not in s:
    raise SystemExit('render image list anchor not found')
s=s.replace(old_imgs,new_imgs,1)

s=s.replace("detailMain.innerHTML=`<img src=\"${esc(imgs[selectedProductImage])}\" alt=\"${esc(p.name||'')}\">`","detailMain.innerHTML=`<img src=\"${esc(displayProductImage(imgs[selectedProductImage]))}\" alt=\"${esc(p.name||'')}\">`",1)
s=s.replace("<img src=\"${esc(u)}\" alt=\"\">","<img src=\"${esc(displayProductImage(u))}\" alt=\"\">",1)

p.write_text(s,encoding='utf-8')
