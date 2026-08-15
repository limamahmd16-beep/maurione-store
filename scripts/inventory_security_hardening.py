from pathlib import Path

p=Path('index.html')
s=p.read_text()
old="const items=rows.map(({p,qty})=>({productId:String(p.id),name:String(p.name||''),price:Number(p.price||0),qty:Number(qty||1),image:Array.isArray(p.images)&&p.images[0]?String(p.images[0]):''}));const total=items.reduce((sum,x)=>sum+x.price*x.qty,0),orderNo='MO-'+String(Date.now()).slice(-6);"
new="const items=rows.map(({p,qty})=>({productId:String(p.id),name:String(p.name||''),price:Number(p.price||0),qty:Number(qty||1),image:Array.isArray(p.images)&&p.images[0]?String(p.images[0]):''})),inventory={};items.forEach(i=>inventory[i.productId]=i.qty);const total=items.reduce((sum,x)=>sum+x.price*x.qty,0),orderNo='MO-'+String(Date.now()).slice(-6);"
if old not in s: raise SystemExit('items marker missing')
s=s.replace(old,new,1)
old="status:'new',inventoryManaged:true,createdAt:serverTimestamp()"
new="status:'new',inventoryManaged:true,inventory,createdAt:serverTimestamp()"
if old not in s: raise SystemExit('order inventory marker missing')
s=s.replace(old,new,1)
old="updates.forEach(u=>tx.update(u.ref,{stock:u.stock,updatedAt:serverTimestamp()}))"
new="updates.forEach(u=>tx.update(u.ref,{stock:u.stock,updatedAt:serverTimestamp(),lastInventoryOrderId:orderRef.id}))"
if old not in s: raise SystemExit('product inventory marker missing')
s=s.replace(old,new,1)
p.write_text(s)
print('inventory security hardening applied')
