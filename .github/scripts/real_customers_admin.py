from pathlib import Path

p = Path('admin.html')
s = p.read_text(encoding='utf-8')

def rep(old, new, label):
    global s
    if old not in s:
        raise SystemExit('Missing pattern: ' + label)
    s = s.replace(old, new, 1)

# Small UI helpers for customer cards.
css_old = '.templateHint{font-size:9px;color:#888;margin-top:-5px;line-height:1.6}.stickyActions'
css_new = '.templateHint{font-size:9px;color:#888;margin-top:-5px;line-height:1.6}.customerSource{display:inline-flex;align-items:center;padding:4px 7px;border-radius:20px;background:#eef5ff;color:#225d9b;font-size:8px;font-weight:800}.customerSource.manual{background:#f5f5f7;color:#666}.customerInfo{margin-top:9px;display:grid;gap:5px;font-size:10px;color:#666}.customerInfo b{color:#111}.customerStats{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}.customerStat{background:#f6f6f8;border-radius:9px;padding:7px 9px;font-size:9px}.stickyActions'
rep(css_old, css_new, 'customer CSS')

old_section = '<section id="customers" class="page"><div class="panel"><h2>تسجيل زبون</h2><div class="field"><label>الاسم</label><input id="cName"></div><div class="field"><label>الهاتف</label><input id="cPhone"></div><div class="field"><label>WhatsApp</label><input id="cWhats"></div><div class="field"><label>المدينة</label><input id="cCity"></div><div class="field"><label>العنوان</label><input id="cAddress"></div><button id="saveCustomer" class="primary">حفظ الزبون</button></div><div class="panel"><div id="customerList"></div></div></section>'
new_section = '''<section id="customers" class="page"><div class="panel"><div class="sectionTitle"><h2>كل الزبناء</h2><span id="customerPageCount" class="count">0</span></div><p class="adminHint">تظهر هنا حسابات الزبناء المسجلين فعليًا في MauriOne، بالإضافة إلى الزبناء الذين تضيفهم يدويًا. الحسابات المكررة حسب البريد أو الهاتف تُعرض مرة واحدة.</p><div class="customerStats"><span class="customerStat">حسابات المتجر: <b id="registeredCustomerCount">0</b></span><span class="customerStat">سجل يدوي: <b id="manualCustomerCount">0</b></span></div><div id="customerList"></div></div><div class="panel"><details class="contentGroup"><summary>إضافة زبون يدوي</summary><div class="contentBody"><div class="field"><label>الاسم</label><input id="cName"></div><div class="field"><label>الهاتف</label><input id="cPhone"></div><div class="field"><label>WhatsApp</label><input id="cWhats"></div><div class="field"><label>المدينة</label><input id="cCity"></div><div class="field"><label>العنوان</label><input id="cAddress"></div><button id="saveCustomer" class="primary">حفظ الزبون</button></div></details></div></section>'''
rep(old_section, new_section, 'customers section')

rep("let pub=[],priv={},products=[],orders=[],suppliers=[],customers=[],started=false;", "let pub=[],priv={},products=[],orders=[],suppliers=[],customers=[],customerAccounts=[],started=false;", 'state vars')

old_start = "function start(){if(started)return;started=true;onSnapshot(collection(db,'products'),s=>{pub=s.docs.map(d=>({id:d.id,...d.data()}));merge()});onSnapshot(collection(db,'product_private'),s=>{priv={};s.docs.forEach(d=>priv[d.id]=d.data());merge()});onSnapshot(collection(db,'orders'),s=>{orders=s.docs.map(d=>({id:d.id,...d.data()})).sort((a,b)=>(b.createdAt?.seconds||0)-(a.createdAt?.seconds||0));render()});onSnapshot(collection(db,'suppliers'),s=>{suppliers=s.docs.map(d=>({id:d.id,...d.data()}));render()});onSnapshot(collection(db,'customers'),s=>{customers=s.docs.map(d=>({id:d.id,...d.data()}));render()})}function merge(){products=pub.map(p=>({...p,...(priv[p.id]||{})}));render()}"
new_start = "function start(){if(started)return;started=true;onSnapshot(collection(db,'products'),s=>{pub=s.docs.map(d=>({id:d.id,...d.data()}));merge()});onSnapshot(collection(db,'product_private'),s=>{priv={};s.docs.forEach(d=>priv[d.id]=d.data());merge()});onSnapshot(collection(db,'orders'),s=>{orders=s.docs.map(d=>({id:d.id,...d.data()})).sort((a,b)=>(b.createdAt?.seconds||0)-(a.createdAt?.seconds||0));render()});onSnapshot(collection(db,'suppliers'),s=>{suppliers=s.docs.map(d=>({id:d.id,...d.data()}));render()});onSnapshot(collection(db,'customers'),s=>{customers=s.docs.map(d=>({id:d.id,...d.data()}));render()});onSnapshot(collection(db,'customerAccounts'),s=>{customerAccounts=s.docs.map(d=>({id:d.id,...d.data()}));render()},e=>console.warn('Customer accounts:',e.code||e.message))}function merge(){products=pub.map(p=>({...p,...(priv[p.id]||{})}));render()}"
rep(old_start, new_start, 'start subscriptions')

render_marker = 'function render(){const active='
helpers = '''function normPhone(v){return String(v||'').replace(/\\D/g,'')}
function allCustomerRows(){const rows=[...customerAccounts.map(c=>({...c,_source:'account'})),...customers.map(c=>({...c,_source:'manual'}))],seen=new Set(),out=[];for(const c of rows){const email=String(c.email||'').trim().toLowerCase(),phone=normPhone(c.phone||c.whats),key=email?'e:'+email:phone?'p:'+phone:c.uid?'u:'+c.uid:'i:'+String(c.id||Math.random());if(seen.has(key))continue;seen.add(key);out.push(c)}return out}
function customerOrderCount(c){const email=String(c.email||'').trim().toLowerCase(),phone=normPhone(c.phone||c.whats);return orders.filter(o=>{const oc=o.customer||{};return(c.uid&&String(o.customerUid||'')===String(c.uid))||(email&&String(o.customerEmail||'').trim().toLowerCase()===email)||(phone&&normPhone(oc.phone)===phone)}).length}
function customerSpend(c){const email=String(c.email||'').trim().toLowerCase(),phone=normPhone(c.phone||c.whats);return orders.filter(o=>{const oc=o.customer||{};return(c.uid&&String(o.customerUid||'')===String(c.uid))||(email&&String(o.customerEmail||'').trim().toLowerCase()===email)||(phone&&normPhone(oc.phone)===phone)}).filter(o=>o.status==='delivered').reduce((sum,o)=>sum+Number(o.total||0),0)}
function customerCards(){const rows=allCustomerRows();$('customerPageCount')&&($('customerPageCount').textContent=rows.length);$('registeredCustomerCount')&&($('registeredCustomerCount').textContent=customerAccounts.length);$('manualCustomerCount')&&($('manualCustomerCount').textContent=customers.length);if(!rows.length)return'<div class="empty">لا يوجد زبناء بعد.</div>';return rows.map(c=>{const source=c._source==='account'?'حساب MauriOne':'سجل يدوي',sourceClass=c._source==='manual'?' manual':'',name=c.name||String(c.email||'').split('@')[0]||'زبون',email=c.email||'',phone=c.phone||c.whats||'',city=c.city||'',address=c.address||'',ordersCount=customerOrderCount(c),spent=customerSpend(c);return`<div class="card"><div class="row"><b>${esc(name)}</b><span class="customerSource${sourceClass}">${source}</span></div><div class="customerInfo">${email?`<div>البريد: <b dir="ltr">${esc(email)}</b></div>`:''}${phone?`<div>الهاتف: <b dir="ltr">${esc(phone)}</b></div>`:''}${city?`<div>المدينة: <b>${esc(city)}</b></div>`:''}${address?`<div>العنوان: <b>${esc(address)}</b></div>`:''}</div><div class="customerStats"><span class="customerStat">الطلبات: <b>${ordersCount}</b></span><span class="customerStat">المشتريات المكتملة: <b>${Number(spent).toLocaleString()} MRU</b></span></div>${phone?`<a class="secondary" style="display:block;text-align:center;text-decoration:none;margin-top:10px" href="tel:${esc(phone)}">اتصال</a>`:''}</div>`}).join('')}
'''
if render_marker not in s:
    raise SystemExit('Missing render marker')
s = s.replace(render_marker, helpers + render_marker, 1)

rep("$('nCustomers').textContent=customers.length;", "$('nCustomers').textContent=allCustomerRows().length;", 'dashboard customer count')

old_list = "$('customerList').innerHTML=customers.map(c=>`<div class=\"card\"><b>${esc(c.name)}</b><br>${esc(c.phone||'—')}<br>${esc(c.city||'—')}</div>`).join('')||'لا يوجد زبناء.';"
new_list = "$('customerList').innerHTML=customerCards();"
rep(old_list, new_list, 'customer cards render')

p.write_text(s, encoding='utf-8')
print('Real customer accounts admin patched')
