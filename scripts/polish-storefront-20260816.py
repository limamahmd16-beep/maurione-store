from pathlib import Path

# ---------- Storefront ----------
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Compact first screen and improve readability.
repls={
'.circle{width:38px;height:38px;border:0;border-radius:50%;background:var(--soft);display:grid;place-items:center;position:relative}':'.circle{width:38px;height:38px;border:0;border-radius:50%;background:var(--soft);display:grid;place-items:center;position:relative}.circle svg{width:20px;height:20px;fill:none;stroke:var(--navy);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}',
'.hero{min-height:430px;':'.hero{min-height:330px;',
'.hero-copy{padding:44px 28px 0;':'.hero-copy{padding:34px 24px 0;',
'.hero h1{font-size:39px;':'.hero h1{font-size:34px;',
'.hero p{margin-top:15px;max-width:285px;color:#b7bac1;font-size:11px;':'.hero p{margin-top:13px;max-width:310px;color:#c4c8cf;font-size:13px;',
'.trust-card{min-height:165px;padding:19px 10px;':'.trust-card{min-height:118px;padding:14px 10px;',
'.icon-box{width:62px;height:62px;margin:0 auto 14px;':'.icon-box{width:48px;height:48px;margin:0 auto 10px;',
'.icon-box svg{width:39px;height:39px;':'.icon-box svg{width:31px;height:31px;',
'.section{padding:38px 12px 0}':'.section{padding:28px 12px 0}',
'.category-art{height:80px;border-radius:13px;background:var(--soft);display:grid;place-items:center;font-size:34px}':'.category-art{height:72px;border-radius:13px;background:var(--soft);display:grid;place-items:center}.category-art svg{width:36px;height:36px;fill:none;stroke:var(--navy);stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}.category-art svg .accent{stroke:var(--gold)}',
'.category strong{display:block;margin-top:8px;font-size:11px}':'.category strong{display:block;margin-top:8px;font-size:12px}',
'.product small{display:block;margin-top:7px;color:var(--muted);font-size:8px}':'.product small{display:block;margin-top:7px;color:var(--muted);font-size:10px;line-height:1.45}',
'.product h3{font-size:11px;margin-top:4px;min-height:30px}':'.product h3{font-size:13px;line-height:1.45;margin-top:5px;min-height:38px}',
'.price{margin-top:6px;font-size:13px;font-weight:800}':'.price{margin-top:7px;font-size:15px;font-weight:900}',
'.stock{margin-top:5px;font-size:8px;color:var(--green)}':'.stock{margin-top:6px;font-size:10px;color:var(--green)}',
'.add{width:100%;margin-top:9px;padding:9px;border:0;border-radius:9px;background:#111;color:#fff;font-size:9px}':'.add{width:100%;margin-top:10px;padding:11px;border:0;border-radius:10px;background:#111;color:#fff;font-size:11px;font-weight:800}',
}
for old,new in repls.items():
    if old in s:
        s=s.replace(old,new,1)

# Floating WhatsApp support button.
if '.support-fab{' not in s:
    anchor='.product-rating .stars{color:var(--gold);letter-spacing:.5px}.product-rating .rating-count{color:var(--muted)}'
    assert anchor in s, 'support css anchor missing'
    s=s.replace(anchor,anchor+'.support-fab{display:none;position:fixed;left:14px;bottom:92px;z-index:120;width:52px;height:52px;border-radius:50%;background:#111;color:#fff;align-items:center;justify-content:center;box-shadow:0 10px 28px rgba(0,0,0,.18);text-decoration:none}.support-fab.show{display:flex}.support-fab svg{width:25px;height:25px;fill:none;stroke:#fff;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}',1)

# Replace top emoji tools with consistent SVG icons.
s=s.replace('<button class="circle" onclick="openLanguages()" aria-label="اللغة">🌐</button>','<button class="circle" onclick="openLanguages()" aria-label="اللغة"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.7 2.6 4 5.6 4 9s-1.3 6.4-4 9c-2.7-2.6-4-5.6-4-9s1.3-6.4 4-9Z"/></svg></button>',1)
s=s.replace('<button class="circle" onclick="openStore(\'cartPage\',\'navCart\')" aria-label="السلة">🛒<span class="badge" id="cartBadge">0</span></button>','<button class="circle" onclick="openStore(\'cartPage\',\'navCart\')" aria-label="السلة"><svg viewBox="0 0 24 24"><path d="M3 5h2l2.2 10.5h9.9l2.2-7.5H6"/><circle cx="9" cy="19" r="1.3"/><circle cx="17" cy="19" r="1.3"/></svg><span class="badge" id="cartBadge">0</span></button>',1)

# Put products before categories on the home page and use accurate title.
old_home='<section id="siteCategoriesSection" class="section"><div class="section-head"><h2 id="siteCategoriesTitle">تسوق حسب الفئة</h2><button class="view-all" onclick="showAllProducts()" id="viewAllCategoriesText">عرض الكل</button></div><div class="categories" id="homeCategories"></div></section><section id="siteProductsSection" class="section"><div class="section-head"><h2 id="siteProductsTitle">الأكثر طلبًا</h2><button class="view-all" onclick="showAllProducts()" id="viewAllProductsText">عرض الكل</button></div><div class="products" id="productList"></div></section>'
new_home='<section id="siteProductsSection" class="section"><div class="section-head"><h2 id="siteProductsTitle">منتجاتنا</h2><button class="view-all" onclick="showAllProducts()" id="viewAllProductsText">عرض الكل</button></div><div class="products" id="productList"></div></section><section id="siteCategoriesSection" class="section"><div class="section-head"><h2 id="siteCategoriesTitle">تسوق حسب الفئة</h2><button class="view-all" onclick="showAllProducts()" id="viewAllCategoriesText">عرض الكل</button></div><div class="categories" id="homeCategories"></div></section>'
if old_home in s:
    s=s.replace(old_home,new_home,1)
else:
    s=s.replace('<h2 id="siteProductsTitle">الأكثر طلبًا</h2>','<h2 id="siteProductsTitle">منتجاتنا</h2>',1)

# Only expose Arabic until real translations are complete.
old_lang='<div class="lang-grid"><button id="langArPublic" onclick="setLanguage(\'ar\')">العربية</button><button id="langFrPublic" onclick="setLanguage(\'fr\')">Français</button><button id="langEnPublic" onclick="setLanguage(\'en\')">English</button><button id="langPtPublic" onclick="setLanguage(\'pt\')">Português</button></div><div class="notice" id="languageNote">سيتم حفظ اختيار اللغة على هذا الجهاز. ترجمة أسماء المنتجات تبقى كما أُدخلت من الإدارة.</div>'
new_lang='<div class="lang-grid" style="grid-template-columns:1fr"><button id="langArPublic" onclick="setLanguage(\'ar\')">العربية</button></div><div class="notice" id="languageNote">العربية متاحة الآن. الفرنسية والإنجليزية والبرتغالية ستظهر بعد اكتمال ترجمة الواجهة بالكامل.</div>'
if old_lang in s:
    s=s.replace(old_lang,new_lang,1)

# Add floating support button before bottom navigation.
if 'id="whatsappSupport"' not in s:
    anchor='<nav class="bottom-nav">'
    assert anchor in s, 'bottom nav anchor missing'
    fab='<a id="whatsappSupport" class="support-fab" href="#" target="_blank" rel="noopener" aria-label="دعم MauriOne عبر WhatsApp"><svg viewBox="0 0 24 24"><path d="M20 11.5a8 8 0 0 1-11.8 7L4 20l1.5-4A8 8 0 1 1 20 11.5Z"/><path d="M8.5 9.2c.8 2.2 2.1 3.6 4.4 4.5M13.6 13.9l1.3-.8"/></svg></a>'
    s=s.replace(anchor,fab+anchor,1)

# Category SVG system.
s=s.replace("const categoryData=[['الهواتف','📱'],['الكمبيوتر','💻'],['الإكسسوارات','🎧'],['الساعات','⌚'],['السماعات','🎧']];","const categoryData=[['الهواتف','phone'],['الكمبيوتر','computer'],['الإكسسوارات','accessories'],['الساعات','watch'],['السماعات','headphones']];",1)
old_cat_fn="function categoryButtons(){return categoryData.map(([name,icon])=>`<button class=\"category\" onclick=\"filterCategory('${name}')\"><div class=\"category-art\">${icon}</div><strong>${esc(displayCategory(name))}</strong></button>`).join('')}"
new_cat_fn="const categoryIcons={phone:'<svg viewBox=\"0 0 48 48\"><rect x=\"14\" y=\"5\" width=\"20\" height=\"38\" rx=\"5\"/><path class=\"accent\" d=\"M21 9h6M22 38h4\"/></svg>',computer:'<svg viewBox=\"0 0 48 48\"><rect x=\"7\" y=\"8\" width=\"34\" height=\"24\" rx=\"3\"/><path class=\"accent\" d=\"M17 40h14M22 32v8M26 32v8\"/></svg>',accessories:'<svg viewBox=\"0 0 48 48\"><path d=\"M15 20a9 9 0 0 1 18 0v12\"/><rect x=\"9\" y=\"24\" width=\"8\" height=\"13\" rx=\"3\"/><rect x=\"31\" y=\"24\" width=\"8\" height=\"13\" rx=\"3\"/><path class=\"accent\" d=\"M24 8v5\"/></svg>',watch:'<svg viewBox=\"0 0 48 48\"><rect x=\"14\" y=\"14\" width=\"20\" height=\"20\" rx=\"6\"/><path d=\"M19 14l2-8h6l2 8M19 34l2 8h6l2-8\"/><path class=\"accent\" d=\"M24 19v6l4 2\"/></svg>',headphones:'<svg viewBox=\"0 0 48 48\"><path d=\"M9 27v-5a15 15 0 0 1 30 0v5\"/><rect x=\"7\" y=\"25\" width=\"8\" height=\"14\" rx=\"4\"/><rect x=\"33\" y=\"25\" width=\"8\" height=\"14\" rx=\"4\"/><path class=\"accent\" d=\"M33 39h-5\"/></svg>'};function categoryButtons(){return categoryData.map(([name,key])=>`<button class=\"category\" onclick=\"filterCategory('${name}')\"><div class=\"category-art\">${categoryIcons[key]||''}</div><strong>${esc(displayCategory(name))}</strong></button>`).join('')}"
if old_cat_fn in s:
    s=s.replace(old_cat_fn,new_cat_fn,1)

# Accurate products section title even for existing legacy content document.
s=s.replace("function applySiteContent(c={}){contentSettings={...CONTENT_DEFAULTS,...c};","function applySiteContent(c={}){if(c.productsTitle==='الأكثر طلبًا')c={...c,productsTitle:'منتجاتنا'};contentSettings={...CONTENT_DEFAULTS,...c};",1)
s=s.replace('"productsTitle":"الأكثر طلبًا"','"productsTitle":"منتجاتنا"',1)

# WhatsApp support setting wired to storefront.
old_apply="function applyGeneralSettings(d={}){generalSettings=d;const info=document.getElementById('bankTransferInfo');if(info){const parts=[];if(d.bankName)parts.push('البنك: '+d.bankName);if(d.bankHolder)parts.push('اسم الحساب: '+d.bankHolder);if(d.bankAccount)parts.push('رقم الحساب: '+d.bankAccount);info.textContent=parts.length?parts.join(' • '):ct('bankInfoEmptyMessage')}syncDeliverySelect(document.getElementById('coCity')?.value||'')}"
new_apply="function applyGeneralSettings(d={}){generalSettings=d;const info=document.getElementById('bankTransferInfo');if(info){const parts=[];if(d.bankName)parts.push('البنك: '+d.bankName);if(d.bankHolder)parts.push('اسم الحساب: '+d.bankHolder);if(d.bankAccount)parts.push('رقم الحساب: '+d.bankAccount);info.textContent=parts.length?parts.join(' • '):ct('bankInfoEmptyMessage')}const support=document.getElementById('whatsappSupport'),digits=String(d.supportWhatsApp||'').replace(/\\D/g,'');if(support){support.classList.toggle('show',!!digits);support.href=digits?'https://wa.me/'+digits:'#'}syncDeliverySelect(document.getElementById('coCity')?.value||'')}"
assert old_apply in s, 'applyGeneralSettings anchor missing'
s=s.replace(old_apply,new_apply,1)

# Force Arabic while translations are incomplete.
old_saved="const savedLang=localStorage.getItem('MauriOne_lang')||'ar';document.documentElement.lang=savedLang;document.documentElement.dir=uiLang[savedLang]?.dir||'rtl';loadAccount();renderStore();renderMyOrders();connectTracking();"
new_saved="const savedLang='ar';localStorage.setItem('MauriOne_lang','ar');document.documentElement.lang='ar';document.documentElement.dir='rtl';loadAccount();renderStore();renderMyOrders();connectTracking();"
assert old_saved in s, 'saved language anchor missing'
s=s.replace(old_saved,new_saved,1)
old_set="window.setLanguage=lang=>{localStorage.setItem('MauriOne_lang',lang);document.documentElement.lang=lang;document.documentElement.dir=uiLang[lang]?.dir||'rtl';closeOverlay('languageOverlay');alert(ct(uiLang[lang]?.key,'OK'))};"
new_set="window.setLanguage=lang=>{localStorage.setItem('MauriOne_lang','ar');document.documentElement.lang='ar';document.documentElement.dir='rtl';closeOverlay('languageOverlay');alert(ct('langSelectedAr','تم اختيار العربية.'))};"
assert old_set in s, 'setLanguage anchor missing'
s=s.replace(old_set,new_set,1)

p.write_text(s,encoding='utf-8')

# ---------- Admin ----------
p=Path('admin.html')
a=p.read_text(encoding='utf-8')

# WhatsApp support field in settings.
old_bank='<div class="field"><label>اسم البنك للتحويل</label><input id="setBankName"></div>'
new_bank='<div class="field"><label>رقم WhatsApp للدعم</label><input id="setSupportWhatsApp" inputmode="tel" placeholder="مثال: 22212345678"></div><p class="adminHint">اكتب الرقم مع مفتاح الدولة وبدون علامة +. إذا تركته فارغًا فلن يظهر زر WhatsApp في المتجر.</p>'+old_bank
if 'id="setSupportWhatsApp"' not in a:
    assert old_bank in a, 'admin bank anchor missing'
    a=a.replace(old_bank,new_bank,1)

# Make language status clear: Arabic only until translation is complete.
old_hint='<p class="adminHint">تحكم في اللغات التي يستطيع الزبون اختيارها وفي اللغة الافتراضية للمتجر.</p>'
new_hint='<p class="adminHint">العربية هي اللغة المتاحة حاليًا للزبون. سيتم تفعيل الفرنسية والإنجليزية والبرتغالية بعد اكتمال ترجمة جميع نصوص الواجهة.</p>'
a=a.replace(old_hint,new_hint,1)
a=a.replace('<option value="fr">Français</option><option value="en">English</option><option value="pt">Português</option>','<option value="fr" disabled>Français — قريبًا</option><option value="en" disabled>English — قريبًا</option><option value="pt" disabled>Português — قريبًا</option>',1)
a=a.replace('<label class="checkItem"><input id="langFr" type="checkbox" checked> Français</label><label class="checkItem"><input id="langEn" type="checkbox" checked> English</label><label class="checkItem"><input id="langPt" type="checkbox" checked> Português</label>','<label class="checkItem" style="opacity:.5"><input id="langFr" type="checkbox" disabled> Français — قريبًا</label><label class="checkItem" style="opacity:.5"><input id="langEn" type="checkbox" disabled> English — قريبًا</label><label class="checkItem" style="opacity:.5"><input id="langPt" type="checkbox" disabled> Português — قريبًا</label>',1)

# Load/save support number.
a=a.replace("fill('setBankName',d.bankName||'');","fill('setSupportWhatsApp',d.supportWhatsApp||'');fill('setBankName',d.bankName||'');",1)
old_save="deliveryRates,bankName:$('setBankName').value.trim(),bankHolder:$('setBankHolder').value.trim(),bankAccount:$('setBankAccount').value.trim(),maintenance:$('setMaintenance').value==='true',updatedAt:serverTimestamp()"
new_save="deliveryRates,supportWhatsApp:$('setSupportWhatsApp').value.trim(),bankName:$('setBankName').value.trim(),bankHolder:$('setBankHolder').value.trim(),bankAccount:$('setBankAccount').value.trim(),maintenance:$('setMaintenance').value==='true',updatedAt:serverTimestamp()"
assert old_save in a, 'admin settings save anchor missing'
a=a.replace(old_save,new_save,1)

# Save Arabic only until translations are ready.
old_langsave="window.saveLanguageSettings=async()=>{try{await setDoc(doc(db,'storeSettings','language'),{defaultLang:$('langDefault').value,ar:$('langAr').checked,fr:$('langFr').checked,en:$('langEn').checked,pt:$('langPt').checked,updatedAt:serverTimestamp()},{merge:true});$('langMsg').textContent='تم حفظ إعدادات اللغة.'}catch(e){$('langMsg').textContent='تعذر الحفظ: '+e.message}};"
new_langsave="window.saveLanguageSettings=async()=>{try{await setDoc(doc(db,'storeSettings','language'),{defaultLang:'ar',ar:true,fr:false,en:false,pt:false,updatedAt:serverTimestamp()},{merge:true});$('langMsg').textContent='تم حفظ العربية كلغة المتجر الحالية.'}catch(e){$('langMsg').textContent='تعذر الحفظ: '+e.message}};"
assert old_langsave in a, 'admin language save anchor missing'
a=a.replace(old_langsave,new_langsave,1)

# Avoid old misleading section title in admin content editor.
a=a.replace('value="الأكثر طلبًا"','value="منتجاتنا"',1)
a=a.replace("['ctProductsTitle', 'productsTitle', 'الأكثر طلبًا']","['ctProductsTitle', 'productsTitle', 'منتجاتنا']",1)
a=a.replace("function applyAdminContent(d){CONTENT_TEXT_FIELDS.forEach","function applyAdminContent(d){if(d.productsTitle==='الأكثر طلبًا')d={...d,productsTitle:'منتجاتنا'};CONTENT_TEXT_FIELDS.forEach",1)

p.write_text(a,encoding='utf-8')
