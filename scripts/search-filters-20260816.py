from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# CSS
css_anchor='.field input,.field select{width:100%;padding:12px;border:1px solid var(--line);border-radius:10px;outline:0;background:#fff}'
css_add=css_anchor+'.search-controls{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}.search-control{border:1px solid var(--line);border-radius:11px;padding:10px;background:#fff}.search-control label{display:block;font-size:8px;color:var(--muted);margin-bottom:5px}.search-control select{width:100%;border:0;background:transparent;outline:0;font-size:10px}.stock-only{display:flex;align-items:center;gap:8px;min-height:50px;font-size:10px}.stock-only input{width:18px;height:18px}.search-result-meta{margin:0 15px 4px;color:var(--muted);font-size:9px}'
if '.search-controls{' not in s:
    assert css_anchor in s, 'css anchor missing'
    s=s.replace(css_anchor,css_add,1)

# Search UI
old='<main id="searchPage" class="page"><div class="page-head"><h1 id="searchTitle">البحث</h1><p id="searchSubtitle">ابحث عن المنتج الذي تريده.</p></div><div class="box"><div class="field"><input id="searchInput" placeholder="ابحث عن منتج..." oninput="renderSearch()"></div></div><div class="section" style="padding-top:5px"><div class="products" id="searchResults"></div></div></main>'
new='<main id="searchPage" class="page"><div class="page-head"><h1 id="searchTitle">البحث</h1><p id="searchSubtitle">ابحث عن المنتج الذي تريده.</p></div><div class="box"><div class="field"><input id="searchInput" placeholder="ابحث عن منتج..." oninput="renderSearch()"></div><div class="search-controls"><div class="search-control"><label>ترتيب المنتجات</label><select id="searchSort" onchange="renderSearch()"><option value="newest">الأحدث</option><option value="priceAsc">السعر: الأقل أولًا</option><option value="priceDesc">السعر: الأعلى أولًا</option><option value="rating">الأعلى تقييمًا</option></select></div><label class="search-control stock-only"><input id="searchStockOnly" type="checkbox" onchange="renderSearch()"> المتوفر فقط</label></div></div><div id="searchResultsCount" class="search-result-meta"></div><div class="section" style="padding-top:5px"><div class="products" id="searchResults"></div></div></main>'
if 'id="searchSort"' not in s:
    assert old in s, 'search html anchor missing'
    s=s.replace(old,new,1)

# Reset filters when opening search/all/categories
old_open="window.openSearch=()=>{categoryFilter='';searchInput.value='';searchTitle.textContent=ct('searchPageTitle');searchSubtitle.textContent=ct('searchPageSubtitle');openStore('searchPage','navSearch');renderSearch();setTimeout(()=>searchInput.focus(),100)};"
new_open="window.openSearch=()=>{categoryFilter='';searchInput.value='';const sort=document.getElementById('searchSort'),stock=document.getElementById('searchStockOnly');if(sort)sort.value='newest';if(stock)stock.checked=false;searchTitle.textContent=ct('searchPageTitle');searchSubtitle.textContent=ct('searchPageSubtitle');openStore('searchPage','navSearch');renderSearch();setTimeout(()=>searchInput.focus(),100)};"
if new_open not in s:
    assert old_open in s, 'openSearch anchor missing'
    s=s.replace(old_open,new_open,1)

old_all="window.showAllProducts=()=>{categoryFilter='';searchInput.value='';searchTitle.textContent=ct('allProductsTitle');searchSubtitle.textContent=ct('allProductsSubtitle');openStore('searchPage','navSearch');renderSearch()};"
new_all="window.showAllProducts=()=>{categoryFilter='';searchInput.value='';const sort=document.getElementById('searchSort'),stock=document.getElementById('searchStockOnly');if(sort)sort.value='newest';if(stock)stock.checked=false;searchTitle.textContent=ct('allProductsTitle');searchSubtitle.textContent=ct('allProductsSubtitle');openStore('searchPage','navSearch');renderSearch()};"
if new_all not in s:
    assert old_all in s, 'showAllProducts anchor missing'
    s=s.replace(old_all,new_all,1)

old_cat="window.filterCategory=cat=>{categoryFilter=cat;searchInput.value='';searchTitle.textContent=displayCategory(cat);searchSubtitle.textContent=tpl('categoryResultsTemplate',{category:displayCategory(cat)});openStore('searchPage','navSearch');renderSearch()};"
new_cat="window.filterCategory=cat=>{categoryFilter=cat;searchInput.value='';const sort=document.getElementById('searchSort'),stock=document.getElementById('searchStockOnly');if(sort)sort.value='newest';if(stock)stock.checked=false;searchTitle.textContent=displayCategory(cat);searchSubtitle.textContent=tpl('categoryResultsTemplate',{category:displayCategory(cat)});openStore('searchPage','navSearch');renderSearch()};"
if new_cat not in s:
    assert old_cat in s, 'filterCategory anchor missing'
    s=s.replace(old_cat,new_cat,1)

# Replace renderSearch
old_render="window.renderSearch=()=>{const q=searchInput.value.trim().toLowerCase();searchResults.innerHTML=cards(products.filter(p=>(!categoryFilter||p.category===categoryFilter)&&(!q||String(p.name||'').toLowerCase().includes(q)||String(p.category||'').toLowerCase().includes(q)||String(p.meta||'').toLowerCase().includes(q))))};"
new_render="window.renderSearch=()=>{const q=searchInput.value.trim().toLowerCase(),stockOnly=document.getElementById('searchStockOnly')?.checked===true,sort=document.getElementById('searchSort')?.value||'newest';let list=products.filter(p=>(!categoryFilter||p.category===categoryFilter)&&(!q||String(p.name||'').toLowerCase().includes(q)||String(p.category||'').toLowerCase().includes(q)||String(p.meta||'').toLowerCase().includes(q)));if(stockOnly)list=list.filter(p=>Number(p.stock||0)>0);list=[...list];if(sort==='priceAsc')list.sort((a,b)=>Number(a.price||0)-Number(b.price||0));else if(sort==='priceDesc')list.sort((a,b)=>Number(b.price||0)-Number(a.price||0));else if(sort==='rating')list.sort((a,b)=>{const rb=productReviewSummary(b.id),ra=productReviewSummary(a.id);return rb.avg-ra.avg||rb.count-ra.count});else list.sort((a,b)=>(b.createdAt?.seconds||0)-(a.createdAt?.seconds||0));const meta=document.getElementById('searchResultsCount');if(meta)meta.textContent=list.length+' منتج';searchResults.innerHTML=cards(list)};"
if new_render not in s:
    assert old_render in s, 'renderSearch anchor missing'
    s=s.replace(old_render,new_render,1)

p.write_text(s,encoding='utf-8')
