from pathlib import Path
p=Path('index.html')
html=p.read_text(encoding='utf-8')
marker='/* MauriOne header mark v19 */'
css=r'''
/* MauriOne header mark v19 */
header .logo .mark{
  width:18px!important;
  height:24px!important;
  flex:0 0 18px!important;
  transform:scale(.88)!important;
  transform-origin:center!important;
}
header .logo .mark i{
  width:11px!important;
  height:15px!important;
}
@media(max-width:390px){
  header .logo .mark{width:17px!important;height:23px!important;flex-basis:17px!important;transform:scale(.84)!important}
  header .logo .mark i{width:10px!important;height:14px!important}
}
'''
if marker not in html:
    html=html.replace('</style>',css+'\n</style>',1)
p.write_text(html,encoding='utf-8')
assert marker in html
print('header mark resized')
