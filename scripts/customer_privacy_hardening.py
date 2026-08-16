from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

repls = [
("let orderHistory=JSON.parse(localStorage.getItem('MauriOne_orders')||'[]'),currentUser=null,customerOrdersUnsub=null,customerProfileUnsub=null;",
 "let orderHistory=[],currentUser=null,customerOrdersUnsub=null,customerProfileUnsub=null;"),
("const trackingUnsubs=new Map();",
 "const trackingUnsubs=new Map();\nfunction resetTrackingSubscriptions(){for(const unsub of trackingUnsubs.values()){try{unsub()}catch{}}trackingUnsubs.clear()}"),
("const saveOrders=()=>localStorage.setItem('MauriOne_orders',JSON.stringify(orderHistory));",
 "const saveOrders=()=>{if(!currentUser)localStorage.setItem('MauriOne_orders',JSON.stringify(orderHistory))};"),
("function account(){try{return JSON.parse(localStorage.getItem('MauriOne_account')||'{}')}catch{return {}}}",
 "function account(){try{const a=JSON.parse(localStorage.getItem('MauriOne_account')||'{}');if(currentUser){if(!a.uid||String(a.uid)!==String(currentUser.uid))return {};if(a.email&&currentUser.email&&String(a.email).toLowerCase()!==String(currentUser.email).toLowerCase())return {}}return a}catch{return {}}}"),
("function watchCustomerOrders(){if(customerOrdersUnsub){customerOrdersUnsub();customerOrdersUnsub=null}if(!currentUser){orderHistory=JSON.parse(localStorage.getItem('MauriOne_orders')||'[]');renderMyOrders();connectTracking();return}const q=query(collection(db,'orders'),where('customerUid','==',currentUser.uid));customerOrdersUnsub=onSnapshot(q,snap=>{const cloud=snap.docs.map(d=>({id:d.id,...d.data()})).sort((a,b)=>(b.createdAt?.seconds||0)-(a.createdAt?.seconds||0));const legacy=JSON.parse(localStorage.getItem('MauriOne_orders')||'[]').filter(x=>!cloud.some(c=>c.id===x.id));orderHistory=[...cloud,...legacy];renderMyOrders();connectTracking()},e=>{console.warn('Customer orders:',e.code||e.message);renderMyOrders()})}",
 "function watchCustomerOrders(){if(customerOrdersUnsub){customerOrdersUnsub();customerOrdersUnsub=null}resetTrackingSubscriptions();if(!currentUser){orderHistory=[];renderMyOrders();return}const uid=currentUser.uid,q=query(collection(db,'orders'),where('customerUid','==',uid));customerOrdersUnsub=onSnapshot(q,snap=>{if(!currentUser||currentUser.uid!==uid)return;orderHistory=snap.docs.map(d=>({id:d.id,...d.data()})).sort((a,b)=>(b.createdAt?.seconds||0)-(a.createdAt?.seconds||0));renderMyOrders();connectTracking()},e=>{console.warn('Customer orders:',e.code||e.message);if(currentUser&&currentUser.uid===uid){orderHistory=[];renderMyOrders()}})}")
]

for old, new in repls:
    if old not in s:
        raise SystemExit('Target not found: ' + old[:120])
    s = s.replace(old, new, 1)

# Guard against reintroducing signed-in legacy order mixing.
if "const legacy=JSON.parse(localStorage.getItem('MauriOne_orders')" in s:
    raise SystemExit('Legacy order merge still present')

p.write_text(s, encoding='utf-8')
print('Customer privacy hardening applied')
