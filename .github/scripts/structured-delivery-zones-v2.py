from pathlib import Path

ADMIN=Path('admin.html')
INDEX=Path('index.html')
a=ADMIN.read_text(encoding='utf-8')
i=INDEX.read_text(encoding='utf-8')

# Admin styles
anchor='.stickyActions{position:sticky;bottom:72px;background:#fff;padding:10px 0 2px;z-index:5}'
extra='.deliveryZones{display:grid;gap:8px;margin:10px 0}.deliveryZoneRow{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(92px,.7fr) 42px;gap:7px;align-items:center;border:1px solid #e8e8eb;border-radius:13px;padding:9px;background:#fafafa}.deliveryZoneRow input{width:100%;padding:11px;border:1px solid #e1e1e5;border-radius:9px;background:#fff}.deliveryZoneRemove{width:42px;height:42px;border:1px solid #f0c8c4;border-radius:10px;background:#fff;color:#b42318;font-size:18px}.deliveryZoneHead{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(92px,.7fr) 42px;gap:7px;color:#888;font-size:9px;padding:0 9px}.deliveryEmpty{padding:13px;border:1px dashed #d9d9de;border-radius:12px;color:#888;font-size:10px;text-align:center}'
if '.deliveryZones{' not in a:
    if anchor not in a: raise SystemExit('css anchor missing')
    a=a.replace(anchor,anchor+extra,1)

# Admin UI
s=a.find('<section id="settings" class="page">')
e=a.find('</section>',s)
if s<0 or e<0: raise SystemExit('settings section missing')
e+=len('</section>')
new_settings='''<section id="settings" class="page"><div class="panel"><h2>التوصيل والمدن</h2><p class="adminHint">حدد المدن أو المناطق التي يستطيع الزبون اختيارها عند الشراء، وحدد سعر التوصيل لكل منطقة. مثال: عرفات — 120 MRU.</p><div class="field"><label>المدينة / المنطقة الافتراضية</label><input id="setDeliveryCity" placeholder="مثال: عرفات"></div><div class="field"><label>رسوم افتراضية عند الحاجة (MRU)</label><input id="setDeliveryDefaultFee" type="number" min="0" step="1" value="0"></div><div class="sectionTitle"><h3 style="font-size:14px;margin:0">أسعار التوصيل حسب المنطقة</h3><span id="deliveryZoneCount" class="count">0</span></div><div class="deliveryZoneHead"><span>المدينة / المنطقة</span><span>السعر MRU</span><span></span></div><div id="deliveryZones" class="deliveryZones"></div><button class="secondary" type="button" onclick="addDeliveryZone()">＋ إضافة مدينة / منطقة</button><h3 style="font-size:14px;margin:24px 0 8px">التحويل البنكي والمتجر</h3><div class="field"><label>اسم البنك للتحويل</label><input id="setBankName"></div><div class="field"><label>اسم صاحب الحساب</label><input id="setBankHolder"></div><div class="field"><label>رقم الحساب / IBAN</label><input id="setBankAccount"></div><div class="field"><label>حالة المتجر</label><select id="setMaintenance"><option value="false">مفتوح</option><option value="true">وضع الصيانة</option></select></div><button class="primary" onclick="saveGeneralSettings()">حفظ إعدادات التوصيل والمتجر</button><div id="settingsMsg" class="ok"></div></div></section>'''
a=a[:s]+new_settings+a[e:]

# Admin load: replace legacy textarea loader only
p=a.find("fill('setDeliveryRates'")
if p<0: raise SystemExit('legacy delivery loader missing')
q=a.find(";fill('setBankName'",p)
if q<0: raise SystemExit('bank loader anchor missing')
a=a[:p]+"loadDeliveryZones(d.deliveryRates||{})"+a[q:]

# Admin zone functions + save
p=a.find('function parseDeliveryRates()')
q=a.find('window.saveLanguageSettings',p)
if p<0 or q<0: raise SystemExit('legacy delivery parser/save missing')
admin_delivery='''function deliveryZoneRow(name='',fee=''){return `<div class="deliveryZoneRow"><input class="deliveryZoneName" placeholder="مثال: عرفات" value="${esc(name)}"><input class="deliveryZoneFee" type="number" min="0" step="1" placeholder="0" value="${Number.isFinite(Number(fee))?Number(fee):0}"><button class="deliveryZoneRemove" type="button" aria-label="حذف" onclick="this.closest('.deliveryZoneRow').remove();refreshDeliveryZoneCount()">×</button></div>`}
window.refreshDeliveryZoneCount=()=>{const n=document.querySelectorAll('#deliveryZones .deliveryZoneRow').length;$('deliveryZoneCount').textContent=n;if(!n)$('deliveryZones').innerHTML='<div class="deliveryEmpty">لا توجد مناطق بعد. اضغط «إضافة مدينة / منطقة».</div>'};
window.addDeliveryZone=(name='',fee='')=>{const box=$('deliveryZones');box.querySelector('.deliveryEmpty')?.remove();box.insertAdjacentHTML('beforeend',deliveryZoneRow(name,fee));refreshDeliveryZoneCount();const rows=box.querySelectorAll('.deliveryZoneRow');rows[rows.length-1]?.querySelector('.deliveryZoneName')?.focus()};
function loadDeliveryZones(rates={}){const box=$('deliveryZones');box.innerHTML='';Object.entries(rates).forEach(([name,fee])=>box.insertAdjacentHTML('beforeend',deliveryZoneRow(name,fee)));refreshDeliveryZoneCount()}
function readDeliveryRates(){const out={};for(const row of document.querySelectorAll('#deliveryZones .deliveryZoneRow')){const name=row.querySelector('.deliveryZoneName').value.trim(),fee=Number(row.querySelector('.deliveryZoneFee').value||0);if(!name)throw Error('أدخل اسم كل مدينة أو منطقة.');if(!Number.isFinite(fee)||fee<0)throw Error('سعر التوصيل يجب أن يكون صفرًا أو أكثر.');if(Object.prototype.hasOwnProperty.call(out,name))throw Error('المنطقة «'+name+'» مكررة.');out[name]=fee}return out}
window.saveGeneralSettings=async()=>{try{const deliveryRates=readDeliveryRates();let deliveryCity=$('setDeliveryCity').value.trim();if(Object.keys(deliveryRates).length&&!Object.prototype.hasOwnProperty.call(deliveryRates,deliveryCity))deliveryCity=Object.keys(deliveryRates)[0];fill('setDeliveryCity',deliveryCity);await setDoc(doc(db,'storeSettings','general'),{deliveryCity,deliveryDefaultFee:Math.max(0,Number($('setDeliveryDefaultFee').value||0)),deliveryRates,bankName:$('setBankName').value.trim(),bankHolder:$('setBankHolder').value.trim(),bankAccount:$('setBankAccount').value.trim(),maintenance:$('setMaintenance').value==='true',updatedAt:serverTimestamp()},{merge:true});$('settingsMsg').textContent='تم حفظ المدن وأسعار التوصيل وإعدادات المتجر.'}catch(e){$('settingsMsg').textContent='تعذر الحفظ: '+e.message}};
'''
a=a[:p]+admin_delivery+a[q:]

# Store checkout city select
old='<div class="field"><label id="checkoutCityLabel">المدينة / المنطقة</label><input id="coCity" oninput="updateCheckoutTotals()"></div>'
new='<div class="field"><label id="checkoutCityLabel">المدينة / المنطقة</label><select id="coCity" onchange="updateCheckoutTotals()"><option value="">اختر المدينة / المنطقة</option></select><div id="coDeliveryChoice" class="delivery-note">اختر المنطقة ليظهر سعر التوصيل.</div></div>'
if old not in i: raise SystemExit('checkout city field missing')
i=i.replace(old,new,1)

# Store delivery logic
p=i.find('function normalizeZone(v)')
q=i.find('function applyLanguageSettings',p)
if p<0 or q<0: raise SystemExit('store delivery logic anchors missing')
store_delivery='''function normalizeZone(v){return String(v||'').trim()}
function deliveryRows(){const rates=generalSettings.deliveryRates||{};const rows=Object.entries(rates).filter(([,fee])=>Number.isFinite(Number(fee))&&Number(fee)>=0);if(!rows.length&&generalSettings.deliveryCity)rows.push([generalSettings.deliveryCity,Math.max(0,Number(generalSettings.deliveryDefaultFee||0))]);return rows}
function deliveryFeeForCity(city){const target=normalizeZone(city),rates=generalSettings.deliveryRates||{};if(target){for(const [name,fee] of Object.entries(rates)){if(normalizeZone(name)===target)return Math.max(0,Number(fee||0))}if(!Object.keys(rates).length&&normalizeZone(generalSettings.deliveryCity)===target)return Math.max(0,Number(generalSettings.deliveryDefaultFee||0))}return Math.max(0,Number(generalSettings.deliveryDefaultFee||0))}
function syncDeliverySelect(preferred=''){const sel=document.getElementById('coCity');if(!sel)return;const rows=deliveryRows(),wanted=normalizeZone(preferred||sel.value||'');sel.innerHTML='<option value="">اختر المدينة / المنطقة</option>'+rows.map(([name,fee])=>`<option value="${esc(name)}">${esc(name)} — ${Number(fee||0).toLocaleString()} MRU</option>`).join('');const match=rows.find(([name])=>normalizeZone(name)===wanted)||rows.find(([name])=>normalizeZone(name)===normalizeZone(generalSettings.deliveryCity));sel.value=match?match[0]:'';if(typeof window.updateCheckoutTotals==='function')window.updateCheckoutTotals()}
function applyGeneralSettings(d={}){generalSettings=d;const info=document.getElementById('bankTransferInfo');if(info){const parts=[];if(d.bankName)parts.push('البنك: '+d.bankName);if(d.bankHolder)parts.push('اسم الحساب: '+d.bankHolder);if(d.bankAccount)parts.push('رقم الحساب: '+d.bankAccount);info.textContent=parts.length?parts.join(' • '):ct('bankInfoEmptyMessage')}syncDeliverySelect(document.getElementById('coCity')?.value||'')}
'''
i=i[:p]+store_delivery+i[q:]

old="window.updateCheckoutTotals=()=>{const subtotal=cartSubtotalValue(),fee=deliveryFeeForCity(document.getElementById('coCity')?.value||''),total=subtotal+fee;const a=document.getElementById('coSubtotal'),b=document.getElementById('coDeliveryFee'),c=document.getElementById('coGrandTotal');if(a)a.textContent=money(subtotal);if(b)b.textContent=fee>0?money(fee):ct('freeDeliveryText');if(c)c.textContent=money(total)};"
new="window.updateCheckoutTotals=()=>{const subtotal=cartSubtotalValue(),city=document.getElementById('coCity')?.value||'',fee=city?deliveryFeeForCity(city):0,total=subtotal+fee;const a=document.getElementById('coSubtotal'),b=document.getElementById('coDeliveryFee'),c=document.getElementById('coGrandTotal'),hint=document.getElementById('coDeliveryChoice');if(a)a.textContent=money(subtotal);if(b)b.textContent=city?(fee>0?money(fee):ct('freeDeliveryText')):'—';if(c)c.textContent=money(total);if(hint)hint.textContent=city?`التوصيل إلى ${city}: ${fee>0?money(fee):ct('freeDeliveryText')}`:'اختر المنطقة ليظهر سعر التوصيل.'};"
if old not in i: raise SystemExit('checkout totals missing')
i=i.replace(old,new,1)

old="const a=account();coName.value=a.name||'';coPhone.value=a.phone||'';coCity.value=a.city||generalSettings.deliveryCity||'';coAddress.value=a.address||'';"
new="const a=account();coName.value=a.name||'';coPhone.value=a.phone||'';syncDeliverySelect(a.city||generalSettings.deliveryCity||'');coAddress.value=a.address||'';"
if old not in i: raise SystemExit('checkout fill missing')
i=i.replace(old,new,1)

old="if(!customer.name||!customer.phone||!customer.address){checkoutStatus.style.display='block';checkoutStatus.className='notice';checkoutStatus.textContent=ct('requiredFieldsMessage');return}"
new="if(!customer.name||!customer.phone||!customer.city||!customer.address){checkoutStatus.style.display='block';checkoutStatus.className='notice';checkoutStatus.textContent=!customer.city?'اختر مدينة / منطقة التوصيل.':ct('requiredFieldsMessage');return}"
if old not in i: raise SystemExit('required fields check missing')
i=i.replace(old,new,1)

ADMIN.write_text(a,encoding='utf-8')
INDEX.write_text(i,encoding='utf-8')
print('Structured delivery zones v2 patched')
