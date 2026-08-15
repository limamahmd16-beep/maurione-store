from pathlib import Path
import re

# Storefront reservation ledger
p=Path('index.html')
s=p.read_text()
old="const orderRef=doc(collection(db,'orders')),trackingRef=doc(db,'orderTracking',orderRef.id),productRefs=items.map(i=>doc(db,'products',i.productId));"
new="const orderRef=doc(collection(db,'orders')),trackingRef=doc(db,'orderTracking',orderRef.id),productRefs=items.map(i=>doc(db,'products',i.productId)),reservationRows=items.map(i=>{const id=orderRef.id+'_'+i.productId;return{id,ref:doc(db,'inventoryReservations',id),item:i}});"
if old not in s: raise SystemExit('store order refs marker missing')
s=s.replace(old,new,1)
old="const items=rows.map(({p,qty})=>({productId:String(p.id),name:String(p.name||''),price:Number(p.price||0),qty:Number(qty||1),image:Array.isArray(p.images)&&p.images[0]?String(p.images[0]):''})),inventory={};items.forEach(i=>inventory[i.productId]=i.qty);const total=items.reduce((sum,x)=>sum+x.price*x.qty,0),orderNo='MO-'+String(Date.now()).slice(-6);"
new="const items=rows.map(({p,qty})=>({productId:String(p.id),name:String(p.name||''),price:Number(p.price||0),qty:Number(qty||1),image:Array.isArray(p.images)&&p.images[0]?String(p.images[0]):''})),inventory={};if(items.length>8){checkoutStatus.style.display='block';checkoutStatus.className='notice';checkoutStatus.textContent='يمكن إتمام حتى 8 منتجات مختلفة في الطلب الواحد. قسّم السلة إلى طلبين.';return}items.forEach(i=>inventory[i.productId]=i.qty);const total=items.reduce((sum,x)=>sum+x.price*x.qty,0),orderNo='MO-'+String(Date.now()).slice(-6);"
if old not in s: raise SystemExit('store items marker missing')
s=s.replace(old,new,1)
old="updates.forEach(u=>tx.update(u.ref,{stock:u.stock,updatedAt:serverTimestamp(),lastInventoryOrderId:orderRef.id}))"
new="updates.forEach((u,i)=>{const r=reservationRows[i],item=items[i];tx.set(r.ref,{orderId:orderRef.id,productId:item.productId,customerUid:currentUser.uid,qty:item.qty,state:'reserved',createdAt:serverTimestamp()});tx.update(u.ref,{stock:u.stock,updatedAt:serverTimestamp(),lastInventoryReservationId:r.id})})"
if old not in s: raise SystemExit('store product inventory write marker missing')
s=s.replace(old,new,1)
p.write_text(s)

# Admin: restore/consume only actual reservations
p=Path('admin.html')
s=p.read_text()
new_progress="""window.saveProgress=async id=>{const o=orders.find(x=>x.id===id);if(!o)return;const st=$('st').value,eta=$('eta').value||'',btn=$('saveProgress'),msg=$('progressMsg');btn.disabled=true;msg.className='';msg.textContent='جاري الحفظ...';try{let inventoryChanged=false;await runTransaction(db,async tx=>{const orderRef=doc(db,'orders',id),orderSnap=await tx.get(orderRef);if(!orderSnap.exists())throw new Error('الطلب غير موجود');const live={id,...orderSnap.data()};if((live.status==='cancelled'||live.status==='delivered')&&st!==live.status)throw new Error('الطلب الملغي أو المكتمل نهائي ولا يمكن إعادة فتحه.');const manageInventory=live.inventoryManaged===true&&(st==='cancelled'||st==='delivered')&&live.status!==st;const itemRows=Array.isArray(live.items)?live.items.filter(i=>i?.productId&&Number(i.qty||0)>0):[],reservations=[],productRows=[];if(manageInventory){for(const item of itemRows){const reservationId=id+'_'+String(item.productId),reservationRef=doc(db,'inventoryReservations',reservationId),reservationSnap=await tx.get(reservationRef);if(reservationSnap.exists()&&reservationSnap.data().state==='reserved'){const r=reservationSnap.data();reservations.push({ref:reservationRef,data:r});if(st==='cancelled'){const productRef=doc(db,'products',String(r.productId)),productSnap=await tx.get(productRef);if(productSnap.exists())productRows.push({ref:productRef,stock:Number(productSnap.data().stock||0),qty:Number(r.qty||0)})}}}}tx.update(orderRef,{status:st,estimatedDelivery:eta,updatedAt:serverTimestamp()});tx.set(doc(db,'orderTracking',id),{orderNo:live.orderNo||id,status:st,estimatedDelivery:eta,updatedAt:serverTimestamp()},{merge:true});if(manageInventory&&st==='cancelled'){productRows.forEach(p=>tx.update(p.ref,{stock:p.stock+p.qty,updatedAt:serverTimestamp()}));reservations.forEach(r=>tx.update(r.ref,{state:'released',releasedAt:serverTimestamp()}));if(reservations.length)inventoryChanged=true}else if(manageInventory&&st==='delivered'){reservations.forEach(r=>tx.update(r.ref,{state:'consumed',consumedAt:serverTimestamp()}));if(reservations.length)inventoryChanged=true}});o.status=st;o.estimatedDelivery=eta;render();msg.className='ok';if(st==='cancelled')msg.textContent=inventoryChanged?'تم إلغاء الطلب وإعادة الكمية المحجوزة إلى المخزون.':'تم إلغاء الطلب.';else if(st==='delivered')msg.textContent='تم التسليم ونُقل الطلب إلى الطلبات المكتملة.';else msg.textContent='تم الحفظ وسيظهر للزبون.';if(st==='delivered'||st==='cancelled')setTimeout(()=>{closeOrder();openPage('orders','navOrders')},450)}catch(e){msg.textContent='تعذر الحفظ: '+(e.message||e)}finally{btn.disabled=false}};"""
pat=r"window\.saveProgress=async id=>\{.*?\};\n(?=function render\(\))"
s2,n=re.subn(pat,new_progress+'\n',s,count=1,flags=re.S)
if n!=1: raise SystemExit(f'admin saveProgress regex marker missing: {n}')
p.write_text(s2)
print('inventory reservations applied')
