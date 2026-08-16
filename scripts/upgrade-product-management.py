from pathlib import Path
import re

p = Path('admin.html')
s = p.read_text(encoding='utf-8')

# CSS for product management
css_anchor = ".customerStat{background:#f6f6f8;border-radius:9px;padding:7px 9px;font-size:9px}"
css_add = css_anchor + ".productManageHead{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}.productManageMeta{margin-top:8px;display:grid;grid-template-columns:1fr 1fr;gap:7px}.productManageMeta div{background:#f6f6f8;border-radius:10px;padding:8px;font-size:9px}.productManageMeta small{display:block;color:#888;font-size:8px;margin-bottom:3px}.productState{display:inline-flex;padding:4px 8px;border-radius:20px;background:#edf8f1;color:#168247;font-size:8px;font-weight:900;white-space:nowrap}.productState.off{background:#fff0f0;color:#a42020}.productActions{display:grid;grid-template-columns:1fr 1fr 1fr;gap:7px;margin-top:11px}.manageBtn{border:1px solid #ddd;background:#fff;border-radius:10px;padding:9px 6px;font-size:9px}.manageBtn.danger{color:#b42318;border-color:#f1c7c3}.editBadge{font-size:8px;padding:5px 8px;border-radius:20px;background:#f5f5f7;color:#666}.editBadge.on{background:#fff4d9;color:#8d5d00}"
if '.productActions{' not in s:
    if css_anchor not in s:
        raise SystemExit('CSS anchor not found')
    s = s.replace(css_anchor, css_add, 1)

# Product form heading / edit state
old = '<section id="products" class="page"><div class="panel"><h2>تسجيل منتج</h2><div class="grid">'
new = '<section id="products" class="page"><div class="panel"><div class="sectionTitle"><h2 id="productFormTitle">تسجيل منتج</h2><span id="productEditBadge" class="editBadge">وضع الإضافة</span></div><div class="grid">'
if old in s:
    s = s.replace(old, new, 1)
elif 'id="productFormTitle"' not in s:
    raise SystemExit('Product section heading anchor not found')

old = '<button id="saveProduct" class="primary">حفظ المنتج</button></div><div class="panel"><h2>المنتجات الحالية</h2>'
new = '<button id="saveProduct" class="primary">حفظ المنتج</button><button id="cancelProductEdit" class="secondary" style="display:none;margin-top:8px" onclick="cancelProductEdit()">إلغاء التعديل</button></div><div class="panel"><div class="sectionTitle"><h2>المنتجات الحالية</h2><span id="productPageCount" class="count">0</span></div><p class="adminHint">اضغط «تعديل» لتغيير السعر أو المخزون أو الصور أو الوصف. يمكنك إخفاء المنتج من المتجر بدون حذفه.</p>'
if old in s:
    s = s.replace(old, new, 1)
elif 'id="cancelProductEdit"' not in s:
    raise SystemExit('Save button anchor not found')

# State
old = 'let pub=[],priv={},products=[],orders=[],suppliers=[],customers=[],customerAccounts=[],started=false;'
new = 'let pub=[],priv={},products=[],orders=[],suppliers=[],customers=[],customerAccounts=[],editingProductId=\'\',started=false;'
if old in s:
    s = s.replace(old, new, 1)
elif 'editingProductId=' not in s:
    raise SystemExit('State anchor not found')

# Insert product management helpers before profit()
helper_anchor = 'function profit(){'
helpers = r'''function clearProductForm(){editingProductId='';$('productFormTitle').textContent='تسجيل منتج';$('productEditBadge').textContent='وضع الإضافة';$('productEditBadge').className='editBadge';$('saveProduct').textContent='حفظ المنتج';$('cancelProductEdit').style.display='none';$('pName').value='';$('pCat').selectedIndex=0;$('pSup').value='';$('pCost').value='';$('pPrice').value='';$('pStock').value='1';$('pMin').value='2';$('pMeta').value='';$('pBrand').value='';$('pWarranty').value='';$('pDescription').value='';$('pImages').value='';$('preview').innerHTML='';$('uploadMsg').textContent='';profit()}
window.cancelProductEdit=()=>clearProductForm();
window.editProduct=id=>{const p=products.find(x=>String(x.id)===String(id));if(!p)return;editingProductId=String(id);$('productFormTitle').textContent='تعديل المنتج';$('productEditBadge').textContent='وضع التعديل';$('productEditBadge').className='editBadge on';$('saveProduct').textContent='حفظ التعديلات';$('cancelProductEdit').style.display='block';$('pName').value=p.name||'';$('pCat').value=p.category||'الهواتف';$('pSup').value=p.supplierId||'';$('pCost').value=Number(p.cost||0);$('pPrice').value=Number(p.price||0);$('pStock').value=Number(p.stock||0);$('pMin').value=Number(p.min||0);$('pMeta').value=p.meta||'';$('pBrand').value=p.brand||'';$('pWarranty').value=p.warranty||'';$('pDescription').value=p.description||'';$('pImages').value='';$('preview').innerHTML=(Array.isArray(p.images)?p.images:[]).map(u=>`<img src="${esc(u)}">`).join('');$('uploadMsg').textContent=(p.images?.length||0)?'الصور الحالية — اختر صورًا جديدة فقط إذا أردت استبدالها بالكامل.':'';profit();openPage('products','navProducts');setTimeout(()=>scrollTo({top:0,behavior:'smooth'}),30)};
window.toggleProduct=async id=>{const p=products.find(x=>String(x.id)===String(id));if(!p)return;const next=p.active===false;try{const b=writeBatch(db);b.update(doc(db,'products',String(id)),{active:next,updatedAt:serverTimestamp()});await b.commit()}catch(e){alert('تعذر تغيير ظهور المنتج: '+(e.message||e))}};
window.deleteProduct=async id=>{const p=products.find(x=>String(x.id)===String(id));if(!p)return;const hasOpenOrder=orders.some(o=>o.status!=='delivered'&&o.status!=='cancelled'&&(Array.isArray(o.items)?o.items:[]).some(i=>String(i.productId||'')===String(id)));if(hasOpenOrder)return alert('لا يمكن حذف هذا المنتج لأن هناك طلبًا حاليًا مرتبطًا به. يمكنك إخفاؤه من المتجر بدلًا من الحذف.');if(!confirm(`حذف «${p.name||'المنتج'}» نهائيًا من المنتجات؟`))return;try{const b=writeBatch(db);b.delete(doc(db,'products',String(id)));b.delete(doc(db,'product_private',String(id)));await b.commit();if(editingProductId===String(id))clearProductForm()}catch(e){alert('تعذر حذف المنتج: '+(e.message||e))}};
'''
if 'window.editProduct=' not in s:
    if helper_anchor not in s:
        raise SystemExit('profit anchor not found')
    s = s.replace(helper_anchor, helpers + helper_anchor, 1)

# Replace save product handler
pattern = re.compile(r"\$\('saveProduct'\)\.onclick=async\(\)=>\{.*?\};\n\$\('saveSupplier'\)", re.S)
new_handler = r'''$('saveProduct').onclick=async()=>{const name=$('pName').value.trim(),price=Number($('pPrice').value||0);if(!name||price<=0)return alert('أدخل الاسم وسعر البيع');const fs=[...$('pImages').files];if(fs.length>6)return alert('الحد الأقصى 6 صور');const cost=Number($('pCost').value||0),sid=$('pSup').value,sup=suppliers.find(x=>x.id===sid),btn=$('saveProduct');btn.disabled=true;try{let images=[];if(fs.length)images=await upload(fs);else if(editingProductId){const current=pub.find(x=>String(x.id)===String(editingProductId));images=Array.isArray(current?.images)?current.images:[]}const publicData={name,category:$('pCat').value,meta:$('pMeta').value.trim(),brand:$('pBrand').value.trim(),warranty:$('pWarranty').value.trim(),description:$('pDescription').value.trim(),price,stock:Math.max(0,Number($('pStock').value||0)),min:Math.max(0,Number($('pMin').value||0)),images,updatedAt:serverTimestamp()};if(editingProductId){const id=editingProductId,current=pub.find(x=>String(x.id)===String(id)),b=writeBatch(db);b.set(doc(db,'products',id),{...publicData,active:current?.active!==false},{merge:true});b.set(doc(db,'product_private',id),{cost,supplierId:sid,supplierName:sup?.name||'',updatedAt:serverTimestamp()},{merge:true});await b.commit();alert('تم تحديث المنتج بنجاح');clearProductForm()}else{const ref=doc(collection(db,'products')),b=writeBatch(db);b.set(ref,{...publicData,active:true,createdAt:serverTimestamp()});b.set(doc(db,'product_private',ref.id),{cost,supplierId:sid,supplierName:sup?.name||'',createdAt:serverTimestamp(),updatedAt:serverTimestamp()});await b.commit();alert('تم حفظ المنتج');clearProductForm()}}catch(e){alert(e.message||e)}finally{btn.disabled=false}};
$('saveSupplier')'''
if pattern.search(s):
    s = pattern.sub(new_handler, s, count=1)
elif "alert('تم تحديث المنتج بنجاح')" not in s:
    raise SystemExit('saveProduct handler not found')

# Replace product list renderer with controls
old_expr = "$('productList').innerHTML=products.map(p=>`<div class=\"card\">${p.images?.[0]?`<img class=\"thumb\" src=\"${esc(p.images[0])}\">`:''}<br><b>${esc(p.name)}</b><br>سعر البيع: ${Number(p.price||0).toLocaleString()} MRU<br>المخزون: ${Number(p.stock||0)}</div>`).join('')||'لا توجد منتجات.'"
new_expr = "$('productPageCount').textContent=products.length;$('productList').innerHTML=products.length?products.map(p=>`<div class=\"card\"><div class=\"productManageHead\"><div style=\"display:flex;gap:9px;align-items:center\">${p.images?.[0]?`<img class=\"thumb\" src=\"${esc(p.images[0])}\">`:'<div class=\"thumb\"></div>'}<div><b>${esc(p.name)}</b><div class=\"muted\" style=\"margin-top:4px\">${esc(p.category||'—')} • ${esc(p.brand||'بدون علامة')}</div></div></div><span class=\"productState ${p.active===false?'off':''}\">${p.active===false?'مخفي':'ظاهر'}</span></div><div class=\"productManageMeta\"><div><small>سعر البيع</small><b>${Number(p.price||0).toLocaleString()} MRU</b></div><div><small>سعر الشراء</small><b>${Number(p.cost||0).toLocaleString()} MRU</b></div><div><small>المخزون</small><b>${Number(p.stock||0)}</b></div><div><small>المورد</small><b>${esc(p.supplierName||'بدون مورد')}</b></div></div><div class=\"productActions\"><button class=\"manageBtn\" onclick=\"editProduct('${esc(p.id)}')\">تعديل</button><button class=\"manageBtn\" onclick=\"toggleProduct('${esc(p.id)}')\">${p.active===false?'إظهار':'إخفاء'}</button><button class=\"manageBtn danger\" onclick=\"deleteProduct('${esc(p.id)}')\">حذف</button></div></div>`).join(''):'<div class=\"empty\">لا توجد منتجات.</div>'"
if old_expr in s:
    s = s.replace(old_expr, new_expr, 1)
elif 'productActions' not in s[s.find('function render(){'):]:
    raise SystemExit('product list renderer anchor not found')

p.write_text(s, encoding='utf-8')
print('Product management upgrade applied')
