from pathlib import Path

ADMIN = Path('admin.html')
INDEX = Path('index.html')

a = ADMIN.read_text(encoding='utf-8')
i = INDEX.read_text(encoding='utf-8')

# ---- Admin CSS ----
css_anchor = ".stickyActions{position:sticky;bottom:72px;background:#fff;padding:10px 0 2px;z-index:5}"
css_add = css_anchor + ".deliveryZones{display:grid;gap:8px;margin:10px 0}.deliveryZoneRow{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(92px,.7fr) 42px;gap:7px;align-items:center;border:1px solid #e8e8eb;border-radius:13px;padding:9px;background:#fafafa}.deliveryZoneRow input{width:100%;padding:11px;border:1px solid #e1e1e5;border-radius:9px;background:#fff}.deliveryZoneRemove{width:42px;height:42px;border:1px solid #f0c8c4;border-radius:10px;background:#fff;color:#b42318;font-size:18px}.deliveryZoneHead{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(92px,.7fr) 42px;gap:7px;color:#888;font-size:9px;padding:0 9px}.deliveryEmpty{padding:13px;border:1px dashed #d9d9de;border-radius:12px;color:#888;font-size:10px;text-align:center}"
if css_anchor not in a:
    raise SystemExit('admin css anchor missing')
a = a.replace(css_anchor, css_add, 1)

# ---- Admin delivery settings UI ----
old_settings = '''<section id="settings" class="page"><div class="panel"><h2>إعدادات المتجر</h2><div class="field"><label>مدينة التوصيل الافتراضية</label><input id="setDeliveryCity" placeholder="نواكشوط"></div><h3 style="font-size:14px;margin:18px 0 8px">رسوم التوصيل</h3><p class="adminHint">ضع سعرًا افتراضيًا، ثم أضف المدن أو المناطق الخاصة كل واحدة في سطر بالشكل: تفرغ زينة = 120</p><div class="field"><label>رسوم التوصيل الافتراضية (MRU)</label><input id="setDeliveryDefaultFee" type="number" min="0" step="1" value="0"></div><div class="field"><label>رسوم حسب المدينة / المنطقة</label><textarea id="setDeliveryRates" placeholder="تفرغ زينة = 120&#10;عرفات = 100&#10;لكصر = 90"></textarea></div><div class="field"><label>اسم البنك للتحويل</label><input id="setBankName"></div><div class="field"><label>اسم صاحب الحساب</label><input id="setBankHolder"></div><div class="field"><label>رقم الحساب / IBAN</label><input id="setBankAccount"></div><div class="field"><label>حالة المتجر</label><select id="setMaintenance"><option value="false">مفتوح</option><option value="true">وضع الصيانة</option></select></div><button class="primary" onclick="saveGeneralSettings()">حفظ الإعدادات</button><div id="settingsMsg" class="ok"></div></div></section>'''
new_settings = '''<section id="settings" class="page"><div class="panel"><h2>التوصيل والمدن</h2><p class="adminHint">حدد المدن أو المناطق التي يستطيع الزبون اختيارها عند الشراء، وحدد سعر التوصيل لكل منطقة. مثال: عرفات — 120 MRU.</p><div class="field"><label>المدينة / المنطقة الافتراضية</label><input id="setDeliveryCity" placeholder="مثال: عرفات"></div><div class="field"><label>رسوم افتراضية عند الحاجة (MRU)</label><input id="setDeliveryDefaultFee" type="number" min="0" step="1" value="0"></div><div class="sectionTitle"><h3 style="font-size:14px;margin:0">أسعار التوصيل حسب المنطقة</h3><span id="deliveryZoneCount" class="count">0</span></div><div class="deliveryZoneHead"><span>المدينة / المنطقة</span><span>السعر MRU</span><span></span></div><div id="deliveryZones" class="deliveryZones"></div><button class="secondary" type="button" onclick="addDeliveryZone()">＋ إضافة مدينة / منطقة</button><h3 style="font-size:14px;margin:24px 0 8px">التحويل البنكي والمتجر</h3><div class="field"><label>اسم البنك للتحويل</label><input id="setBankName"></div><div class="field"><label>اسم صاحب الحساب</label><input id="setBankHolder"></div><div class="field"><label>رقم الحساب / IBAN</label><input id="setBankAccount"></div><div class="field"><label>حالة المتجر</label><select id="setMaintenance"><option value="false">مفتوح</option><option value="true">وضع الصيانة</option></select></div><button class="primary" onclick="saveGeneralSettings()">حفظ إعدادات التوصيل والمتجر</button><div id="settingsMsg" class="ok"></div></div></section>'''
if old_settings not in a:
    raise SystemExit('admin settings block missing')
a = a.replace(old_settings, new_settings, 1)

# ---- Admin loading ----
old_load = "onSnapshot(doc(db,'storeSettings','general'),s=>{const d=s.data()||{};fill('setDeliveryCity',d.deliveryCity||'نواكشوط');fill('setDeliveryDefaultFee',Number(d.deliveryDefaultFee||0));fill('setDeliveryRates',Object.entries(d.deliveryRates||{}).map(([k,v])=>k+' = '+v).join('\\\n'));fill('setBankName',d.bankName||'');fill('setBankHolder',d.bankHolder||'');fill('setBankAccount',d.bankAccount||'');fill('setMaintenance',String(d.maintenance===true))});"
new_load = "onSnapshot(doc(db,'storeSettings','general'),s=>{const d=s.data()||{};fill('setDeliveryCity',d.deliveryCity||'نواكشوط');fill('setDeliveryDefaultFee',Number(d.deliveryDefaultFee||0));loadDeliveryZones(d.deliveryRates||{});fill('setBankName',d.bankName||'');fill('setBankHolder',d.bankHolder||'');fill('setBankAccount',d.bankAccount||'');fill('setMaintenance',String(d.maintenance===true))});"
if old_load not in a:
    raise SystemExit('admin settings load anchor missing')
a = a.replace(old_load, new_load, 1)

# ---- Admin zone functions/save ----
start = a.find("function parseDeliveryRates()")
end = a.find("window.saveLanguageSettings", start)
if start < 0 or end < 0:
    raise SystemExit('admin delivery parser block missing')
old_chunk = a[start:end]
new_chunk = '''function deliveryZoneRow(name='',fee=''){return `<div class="deliveryZoneRow"><input class="deliveryZoneName" placeholder="مثال: عرفات" value="${esc(name)}"><input class="deliveryZoneFee" type="number" min="0" step="1" placeholder="0" value="${Number.isFinite(Number(fee))?Number(fee):0}"><button class="deliveryZoneRemove" type="button" aria-label="حذف" onclick="this.closest('.deliveryZoneRow').remove();refreshDeliveryZoneCount()">×</button></div>`}
window.refreshDeliveryZoneCount=()=>{const n=document.querySelectorAll('#deliveryZones .deliveryZoneRow').length;$('deliveryZoneCount').textContent=n;if(!n)$('deliveryZones').innerHTML='<div class="deliveryEmpty">لا توجد مناطق بعد. اضغط «إضافة مدينة / منطقة».</div>'};
window.addDeliveryZone=(name='',fee='')=>{const box=$('deliveryZones');box.querySelector('.deliveryEmpty')?.remove();box.insertAdjacentHTML('beforeend',deliveryZoneRow(name,fee));refreshDeliveryZoneCount();const rows=box.querySelectorAll('.deliveryZoneRow');rows[rows.length-1]?.querySelector('.deliveryZoneName')?.focus()};
function loadDeliveryZones(rates={}){const box=$('deliveryZones');box.innerHTML='';Object.entries(rates).forEach(([name,fee])=>box.insertAdjacentHTML('beforeend',deliveryZoneRow(name,fee)));refreshDeliveryZoneCount()}
function readDeliveryRates(){const out={};for(const row of document.querySelectorAll('#deliveryZones .deliveryZoneRow')){const name=row.querySelector('.deliveryZoneName').value.trim(),fee=Number(row.querySelector('.deliveryZoneFee').value||0);if(!name)throw Error('أدخل اسم كل مدينة أو منطقة.');if(!Number.isFinite(fee)||fee<0)throw Error('سعر التوصيل يجب أن يكون صفرًا أو أكثر.');if(Object.prototype.hasOwnProperty.call(out,name))throw Error('المنطقة «'+name+'» مكررة.');out[name]=fee}return out}
window.saveGeneralSettings=async()=>{try{const deliveryRates=readDeliveryRates();const deliveryCity=$('setDeliveryCity').value.trim();if(Object.keys(deliveryRates).length&&deliveryCity&&!Object.prototype.hasOwnProperty.call(deliveryRates,deliveryCity))throw Error('المنطقة الافتراضية يجب أن تكون واحدة من مناطق التوصيل المضافة.');await setDoc(doc(db,'storeSettings','general'),{deliveryCity,deliveryDefaultFee:Math.max(0,Number($('setDeliveryDefaultFee').value||0)),deliveryRates,bankName:$('setBankName').value.trim(),bankHolder:$('setBankHolder').value.trim(),bankAccount:$('setBankAccount').value.trim(),maintenance:$('setMaintenance').value==='true',updatedAt:serverTimestamp()},{merge:true});$('settingsMsg').textContent='تم حفظ المدن وأسعار التوصيل وإعدادات المتجر.'}catch(e){$('settingsMsg').textContent='تعذر الحفظ: '+e.message}};
'''
a = a[:start] + new_chunk + a[end:]

# ---- Store checkout city input -> select ----
old_city = '<div class="field"><label id="checkoutCityLabel">المدينة / المنطقة</label><input id="coCity" oninput="updateCheckoutTotals()"></div>'
new_city = '<div class="field"><label id="checkoutCityLabel">المدينة / المنطقة</label><select id="coCity" onchange="updateCheckoutTotals()"><option value="">اختر المدينة / المنطقة</option></select><div id="coDeliveryChoice" class="delivery-note">اختر المنطقة ليظهر سعر التوصيل.</div></div>'
if old_city not in i:
    raise SystemExit('store city input missing')
i = i.replace(old_city, new_city, 1)

# ---- Store delivery functions ----
old_funcs = "function normalizeZone(v){return String(v||'').trim()}\nfunction deliveryFeeForCity(city){const target=normalizeZone(city),rates=generalSettings.deliveryRates||{};if(target){for(const [name,fee] of Object.entries(rates)){if(normalizeZone(name)===target)return Math.max(0,Number(fee||0))}}return Math.max(0,Number(generalSettings.deliveryDefaultFee||0))}\nfunction applyGeneralSettings(d={}){generalSettings=d;const info=document.getElementById('bankTransferInfo');if(info){const parts=[];if(d.bankName)parts.push('البنك: '+d.bankName);if(d.bankHolder)parts.push('اسم الحساب: '+d.bankHolder);if(d.bankAccount)parts.push('رقم الحساب: '+d.bankAccount);info.textContent=parts.length?parts.join(' • '):ct('bankInfoEmptyMessage')}if(typeof window.updateCheckoutTotals==='function')window.updateCheckoutTotals()}"
new_funcs = "function normalizeZone(v){return String(v||'').trim()}\nfunction deliveryRows(){const rates=generalSettings.deliveryRates||{};const rows=Object.entries(rates).filter(([,fee])=>Number.isFinite(Number(fee))&&Number(fee)>=0);if(!rows.length&&generalSettings.deliveryCity)rows.push([generalSettings.deliveryCity,Math.max(0,Number(generalSettings.deliveryDefaultFee||0))]);return rows}\nfunction deliveryFeeForCity(city){const target=normalizeZone(city),rates=generalSettings.deliveryRates||{};if(target){for(const [name,fee] of Object.entries(rates)){if(normalizeZone(name)===target)return Math.max(0,Number(fee||0))}if(!Object.keys(rates).length&&normalizeZone(generalSettings.deliveryCity)===target)return Math.max(0,Number(generalSettings.deliveryDefaultFee||0))}return Math.max(0,Number(generalSettings.deliveryDefaultFee||0))}\nfunction syncDeliverySelect(preferred=''){const sel=document.getElementById('coCity');if(!sel)return;const rows=deliveryRows(),wanted=normalizeZone(preferred||sel.value||'');sel.innerHTML='<option value=\"\">اختر المدينة / المنطقة</option>'+rows.map(([name,fee])=>`<option value=\"${esc(name)}\">${esc(name)} — ${Number(fee||0).toLocaleString()} MRU</option>`).join('');const match=rows.find(([name])=>normalizeZone(name)===wanted)||rows.find(([name])=>normalizeZone(name)===normalizeZone(generalSettings.deliveryCity));sel.value=match?match[0]:'';if(typeof window.updateCheckoutTotals==='function')window.updateCheckoutTotals()}\nfunction applyGeneralSettings(d={}){generalSettings=d;const info=document.getElementById('bankTransferInfo');if(info){const parts=[];if(d.bankName)parts.push('البنك: '+d.bankName);if(d.bankHolder)parts.push('اسم الحساب: '+d.bankHolder);if(d.bankAccount)parts.push('رقم الحساب: '+d.bankAccount);info.textContent=parts.length?parts.join(' • '):ct('bankInfoEmptyMessage')}syncDeliverySelect(document.getElementById('coCity')?.value||'')}"
if old_funcs not in i:
    raise SystemExit('store delivery functions anchor missing')
i = i.replace(old_funcs, new_funcs, 1)

# ---- Store totals hint ----
old_totals = "window.updateCheckoutTotals=()=>{const subtotal=cartSubtotalValue(),fee=deliveryFeeForCity(document.getElementById('coCity')?.value||''),total=subtotal+fee;const a=document.getElementById('coSubtotal'),b=document.getElementById('coDeliveryFee'),c=document.getElementById('coGrandTotal');if(a)a.textContent=money(subtotal);if(b)b.textContent=fee>0?money(fee):ct('freeDeliveryText');if(c)c.textContent=money(total)};"
new_totals = "window.updateCheckoutTotals=()=>{const subtotal=cartSubtotalValue(),city=document.getElementById('coCity')?.value||'',fee=city?deliveryFeeForCity(city):0,total=subtotal+fee;const a=document.getElementById('coSubtotal'),b=document.getElementById('coDeliveryFee'),c=document.getElementById('coGrandTotal'),hint=document.getElementById('coDeliveryChoice');if(a)a.textContent=money(subtotal);if(b)b.textContent=city?(fee>0?money(fee):ct('freeDeliveryText')):'—';if(c)c.textContent=money(total);if(hint)hint.textContent=city?`التوصيل إلى ${city}: ${fee>0?money(fee):ct('freeDeliveryText')}`:'اختر المنطقة ليظهر سعر التوصيل.'};"
if old_totals not in i:
    raise SystemExit('store totals anchor missing')
i = i.replace(old_totals, new_totals, 1)

# ---- Store checkout preferred city and required city ----
old_checkout = "const a=account();coName.value=a.name||'';coPhone.value=a.phone||'';coCity.value=a.city||generalSettings.deliveryCity||'';coAddress.value=a.address||'';"
new_checkout = "const a=account();coName.value=a.name||'';coPhone.value=a.phone||'';syncDeliverySelect(a.city||generalSettings.deliveryCity||'');coAddress.value=a.address||'';"
if old_checkout not in i:
    raise SystemExit('store checkout city assignment missing')
i = i.replace(old_checkout, new_checkout, 1)

old_required = "if(!customer.name||!customer.phone||!customer.address){checkoutStatus.style.display='block';checkoutStatus.className='notice';checkoutStatus.textContent=ct('requiredFieldsMessage');return}"
new_required = "if(!customer.name||!customer.phone||!customer.city||!customer.address){checkoutStatus.style.display='block';checkoutStatus.className='notice';checkoutStatus.textContent=!customer.city?'اختر مدينة / منطقة التوصيل.':ct('requiredFieldsMessage');return}"
if old_required not in i:
    raise SystemExit('store required fields anchor missing')
i = i.replace(old_required, new_required, 1)

ADMIN.write_text(a, encoding='utf-8')
INDEX.write_text(i, encoding='utf-8')
print('Structured delivery zones patched')
