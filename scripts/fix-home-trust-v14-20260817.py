from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = '/* MauriOne home trust cleanup v14 */'
if marker in text:
    raise SystemExit('v14 already applied')

css = r'''

/* MauriOne home trust cleanup v14 */
#homePolicies{
  display:none!important;
}
#siteTrust{
  display:grid!important;
  grid-template-columns:repeat(2,minmax(0,1fr))!important;
  gap:10px!important;
  overflow:visible!important;
  padding:18px 12px 4px!important;
}
#siteTrust .trust-card{
  flex:none!important;
  min-width:0!important;
  width:auto!important;
  min-height:82px!important;
  margin:0!important;
}
@media(max-width:390px){
  #siteTrust{
    gap:8px!important;
    padding-left:10px!important;
    padding-right:10px!important;
  }
  #siteTrust .trust-card{
    min-height:78px!important;
  }
}
'''

needle = '</style>'
if needle not in text:
    raise SystemExit('style closing tag not found')
text = text.replace(needle, css + '\n' + needle, 1)
path.write_text(text, encoding='utf-8')
print('Applied MauriOne home trust cleanup v14')
