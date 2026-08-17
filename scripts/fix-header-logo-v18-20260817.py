from pathlib import Path

p=Path('index.html')
html=p.read_text(encoding='utf-8')
marker='/* MauriOne header logo v18 */'
css=r'''
/* MauriOne header logo v18 */
header .logo{
  padding:0!important;
  min-width:0!important;
}
header .logo .brand{
  gap:5px!important;
  align-items:center!important;
}
header .logo .mark{
  width:22px!important;
  height:29px!important;
  flex:0 0 22px!important;
}
header .logo .mark i{
  width:13px!important;
  height:18px!important;
  border-radius:2.5px!important;
}
header .logo .brand-name{
  font-size:14px!important;
  line-height:1!important;
  font-weight:700!important;
  letter-spacing:-.15px!important;
  white-space:nowrap!important;
}
@media(max-width:390px){
  header .logo .mark{width:20px!important;height:27px!important;flex-basis:20px!important}
  header .logo .mark i{width:12px!important;height:17px!important}
  header .logo .brand-name{font-size:13px!important}
}
'''
if marker not in html:
    html=html.replace('</style>',css+'\n</style>',1)
p.write_text(html,encoding='utf-8')
assert marker in html
print('header logo resized')
