from pathlib import Path
p=Path('admin.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label):
    global s
    if old not in s:
        raise SystemExit('Missing pattern: '+label)
    s=s.replace(old,new,1)

old_section='<section id="orders" class="page"><div class="panel"><div class="sectionTitle"><h2>الطلبات الحالية</h2><span id="activeCount" class="count">0</span></div><div id="activeList"></div><div class="sectionTitle" style="border-top:1px solid #eee;padding-top:20px;margin-top:28px"><h2>الطلبات المكتملة</h2><span id="doneCount" class="count">0</span></div><div id="doneList"></div></div></section>'
new_section='<section id="orders" class="page"><div class="panel"><div class="sectionTitle"><h2>الطلبات الحالية</h2><span id="activeCount" class="count">0</span></div><div id="activeList"></div><div class="sectionTitle" style="border-top:1px solid #eee;padding-top:20px;margin-top:28px"><h2>الطلبات المكتملة</h2><span id="doneCount" class="count">0</span></div><div id="doneList"></div><div class="sectionTitle" style="border-top:1px solid #eee;padding-top:20px;margin-top:28px"><h2>الطلبات الملغاة</h2><span id="cancelledCount" class="count">0</span></div><div id="cancelledList"></div></div></section>'
rep(old_section,new_section,'orders section')

rep("function render(){const active=orders.filter(o=>o.status!=='delivered'),done=orders.filter(o=>o.status==='delivered'),", "function render(){const active=orders.filter(o=>o.status!=='delivered'&&o.status!=='cancelled'),done=orders.filter(o=>o.status==='delivered'),cancelled=orders.filter(o=>o.status==='cancelled'),", 'order buckets')

old="$('activeCount').textContent=active.length;$('doneCount').textContent=done.length;$('activeList').innerHTML=active.length?active.map(o=>card(o)).join(''):'<div class=\"empty\">لا توجد طلبات حالية.</div>';$('doneList').innerHTML=done.length?done.map(o=>card(o)).join(''):'<div class=\"empty\">لا توجد طلبات مكتملة بعد.</div>';const w="
new="$('activeCount').textContent=active.length;$('doneCount').textContent=done.length;$('cancelledCount').textContent=cancelled.length;$('activeList').innerHTML=active.length?active.map(o=>card(o)).join(''):'<div class=\"empty\">لا توجد طلبات حالية.</div>';$('doneList').innerHTML=done.length?done.map(o=>card(o)).join(''):'<div class=\"empty\">لا توجد طلبات مكتملة بعد.</div>';$('cancelledList').innerHTML=cancelled.length?cancelled.map(o=>card(o)).join(''):'<div class=\"empty\">لا توجد طلبات ملغاة.</div>';const w="
rep(old,new,'order lists render')

p.write_text(s,encoding='utf-8')
print('Cancelled orders separated successfully')
