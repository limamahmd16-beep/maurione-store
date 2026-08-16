from pathlib import Path

idx = Path('index.html')
adm = Path('admin.html')
i = idx.read_text(encoding='utf-8')
a = adm.read_text(encoding='utf-8')

# Storefront styles
style_anchor = ".delivery-note{margin-top:7px;font-size:9px;color:var(--muted);line-height:1.6}"
assert style_anchor in i
policy_css = style_anchor + ".policy-menu{margin-top:12px}.policy-menu h2{font-size:16px;margin-bottom:10px}.policy-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.policy-link{border:1px solid var(--line);background:#fff;border-radius:12px;padding:13px 10px;text-align:right;font-size:10px;font-weight:800}.policy-page{padding:18px 13px 34px}.policy-card{border:1px solid var(--line);border-radius:18px;background:#fff;padding:18px}.policy-card p{white-space:pre-wrap;line-height:2;color:#555;font-size:11px}.policy-back{border:0;background:var(--soft);border-radius:50%;width:38px;height:38px;font-size:20px;margin-bottom:12px}"
i = i.replace(style_anchor, policy_css, 1)

# Storefront account policy menu + policy page
account_tail = '<div id="accountStatus" class="notice" style="display:none"></div></div></div></main>\n<nav class="bottom-nav">'
assert account_tail in i
policy_markup = '''<div id="accountStatus" class="notice" style="display:none"></div></div></div><div class="box policy-menu"><h2>سياسات MauriOne</h2><div class="policy-grid"><button class="policy-link" onclick="openPolicy('returns')">سياسة الاسترجاع</button><button class="policy-link" onclick="openPolicy('shipping')">سياسة التوصيل</button><button class="policy-link" onclick="openPolicy('privacy')">سياسة الخصوصية</button><button class="policy-link" onclick="openPolicy('terms')">الشروط والأحكام</button></div></div></main>
<main id="policyPage" class="page"><div class="policy-page"><button class="policy-back" onclick="openStore('accountPage','navAccount')" aria-label="رجوع">×</button><div class="policy-card"><div class="page-head" style="padding:0 0 14px"><h1 id="policyPageTitle">سياسات MauriOne</h1></div><p id="policyPageBody"></p></div></div></main>
<nav class="bottom-nav">'''
i = i.replace(account_tail, policy_markup, 1)

# Content defaults
og_anchor = '"ogDescription":"تسوق الهواتف والكمبيوتر والإكسسوارات والساعات والسماعات من MauriOne."};'
assert og_anchor in i
policy_defaults = '"returnPolicy":"يتم التعامل مع طلبات الاسترجاع بحسب حالة المنتج وشروط البيع المرتبطة بالطلب. تواصل مع دعم MauriOne قبل إعادة أي منتج، ويجب أن يبقى المنتج وملحقاته بحالتها المناسبة للفحص.","shippingPolicy":"تظهر رسوم التوصيل للمدينة أو المنطقة المختارة قبل تأكيد الطلب. يتم تحديث حالة الطلب من MauriOne، وقد يختلف وقت التسليم بحسب المنطقة وتوفر خدمة التوصيل.","privacyPolicy":"تستخدم بيانات الحساب والطلب اللازمة لتشغيل المتجر، تنفيذ الطلبات، التوصيل، وخدمة الزبون. لا تعرض بيانات الطلبات لزبائن آخرين، ويمكن للزبون تسجيل الخروج من حسابه في أي وقت.","termsPolicy":"إرسال الطلب لا يعني إتمام التسليم تلقائيًا. يخضع الطلب لتوفر المخزون وصحة بيانات الزبون وإمكانية التوصيل. السعر النهائي الظاهر عند التأكيد يشمل المنتجات ورسوم التوصيل المحددة للمنطقة.",'+og_anchor
# avoid malformed duplicate quote start
policy_defaults = policy_defaults.replace(',"ogDescription"', ',"ogDescription"')
i = i.replace(og_anchor, policy_defaults, 1)

# Storefront policy function
fn_anchor = "window.customerLogout=()=>signOut(auth);"
assert fn_anchor in i
policy_fn = fn_anchor + "\nconst POLICY_MAP={returns:['سياسة الاسترجاع','returnPolicy'],shipping:['سياسة التوصيل','shippingPolicy'],privacy:['سياسة الخصوصية','privacyPolicy'],terms:['الشروط والأحكام','termsPolicy']};window.openPolicy=type=>{const row=POLICY_MAP[type]||POLICY_MAP.terms;document.getElementById('policyPageTitle').textContent=row[0];document.getElementById('policyPageBody').textContent=ct(row[1]);openStore('policyPage','navAccount')};"
i = i.replace(fn_anchor, policy_fn, 1)

# Admin content section before SEO
seo_section = '<details class="contentGroup"><summary>SEO وظهور الموقع</summary>'
assert seo_section in a
admin_policy_section = '''<details class="contentGroup"><summary>سياسات المتجر</summary><div class="contentBody"><p class="adminHint">هذه النصوص تظهر للزبون داخل «حسابي». عدّلها بما يطابق سياسة MauriOne الفعلية قبل الإطلاق التجاري.</p><div class="field"><label>سياسة الاسترجاع</label><textarea id="ctReturnPolicy">يتم التعامل مع طلبات الاسترجاع بحسب حالة المنتج وشروط البيع المرتبطة بالطلب. تواصل مع دعم MauriOne قبل إعادة أي منتج، ويجب أن يبقى المنتج وملحقاته بحالتها المناسبة للفحص.</textarea></div><div class="field"><label>سياسة التوصيل</label><textarea id="ctShippingPolicy">تظهر رسوم التوصيل للمدينة أو المنطقة المختارة قبل تأكيد الطلب. يتم تحديث حالة الطلب من MauriOne، وقد يختلف وقت التسليم بحسب المنطقة وتوفر خدمة التوصيل.</textarea></div><div class="field"><label>سياسة الخصوصية</label><textarea id="ctPrivacyPolicy">تستخدم بيانات الحساب والطلب اللازمة لتشغيل المتجر، تنفيذ الطلبات، التوصيل، وخدمة الزبون. لا تعرض بيانات الطلبات لزبائن آخرين، ويمكن للزبون تسجيل الخروج من حسابه في أي وقت.</textarea></div><div class="field"><label>الشروط والأحكام</label><textarea id="ctTermsPolicy">إرسال الطلب لا يعني إتمام التسليم تلقائيًا. يخضع الطلب لتوفر المخزون وصحة بيانات الزبون وإمكانية التوصيل. السعر النهائي الظاهر عند التأكيد يشمل المنتجات ورسوم التوصيل المحددة للمنطقة.</textarea></div></div></details>

'''+seo_section
a = a.replace(seo_section, admin_policy_section, 1)

# Admin content field registry
seo_field_anchor = "['ctSeoTitle', 'seoTitle', 'MauriOne | متجر الإلكترونيات والتقنية']"
assert seo_field_anchor in a
policy_fields = "['ctReturnPolicy', 'returnPolicy', 'يتم التعامل مع طلبات الاسترجاع بحسب حالة المنتج وشروط البيع المرتبطة بالطلب. تواصل مع دعم MauriOne قبل إعادة أي منتج، ويجب أن يبقى المنتج وملحقاته بحالتها المناسبة للفحص.'], ['ctShippingPolicy', 'shippingPolicy', 'تظهر رسوم التوصيل للمدينة أو المنطقة المختارة قبل تأكيد الطلب. يتم تحديث حالة الطلب من MauriOne، وقد يختلف وقت التسليم بحسب المنطقة وتوفر خدمة التوصيل.'], ['ctPrivacyPolicy', 'privacyPolicy', 'تستخدم بيانات الحساب والطلب اللازمة لتشغيل المتجر، تنفيذ الطلبات، التوصيل، وخدمة الزبون. لا تعرض بيانات الطلبات لزبائن آخرين، ويمكن للزبون تسجيل الخروج من حسابه في أي وقت.'], ['ctTermsPolicy', 'termsPolicy', 'إرسال الطلب لا يعني إتمام التسليم تلقائيًا. يخضع الطلب لتوفر المخزون وصحة بيانات الزبون وإمكانية التوصيل. السعر النهائي الظاهر عند التأكيد يشمل المنتجات ورسوم التوصيل المحددة للمنطقة.'], "+seo_field_anchor
a = a.replace(seo_field_anchor, policy_fields, 1)

idx.write_text(i, encoding='utf-8')
adm.write_text(a, encoding='utf-8')
print('policy patch applied')
