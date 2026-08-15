from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# Account page.
old='<main id="accountPage" class="page"><div class="page-head"><h1>حسابي</h1><p>إدارة بيانات حساب MauriOne.</p></div><div class="box"><div class="field"><label>الاسم</label><input id="accountName"></div><div class="field"><label>رقم الهاتف</label><input id="accountPhone" inputmode="tel"></div><div class="field"><label>المدينة</label><input id="accountCity"></div><div class="field"><label>العنوان</label><input id="accountAddress"></div><button class="primary" onclick="saveAccount()">حفظ البيانات</button><div id="accountStatus" class="notice" style="display:none"></div></div></main>'
new='<main id="accountPage" class="page"><div class="page-head"><h1>حسابي</h1><p>حساب MauriOne يحفظ بياناتك وطلباتك على جميع أجهزتك.</p></div><div class="box"><div id="accountLoggedOut"><div class="account-auth"><div class="account-avatar">M</div><h2>تسجيل الدخول إلى MauriOne</h2><p>سجّل الدخول حتى تبقى طلباتك محفوظة ويمكنك متابعتها من أي جهاز.</p><button id="customerLoginBtn" class="primary" onclick="customerLogin()">المتابعة باستخدام Google</button><div id="customerLoginMsg" class="notice" style="display:none"></div></div></div><div id="accountLoggedIn" style="display:none"><div class="account-user"><div><small>الحساب</small><strong id="accountEmail"></strong></div><button class="account-logout" onclick="customerLogout()">تسجيل الخروج</button></div><div class="field"><label>الاسم</label><input id="accountName"></div><div class="field"><label>رقم الهاتف</label><input id="accountPhone" inputmode="tel"></div><div class="field"><label>المدينة</label><input id="accountCity"></div><div class="field"><label>العنوان</label><input id="accountAddress"></div><button class="primary" onclick="saveAccount()">حفظ البيانات</button><div id="accountStatus" class="notice" style="display:none"></div></div></div></main>'
if old not in s: raise SystemExit('account page marker missing')
s=s.replace(old,new,1)

# Styling.
marker='.proof-field{display:none;'
css='.account-auth{text-align:center;padding:10px 2px}.account-avatar{width:64px;height:64px;border-radius:20px;margin:0 auto 14px;background:linear-gradient(145deg,var(--navy),#17324c);color:var(--gold);display:grid;place-items:center;font-size:28px;font-weight:900}.account-auth h2{font-size:20px}.account-auth p{color:var(--muted);font-size:10px;line-height:1.8;margin:8px auto 14px;max-width:310px}.account-user{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px;background:var(--soft);border-radius:13px;margin-bottom:16px}.account-user small{display:block;color:var(--muted);font-size:8px}.account-user strong{display:block;margin-top:3px;font-size:10px;direction:ltr;text-align:right}.account-logout{border:1px solid var(--line);background:#fff;border-radius:9px;padding:8px 10px;font-size:9px}'
if marker not in s: raise SystemExit('style marker missing')
s=s.replace(marker,css+marker,1)

# Firebase imports/init.
old="import { getFirestore, collection, onSnapshot, doc, writeBatch, serverTimestamp } from 'https://www.gstatic.com/firebasejs/12.16.0/firebase-firestore.js';"
new="import { getFirestore, collection, onSnapshot, doc, writeBatch, serverTimestamp, setDoc, query, where } from 'https://www.gstatic.com/firebasejs/12.16.0/firebase-firestore.js';\nimport { getAuth, GoogleAuthProvider, signInWithPopup, signInWithRedirect, onAuthStateChanged, signOut } from 'https://www.gstatic.com/firebasejs/12.16.0/firebase-auth.js';"
if old not in s: raise SystemExit('import marker missing')
s=s.replace(old,new,1)
old="const app=initializeApp(firebaseConfig),db=getFirestore(app);"
new="const app=initializeApp(firebaseConfig),db=getFirestore(app),auth=getAuth(app),provider=new GoogleAuthProvider();provider.setCustomParameters({prompt:'select_account'});"
if old not in s: raise SystemExit('init marker missing')
s=s.replace(old,new,1)

# State.
old="let orderHistory=JSON.parse(localStorage.getItem('MauriOne_orders')||'[]');\nconst trackingUnsubs=new Map();"
new="let orderHistory=JSON.parse(localStorage.getItem('MauriOne_orders')||'[]'),currentUser=null,customerOrdersUnsub=null,customerProfileUnsub=null;\nconst trackingUnsubs=new Map();"
if old not in s: raise SystemExit('state marker missing')
s=s.replace(old,new,1)

# Replace all old local-only account helpers up to the language helper.
account_code="""function account(){try{return JSON.parse(localStorage.getItem('MauriOne_account')||'{}')}catch{return {}}\nfunction setAccountUI(){const out=document.getElementById('accountLoggedOut'),inside=document.getElementById('accountLoggedIn');if(!out||!inside)return;out.style.display=currentUser?'none':'block';inside.style.display=currentUser?'block':'none';if(currentUser)document.getElementById('accountEmail').textContent=currentUser.email||''}\nfunction loadAccount(){const a=account();document.getElementById('accountName').value=a.name||currentUser?.displayName||'';document.getElementById('accountPhone').value=a.phone||'';document.getElementById('accountCity').value=a.city||'';document.getElementById('accountAddress').value=a.address||'';setAccountUI()}\nwindow.customerLogin=async()=>{const btn=document.getElementById('customerLoginBtn'),msg=document.getElementById('customerLoginMsg');btn.disabled=true;msg.style.display='block';msg.textContent='جاري فتح تسجيل الدخول...';try{await signInWithPopup(auth,provider)}catch(e){if(e.code==='auth/popup-blocked'||e.code==='auth/cancelled-popup-request')await signInWithRedirect(auth,provider);else{msg.textContent='تعذر تسجيل الدخول. حاول مرة أخرى.';console.error(e)}}finally{btn.disabled=false}};\nwindow.customerLogout=()=>signOut(auth);\nwindow.saveAccount=async()=>{if(!currentUser)return customerLogin();const a={uid:currentUser.uid,email:currentUser.email||'',name:document.getElementById('accountName').value.trim(),phone:document.getElementById('accountPhone').value.trim(),city:document.getElementById('accountCity').value.trim(),address:document.getElementById('accountAddress').value.trim()};const st=document.getElementById('accountStatus');st.style.display='block';st.textContent='جاري الحفظ...';try{await setDoc(doc(db,'customerAccounts',currentUser.uid),{...a,updatedAt:serverTimestamp()},{merge:true});localStorage.setItem('MauriOne_account',JSON.stringify(a));st.className='notice success';st.textContent='تم حفظ بيانات الحساب في MauriOne.'}catch(e){console.error(e);st.className='notice';st.textContent='تعذر حفظ البيانات. حاول مرة أخرى.'}};\nfunction watchCustomerProfile(){if(customerProfileUnsub){customerProfileUnsub();customerProfileUnsub=null}if(!currentUser){loadAccount();return}customerProfileUnsub=onSnapshot(doc(db,'customerAccounts',currentUser.uid),snap=>{const d=snap.data()||{},local=account(),a={...local,...d};localStorage.setItem('MauriOne_account',JSON.stringify(a));document.getElementById('accountName').value=a.name||currentUser.displayName||'';document.getElementById('accountPhone').value=a.phone||'';document.getElementById('accountCity').value=a.city||'';document.getElementById('accountAddress').value=a.address||''},e=>console.warn('Customer profile:',e.code||e.message))}\nfunction watchCustomerOrders(){if(customerOrdersUnsub){customerOrdersUnsub();customerOrdersUnsub=null}if(!currentUser){orderHistory=JSON.parse(localStorage.getItem('MauriOne_orders')||'[]');renderMyOrders();connectTracking();return}const q=query(collection(db,'orders'),where('customerUid','==',currentUser.uid));customerOrdersUnsub=onSnapshot(q,snap=>{const cloud=snap.docs.map(d=>({id:d.id,...d.data()})).sort((a,b)=>(b.createdAt?.seconds||0)-(a.createdAt?.seconds||0));const legacy=JSON.parse(localStorage.getItem('MauriOne_orders')||'[]').filter(x=>!cloud.some(c=>c.id===x.id));orderHistory=[...cloud,...legacy];renderMyOrders();connectTracking()},e=>{console.warn('Customer orders:',e.code||e.message);renderMyOrders()})}\nonAuthStateChanged(auth,u=>{currentUser=u||null;setAccountUI();if(currentUser){const local=account();if(!local.name&&currentUser.displayName)local.name=currentUser.displayName;if(!local.email)local.email=currentUser.email||'';localStorage.setItem('MauriOne_account',JSON.stringify(local))}watchCustomerProfile();watchCustomerOrders();if(document.getElementById('accountPage')?.classList.contains('active'))loadAccount()});\n"""
pat=r"function account\(\)\{.*?(?=window\.openLanguages=)"
s2,n=re.subn(pat,lambda m:account_code,s,count=1,flags=re.S)
if n!=1: raise SystemExit(f'account regex marker missing: {n}')
s=s2

# Checkout requires account.
old="window.checkout=()=>{if(generalSettings.maintenance===true)return alert('المتجر في وضع الصيانة حاليًا. حاول لاحقًا.');if(!cartRows().length)return alert('السلة فارغة');const a=account();"
new="window.checkout=()=>{if(generalSettings.maintenance===true)return alert('المتجر في وضع الصيانة حاليًا. حاول لاحقًا.');if(!cartRows().length)return alert('السلة فارغة');if(!currentUser){openStore('accountPage','navAccount');setTimeout(()=>alert('سجّل الدخول أولًا لإتمام الطلب وحفظه في حسابك.'),80);return}const a=account();"
if old not in s: raise SystemExit('checkout marker missing')
s=s.replace(old,new,1)

# Bind new orders to the authenticated customer.
old="batch.set(orderRef,{orderNo,customer,items,total,payment:coPayment.value,paymentProofUrl,status:'new',createdAt:serverTimestamp()});batch.set(doc(db,'orderTracking',orderRef.id),{orderNo,status:'new',estimatedDelivery:'',updatedAt:serverTimestamp()});"
new="batch.set(orderRef,{orderNo,customerUid:currentUser.uid,customerEmail:currentUser.email||'',customer,items,total,payment:coPayment.value,paymentProofUrl,status:'new',createdAt:serverTimestamp()});batch.set(doc(db,'orderTracking',orderRef.id),{orderNo,customerUid:currentUser.uid,status:'new',estimatedDelivery:'',updatedAt:serverTimestamp()});"
if old not in s: raise SystemExit('order marker missing')
s=s.replace(old,new,1)
old="orderHistory.unshift({id:orderRef.id,orderNo,items,total,payment:coPayment.value,status:'new',estimatedDelivery:'',updatedAt:new Date().toLocaleString('ar'),createdAt:Date.now()});"
new="orderHistory.unshift({id:orderRef.id,orderNo,customerUid:currentUser.uid,items,total,payment:coPayment.value,status:'new',estimatedDelivery:'',updatedAt:new Date().toLocaleString('ar'),createdAt:Date.now()});"
if old not in s: raise SystemExit('cache marker missing')
s=s.replace(old,new,1)

p.write_text(s)
print('customer account v2 applied')
