from pathlib import Path

p = Path('index.html')
html = p.read_text(encoding='utf-8')

marker = '/* MauriOne checkout premium v17 */'
css = r'''
/* MauriOne checkout premium v17 */
.checkout-overlay{
  align-items:center!important;
  justify-content:center!important;
  padding:10px!important;
  background:rgba(7,21,34,.36)!important;
  backdrop-filter:blur(6px)!important;
  -webkit-backdrop-filter:blur(6px)!important;
}
.checkout-modal{
  width:min(620px,100%)!important;
  height:min(820px,calc(100dvh - 20px))!important;
  max-height:calc(100dvh - 20px)!important;
  border-radius:26px!important;
  background:#f5f6f8!important;
  overflow:auto!important;
  box-shadow:0 24px 80px rgba(7,21,34,.20)!important;
}
.checkout-top{
  min-height:64px!important;
  grid-template-columns:40px 1fr auto!important;
  padding:11px 14px!important;
  background:rgba(255,255,255,.97)!important;
  border-bottom:1px solid #eceef1!important;
}
.checkout-close{
  width:38px!important;
  height:38px!important;
  border-radius:12px!important;
  background:#f3f4f6!important;
  font-size:22px!important;
}
.checkout-title-wrap small{
  display:none!important;
}
.checkout-title-wrap h2{
  font-size:21px!important;
  font-weight:700!important;
  letter-spacing:-.2px!important;
}
.checkout-brand{
  font-size:11px!important;
  gap:3px!important;
  color:#25272b!important;
}
.checkout-brand .mark{
  transform:scale(.54)!important;
  width:24px!important;
}
.checkout-body{
  padding:10px 10px calc(12px + env(safe-area-inset-bottom))!important;
}
.checkout-section{
  margin-bottom:8px!important;
  padding:13px!important;
  border:1px solid #ebecef!important;
  border-radius:18px!important;
  background:#fff!important;
  box-shadow:none!important;
}
.checkout-section-head{
  gap:9px!important;
  margin-bottom:11px!important;
}
.checkout-section-icon{
  width:34px!important;
  height:34px!important;
  flex-basis:34px!important;
  border-radius:11px!important;
  background:#fbf7ef!important;
  border:1px solid #ead9b6!important;
}
.checkout-section-icon svg{
  width:18px!important;
  height:18px!important;
}
.checkout-section-head h3{
  font-size:14px!important;
  font-weight:700!important;
}
.checkout-section-head p{
  margin-top:1px!important;
  font-size:8px!important;
  color:#9a9ca1!important;
}
.checkout-grid{
  gap:8px!important;
}
.checkout-modal .field label{
  margin:0 3px 5px!important;
  font-size:8.5px!important;
  color:#777b82!important;
}
.checkout-modal .field input,
.checkout-modal .field select{
  height:46px!important;
  padding:0 13px!important;
  border:1px solid #dfe1e5!important;
  border-radius:12px!important;
  background:#fafbfc!important;
  font-size:12.5px!important;
  box-shadow:none!important;
}
.checkout-modal .field input:focus,
.checkout-modal .field select:focus{
  background:#fff!important;
  border-color:#d3a44d!important;
  box-shadow:0 0 0 3px rgba(211,164,77,.09)!important;
}
.checkout-delivery-note{
  margin-top:6px!important;
  font-size:8px!important;
  color:#9a742f!important;
}
.checkout-costs{
  padding:0!important;
}
.checkout-costs .cost-row{
  padding:7px 2px!important;
  font-size:10.5px!important;
  color:#4c4f54!important;
}
.checkout-costs .cost-row strong{
  font-size:11.5px!important;
  color:#17191c!important;
}
.checkout-costs .cost-row.total{
  margin-top:7px!important;
  padding:12px 13px!important;
  border:0!important;
  border-radius:13px!important;
  background:linear-gradient(135deg,#071522,#0d2d4b)!important;
  color:#fff!important;
  box-shadow:0 8px 20px rgba(7,21,34,.12)!important;
}
.checkout-costs .cost-row.total span{
  color:#fff!important;
  font-size:12px!important;
  font-weight:700!important;
}
.checkout-costs .cost-row.total strong{
  color:#f0c46c!important;
  font-size:16px!important;
  font-weight:800!important;
}
.checkout-payment-field select{
  font-weight:600!important;
  background-color:#fff!important;
}
.checkout-proof{
  margin-top:8px!important;
  padding:11px!important;
  border-radius:12px!important;
}
.checkout-submit-wrap{
  position:sticky!important;
  bottom:-1px!important;
  margin:0 -2px!important;
  padding:9px 2px 2px!important;
  background:linear-gradient(to top,#f5f6f8 76%,rgba(245,246,248,0))!important;
}
.checkout-confirm{
  min-height:50px!important;
  border-radius:14px!important;
  background:#071522!important;
  font-size:13.5px!important;
  font-weight:700!important;
  box-shadow:0 9px 22px rgba(7,21,34,.16)!important;
}
.checkout-confirm:active{
  transform:translateY(1px);
}
@media(max-width:430px){
  .checkout-overlay{padding:0!important;align-items:flex-end!important}
  .checkout-modal{
    width:100%!important;
    height:calc(100dvh - 8px)!important;
    max-height:calc(100dvh - 8px)!important;
    border-radius:24px 24px 0 0!important;
  }
  .checkout-top{
    min-height:58px!important;
    padding:9px 11px!important;
  }
  .checkout-title-wrap h2{font-size:19px!important}
  .checkout-brand{font-size:10px!important}
  .checkout-body{padding:8px 8px calc(10px + env(safe-area-inset-bottom))!important}
  .checkout-section{padding:11px!important;border-radius:16px!important;margin-bottom:7px!important}
  .checkout-section-head{margin-bottom:9px!important}
  .checkout-section-head p{display:none!important}
  .checkout-grid{grid-template-columns:1fr!important;gap:7px!important}
  .checkout-modal .field input,.checkout-modal .field select{height:44px!important;font-size:12px!important}
  .checkout-costs .cost-row.total{padding:11px 12px!important}
  .checkout-confirm{min-height:48px!important;font-size:13px!important}
}
'''

if marker not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

p.write_text(html, encoding='utf-8')
assert marker in html
assert '.checkout-modal{' in html
assert '.checkout-costs .cost-row.total{' in html
print('checkout premium redesign applied')
