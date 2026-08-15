from pathlib import Path
p=Path('index.html')
s=p.read_text()
s2=s.replace("if(items.length>8){checkoutStatus.style.display='block';checkoutStatus.className='notice';checkoutStatus.textContent='يمكن إتمام حتى 8 منتجات مختلفة في الطلب الواحد. قسّم السلة إلى طلبين.';return}","if(items.length>6){checkoutStatus.style.display='block';checkoutStatus.className='notice';checkoutStatus.textContent='يمكن إتمام حتى 6 منتجات مختلفة في الطلب الواحد. قسّم السلة إلى طلبين.';return}",1)
if s2==s: raise SystemExit('inventory item limit marker missing')
p.write_text(s2)
print('inventory item limit set to 6')
