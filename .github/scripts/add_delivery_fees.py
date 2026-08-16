from pathlib import Path


def must_replace(text, old, new, label, count=1):
    if old not in text:
        raise SystemExit(f'Missing pattern: {label}')
    return text.replace(old, new, count)

# ---------- admin.html ----------
admin_path = Path('admin.html')
admin = admin_path.read_text(encoding='utf-8')

old_settings = '''<section id="settings" class="page"><div class="panel"><h2>إعدادات المتجر</h2><div class="field"><label>مدينة التوصيل الافتراضية</label><input id="setDeliveryCity" placeholder="نواكشوط"></div><div class="field"><label>اسم البنك للتحويل</label><input id="setBankName"></div><div class="field"><label>اسم صاحب الحساب</label><input id="setBankHolder"></div><div class="field"><label>رقم الحساب / IBAN</label><input id="setBankAccount"></div><div class="field"><label>حالة المتجر</label><select id="setMaintenance"><option value="false">مفتوح</option><option value="true">وضع الصيانة</option></select></div><button class="primary" onclick="saveGeneralSettings()">حفظ الإعدادات</button><div id="settingsMsg" class="ok"></div></div></section>'''
new_settings = '''<section id="settings" class="page"><div class="panel"><h2>إعدادات المتجر</h2><div class="field"><label>مدينة التوصيل الافتراضية</label><input id="setDeliveryCity" placeholder="نواكشوط"></div><h3 style="font-size:14px;margin:18px 0 8px">رسوم التوصيل</h3><p class="adminHint">ضع سعرًا افتراضيًا، ثم أضف المدن أو المناطق الخاصة كل واحدة في سطر بالشكل: تفرغ زينة = 120</p><div class="field"><label>رسوم التوصيل الافتراضية (MRU)</label><input id="setDeliveryDefaultFee" type="number" min="0" step="1" value="0"></div><div class="field"><label>رسوم حسب المدينة / المنطقة</label><textarea id="setDeliveryRates" placeholder="تفرغ زينة = 120&#10;عرفات = 100&#10;لكصر = 90"></textarea></div><div class="field"><label>اسم البنك للتحويل</label><input id="setBankName"></div><div class="field"><label>اسم صاحب الحساب</label><input id="setBankHolder"></div><div class="field"><label>رقم الحساب / IBAN</label><input id="setBankAccount"></div><div class="field"><label>حالة المتجر</label><select id="setMaintenance"><option value="false">مفتوح</option><option value="true">وضع الصيانة</option></select></div><button class="primary" onclick="saveGeneralSettings()">حفظ الإعدادات</button><div id="settingsMsg" class="ok"></div></div></section>'''
admin = must_replace(admin, old_settings, new_settings, 'admin settings section')

old_load = "onSnapshot(doc(db,'storeSettings','general'),s=>{const d=s.data()||{};fill('setDeliveryCity',d.deliveryCity||'نواكشوط');fill('setBankName',d.bankName||'');fill('setBankHolder',d.bankHolder||'');fill('setBankAccount',d.bankAccount||'');fill('setMaintenance',String(d.maintenance===true))});"
new_load = "onSnapshot(doc(db,'storeSettings','general'),s=>{const d=s.data()||{};fill('setDeliveryCity',d.deliveryCity||'نواكشوط');fill('setDeliveryDefaultFee',Number(d.deliveryDefaultFee||0));fill('setDeliveryRates',Object.entries(d.deliveryRates||{}).map(([k,v])=>k+' = '+v).join('\\n'));fill('setBankName',d.bankName||'');fill('setBankHolder',d.bankHolder||'');fill('setBankAccount',d.bankAccount||'');fill('setMaintenance',String(d.maintenance===true))});"
admin = must_replace(admin, old_load, new_load, 'admin settings load')

old_save = "window.saveGeneralSettings=async()=>{try{await setDoc(doc(db,'storeSettings','general'),{deliveryCity:$('setDeliveryCity').value.trim(),bankName:$('setBankName').value.trim(),bankHolder:$('setBankHolder').value.trim(),bankAccount:$('setBankAccount').value.trim(),maintenance:$('setMaintenance').value==='true',updatedAt:serverTimestamp()},{merge:true});$('settingsMsg').textContent='تم حفظ إعدادات المتجر.'}catch(e){$('settingsMsg').textContent='تعذر الحفظ: '+e.message}};"
new_save = "function parseDeliveryRates(){const out={};String($('setDeliveryRates').value||'').split(/\\n+/).forEach(line=>{const m=line.split(/=|:/);if(m.length<2)return;const name=m.shift().trim(),fee=Number(m.join(':').trim());if(name&&Number.isFinite(fee)&&fee>=0)out[name]=fee});return out}window.saveGeneralSettings=async()=>{try{await setDoc(doc(db,'storeSettings','general'),{deliveryCity:$('setDeliveryCity').value.trim(),deliveryDefaultFee:Math.max(0,Number($('setDeliveryDefaultFee').value||0)),deliveryRates:parseDeliveryRates(),bankName:$('setBankName').value.trim(),bankHolder:$('setBankHolder').value.trim(),bankAccount:$('setBankAccount').value.trim(),maintenance:$('setMaintenance').value==='true',updatedAt:serverTimestamp()},{merge:true});$('settingsMsg').textContent='تم حفظ إعدادات المتجر ورسوم التوصيل.'}catch(e){$('settingsMsg').textContent='تعذر الحفظ: '+e.message}};"
admin = must_replace(admin, old_save, new_save, 'admin settings save')

checkout_admin_marker = '<h4>إثبات التحويل</h4>'
checkout_admin_insert = '''<h4>الإجماليات والتوصيل</h4><div class="grid"><div class="field"><label>إجمالي المنتجات</label><input id="ctSubtotalLabel" value="إجمالي المنتجات"></div><div class="field"><label>رسوم التوصيل</label><input id="ctDeliveryFeeLabel" value="رسوم التوصيل"></div><div class="field"><label>رسوم التوصيل قبل إدخال المدينة</label><input id="ctDeliveryAtCheckoutText" value="تُحسب رسوم التوصيل بعد إدخال المدينة."></div><div class="field"><label>التوصيل المجاني</label><input id="ctFreeDeliveryText" value="مجاني"></div></div><h4>إثبات التحويل</h4>'''
admin = must_replace(admin, checkout_admin_marker, checkout_admin_insert, 'admin content delivery fields')

content_field_marker = "['ctConfirmOrderText', 'confirmOrderText', 'تأكيد الطلب'], ['ctBankInfoEmptyMessage'"
content_field_repl = "['ctConfirmOrderText', 'confirmOrderText', 'تأكيد الطلب'], ['ctSubtotalLabel', 'subtotalLabel', 'إجمالي المنتجات'], ['ctDeliveryFeeLabel', 'deliveryFeeLabel', 'رسوم التوصيل'], ['ctDeliveryAtCheckoutText', 'deliveryAtCheckoutText', 'تُحسب رسوم التوصيل بعد إدخال المدينة.'], ['ctFreeDeliveryText', 'freeDeliveryText', 'مجاني'], ['ctBankInfoEmptyMessage'"
admin = must_replace(admin, content_field_marker, content_field_repl, 'admin content field registry')

order_totals_old = '<div class="row"><span>طريقة الدفع</span><b>${esc(pay(o.payment))}</b></div><div class="row"><span>الإجمالي</span><b>${Number(o.total||0).toLocaleString()} MRU</b></div>'
order_totals_new = '<div class="row"><span>طريقة الدفع</span><b>${esc(pay(o.payment))}</b></div><div class="row"><span>إجمالي المنتجات</span><b>${Number(o.subtotal??o.total||0).toLocaleString()} MRU</b></div><div class="row"><span>رسوم التوصيل</span><b>${Number(o.deliveryFee||0).toLocaleString()} MRU</b></div><div class="row"><span>الإجمالي</span><b>${Number(o.total||0).toLocaleString()} MRU</b></div>'
admin = must_replace(admin, order_totals_old, order_totals_new, 'admin order totals')

admin_path.write_text(admin, encoding='utf-8')

# ---------- index.html ----------
index_path = Path('index.html')
index = index_path.read_text(encoding='utf-8')

css_marker = '.proof-preview img{display:block;width:100%;max-height:220px;object-fit:contain;background:#fff}'
css_repl = css_marker + '.costs{margin:12px 0;padding:12px;border:1px solid var(--line);border-radius:13px;background:var(--soft)}.cost-row{display:flex;justify-content:space-between;gap:12px;padding:5px 0;font-size:10px}.cost-row.total{border-top:1px solid var(--line);margin-top:5px;padding-top:10px;font-size:13px;font-weight:900}.delivery-note{margin-top:7px;font-size:9px;color:var(--muted);line-height:1.6}'
index = must_replace(index, css_marker, css_repl, 'store delivery CSS')

old_cart_summary = '<div class="summary" id="cartSummary"><div style="display:flex;justify-content:space-between"><span id="cartTotalLabel">الإجمالي</span><strong id="cartTotal">0 MRU</strong></div><button class="primary" id="checkoutBtn" onclick="checkout()">إتمام الطلب</button></div>'
new_cart_summary = '<div class="summary" id="cartSummary"><div style="display:flex;justify-content:space-between"><span id="cartSubtotalLabel">إجمالي المنتجات</span><strong id="cartSubtotal">0 MRU</strong></div><div id="deliveryAtCheckoutText" class="delivery-note">تُحسب رسوم التوصيل بعد إدخال المدينة.</div><button class="primary" id="checkoutBtn" onclick="checkout()">إتمام الطلب</button></div>'
index = must_replace(index, old_cart_summary, new_cart_summary, 'cart summary')

old_city = '<div class="field"><label id="checkoutCityLabel">المدينة</label><input id="coCity"></div><div class="field"><label id="checkoutAddressLabel">العنوان</label><input id="coAddress"></div><div class="field"><label id="paymentLabel">طريقة الدفع</label>'
new_city = '<div class="field"><label id="checkoutCityLabel">المدينة / المنطقة</label><input id="coCity" oninput="updateCheckoutTotals()"></div><div class="field"><label id="checkoutAddressLabel">العنوان</label><input id="coAddress"></div><div class="costs"><div class="cost-row"><span id="coSubtotalLabel">إجمالي المنتجات</span><strong id="coSubtotal">0 MRU</strong></div><div class="cost-row"><span id="coDeliveryFeeLabel">رسوم التوصيل</span><strong id="coDeliveryFee">0 MRU</strong></div><div class="cost-row total"><span id="coGrandTotalLabel">الإجمالي</span><strong id="coGrandTotal">0 MRU</strong></div></div><div class="field"><label id="paymentLabel">طريقة الدفع</label>'
index = must_replace(index, old_city, new_city, 'checkout delivery totals')

# Content defaults
index = must_replace(index, '"cartTotalLabel":"الإجمالي","checkoutButton"', '"cartTotalLabel":"الإجمالي","subtotalLabel":"إجمالي المنتجات","deliveryFeeLabel":"رسوم التوصيل","deliveryAtCheckoutText":"تُحسب رسوم التوصيل بعد إدخال المدينة.","freeDeliveryText":"مجاني","checkoutButton"', 'content delivery defaults')

map_marker = "['cartTotalLabel','cartTotalLabel'],['checkoutBtn','checkoutButton']"
map_repl = "['cartSubtotalLabel','subtotalLabel'],['deliveryAtCheckoutText','deliveryAtCheckoutText'],['checkoutBtn','checkoutButton'],['coSubtotalLabel','subtotalLabel'],['coDeliveryFeeLabel','deliveryFeeLabel'],['coGrandTotalLabel','cartTotalLabel']"
index = must_replace(index, map_marker, map_repl, 'content delivery map')

# General settings function
start = index.find('function applyGeneralSettings(d={}){')
end = index.find('\nfunction applyLanguageSettings', start)
if start < 0 or end < 0:
    raise SystemExit('Missing applyGeneralSettings block')
new_general = '''function normalizeZone(v){return String(v||'').trim().toLocaleLowerCase('ar').replace(/\\s+/g,' ')}
function deliveryFeeForCity(city){const target=normalizeZone(city),rates=generalSettings.deliveryRates||{};if(target){for(const [name,fee] of Object.entries(rates)){if(normalizeZone(name)===target)return Math.max(0,Number(fee||0))}}return Math.max(0,Number(generalSettings.deliveryDefaultFee||0))}
function applyGeneralSettings(d={}){generalSettings=d;const info=document.getElementById('bankTransferInfo');if(info){const parts=[];if(d.bankName)parts.push('البنك: '+d.bankName);if(d.bankHolder)parts.push('اسم الحساب: '+d.bankHolder);if(d.bankAccount)parts.push('رقم الحساب: '+d.bankAccount);info.textContent=parts.length?parts.join(' • '):ct('bankInfoEmptyMessage')}if(typeof window.updateCheckoutTotals==='function')window.updateCheckoutTotals()}'''
index = index[:start] + new_general + index[end:]

# renderCart and helpers
start = index.find('function renderCart(){')
end = index.find('\nwindow.changeQty=', start)
if start < 0 or end < 0:
    raise SystemExit('Missing renderCart block')
new_render_cart = '''function cartSubtotalValue(){return cartRows().reduce((s,{p,qty})=>s+Number(p.price||0)*qty,0)}
function money(v){return Number(v||0).toLocaleString()+' MRU'}
function renderCart(){const rows=cartRows();cartList.innerHTML=rows.length?rows.map(({p,qty})=>`<div class="cart-row"><div><strong>${esc(p.name)}</strong><br><small>${Number(p.price||0).toLocaleString()} MRU × ${qty}</small></div><div class="cart-actions"><button class="qty-btn" onclick="changeQty('${esc(p.id)}',1)">+</button><strong>${qty}</strong><button class="qty-btn" onclick="changeQty('${esc(p.id)}',-1)">−</button><button class="remove-btn" onclick="removeCart('${esc(p.id)}')">×</button></div></div>`).join(''):esc(ct('emptyCartMessage'));cartSubtotal.textContent=money(cartSubtotalValue());checkoutBtn.disabled=!rows.length}
window.updateCheckoutTotals=()=>{const subtotal=cartSubtotalValue(),fee=deliveryFeeForCity(document.getElementById('coCity')?.value||''),total=subtotal+fee;const a=document.getElementById('coSubtotal'),b=document.getElementById('coDeliveryFee'),c=document.getElementById('coGrandTotal');if(a)a.textContent=money(subtotal);if(b)b.textContent=fee>0?money(fee):ct('freeDeliveryText');if(c)c.textContent=money(total)};'''
index = index[:start] + new_render_cart + index[end:]

# Checkout opening
old_checkout = "window.checkout=()=>{if(generalSettings.maintenance===true)return alert(ct('maintenanceMessage'));if(!cartRows().length)return alert(ct('cartEmptyAlert'));if(!currentUser){openStore('accountPage','navAccount');setTimeout(()=>alert(ct('loginRequiredMessage')),80);return}const a=account();coName.value=a.name||'';coPhone.value=a.phone||'';coCity.value=a.city||generalSettings.deliveryCity||'';coAddress.value=a.address||'';coPayment.value='cod';coProof.value='';coProofPreview.innerHTML='';coProofPreview.classList.remove('show');transferProofField.classList.remove('show');checkoutStatus.style.display='none';placeOrderBtn.style.display='block';placeOrderBtn.disabled=false;placeOrderBtn.textContent=ct('confirmOrderText');document.getElementById('checkoutOverlay').classList.add('open')};"
new_checkout = "window.checkout=()=>{if(generalSettings.maintenance===true)return alert(ct('maintenanceMessage'));if(!cartRows().length)return alert(ct('cartEmptyAlert'));if(!currentUser){openStore('accountPage','navAccount');setTimeout(()=>alert(ct('loginRequiredMessage')),80);return}const a=account();coName.value=a.name||'';coPhone.value=a.phone||'';coCity.value=a.city||generalSettings.deliveryCity||'';coAddress.value=a.address||'';coPayment.value='cod';coProof.value='';coProofPreview.innerHTML='';coProofPreview.classList.remove('show');transferProofField.classList.remove('show');checkoutStatus.style.display='none';placeOrderBtn.style.display='block';placeOrderBtn.disabled=false;placeOrderBtn.textContent=ct('confirmOrderText');updateCheckoutTotals();document.getElementById('checkoutOverlay').classList.add('open')};"
index = must_replace(index, old_checkout, new_checkout, 'checkout open')

# placeOrder block
start = index.find('window.placeOrder=async()=>{')
end = index.find("\nonSnapshot(doc(db,'storeSettings'", start)
if start < 0 or end < 0:
    raise SystemExit('Missing placeOrder block')
new_place_order = '''window.placeOrder=async()=>{const rows=cartRows();if(!rows.length)return;if(!currentUser){openStore('accountPage','navAccount');return}const customer={name:coName.value.trim(),phone:coPhone.value.trim(),city:coCity.value.trim(),address:coAddress.value.trim()};if(!customer.name||!customer.phone||!customer.address){checkoutStatus.style.display='block';checkoutStatus.className='notice';checkoutStatus.textContent=ct('requiredFieldsMessage');return}const isTransfer=coPayment.value==='transfer',proofFile=coProof.files?.[0]||null;if(isTransfer&&!proofFile){checkoutStatus.style.display='block';checkoutStatus.className='notice';checkoutStatus.textContent=ct('proofRequiredMessage');return}const items=rows.map(({p,qty})=>({productId:String(p.id),name:String(p.name||''),price:Number(p.price||0),qty:Number(qty||1),image:Array.isArray(p.images)&&p.images[0]?String(p.images[0]):''})),inventory={};if(items.length>6){checkoutStatus.style.display='block';checkoutStatus.className='notice';checkoutStatus.textContent=ct('maxProductsMessage');return}items.forEach(i=>inventory[i.productId]=i.qty);const subtotal=items.reduce((sum,x)=>sum+x.price*x.qty,0),deliveryFee=deliveryFeeForCity(customer.city),total=subtotal+deliveryFee,orderNo='MO-'+String(Date.now()).slice(-6);updateCheckoutTotals();placeOrderBtn.disabled=true;placeOrderBtn.textContent=isTransfer?ct('orderUploadingProofMessage'):ct('orderCheckingStockMessage');try{const paymentProofUrl=isTransfer?await uploadPaymentProof(proofFile):'';placeOrderBtn.textContent=ct('orderReservingMessage');const orderRef=doc(collection(db,'orders')),trackingRef=doc(db,'orderTracking',orderRef.id),productRefs=items.map(i=>doc(db,'products',i.productId)),reservationRows=items.map(i=>{const id=orderRef.id+'_'+i.productId;return{id,ref:doc(db,'inventoryReservations',id),item:i}});await runTransaction(db,async tx=>{const snaps=[];for(const ref of productRefs)snaps.push(await tx.get(ref));const updates=[];for(let i=0;i<items.length;i++){const item=items[i],snap=snaps[i];if(!snap.exists())throw new Error('STOCK|'+item.name+'|0');const available=Number(snap.data().stock||0);if(!Number.isFinite(available)||available<item.qty)throw new Error('STOCK|'+item.name+'|'+Math.max(0,available||0));updates.push({ref:productRefs[i],stock:available-item.qty})}tx.set(orderRef,{orderNo,customerUid:currentUser.uid,customerEmail:currentUser.email||'',customer,items,subtotal,deliveryFee,total,payment:coPayment.value,paymentProofUrl,status:'new',inventoryManaged:true,inventory,createdAt:serverTimestamp()});tx.set(trackingRef,{orderNo,customerUid:currentUser.uid,status:'new',estimatedDelivery:'',updatedAt:serverTimestamp()});updates.forEach((u,i)=>{const r=reservationRows[i],item=items[i];tx.set(r.ref,{orderId:orderRef.id,productId:item.productId,customerUid:currentUser.uid,qty:item.qty,state:'reserved',createdAt:serverTimestamp()});tx.update(u.ref,{stock:u.stock,updatedAt:serverTimestamp(),lastInventoryReservationId:r.id})})});localStorage.setItem('MauriOne_account',JSON.stringify({...account(),...customer,uid:currentUser.uid,email:currentUser.email||''}));orderHistory.unshift({id:orderRef.id,orderNo,customerUid:currentUser.uid,items,subtotal,deliveryFee,total,payment:coPayment.value,status:'new',inventoryManaged:true,estimatedDelivery:'',updatedAt:new Date().toLocaleString('ar'),createdAt:Date.now()});saveOrders();connectTracking();cart=[];saveCart();updateBadge();renderCart();renderMyOrders();checkoutStatus.style.display='block';checkoutStatus.className='notice success';checkoutStatus.textContent=tpl(isTransfer?'orderSuccessTransferTemplate':'orderSuccessCodTemplate',{orderNo});placeOrderBtn.style.display='none'}catch(e){console.error(e);checkoutStatus.style.display='block';checkoutStatus.className='notice';const m=String(e?.message||'');if(m.startsWith('STOCK|')){const parts=m.split('|');checkoutStatus.textContent=tpl('stockUnavailableTemplate',{product:parts[1]||ct('genericProductText'),stock:Number(parts[2]||0)});renderCart()}else if(e?.code==='permission-denied'){checkoutStatus.textContent=ct('inventoryPermissionMessage')}else checkoutStatus.textContent=ct('orderErrorMessage')}finally{placeOrderBtn.disabled=false;placeOrderBtn.textContent=ct('confirmOrderText')}};'''
index = index[:start] + new_place_order + index[end:]

# Show delivery fee in customer order history
old_order_total = '<div class="order-total"><span>${esc(ct(\'orderTotalLabel\'))}</span><strong>${Number(o.total||0).toLocaleString()} MRU</strong></div>'
new_order_total = '${Number(o.deliveryFee||0)>0?`<div class="order-total"><span>${esc(ct(\'deliveryFeeLabel\'))}</span><strong>${Number(o.deliveryFee||0).toLocaleString()} MRU</strong></div>`:\'\'}<div class="order-total"><span>${esc(ct(\'orderTotalLabel\'))}</span><strong>${Number(o.total||0).toLocaleString()} MRU</strong></div>'
index = must_replace(index, old_order_total, new_order_total, 'customer order delivery fee')

index_path.write_text(index, encoding='utf-8')

# ---------- firestore.rules ----------
rules_path = Path('firestore.rules')
rules = rules_path.read_text(encoding='utf-8')
needle = "          'inventoryManaged',\n          'total',"
if rules.count(needle) < 2:
    raise SystemExit('Missing order key lists in rules')
rules = rules.replace(needle, "          'inventoryManaged',\n          'subtotal',\n          'deliveryFee',\n          'total',", 2)
valid_marker = "        && request.resource.data.inventoryManaged == true\n        && request.resource.data.total is number"
valid_repl = "        && request.resource.data.inventoryManaged == true\n        && request.resource.data.subtotal is number\n        && request.resource.data.subtotal > 0\n        && request.resource.data.subtotal <= 100000000\n        && request.resource.data.deliveryFee is number\n        && request.resource.data.deliveryFee >= 0\n        && request.resource.data.deliveryFee <= 1000000\n        && request.resource.data.total == request.resource.data.subtotal + request.resource.data.deliveryFee\n        && request.resource.data.total is number"
rules = must_replace(rules, valid_marker, valid_repl, 'delivery validation rules')
rules_path.write_text(rules, encoding='utf-8')

print('Delivery fee system patched successfully')
