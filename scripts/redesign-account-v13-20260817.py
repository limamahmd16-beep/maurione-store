from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')
marker = '/* MauriOne account redesign v13 */'
if marker in s:
    raise SystemExit('account v13 already applied')
css = r'''
/* MauriOne account redesign v13 */
#accountPage{
  min-height:calc(100vh - 64px);
  background:#f7f7f8;
  padding-bottom:28px;
}
#accountPage .page-head{
  margin:0;
  padding:20px 14px 14px;
  background:#fff;
  border-bottom:1px solid #eeeeef;
}
#accountPage .page-head::before{
  content:'MauriOne Account';
  display:block;
  margin-bottom:4px;
  color:var(--gold);
  font-size:9px;
  font-weight:700;
  letter-spacing:.2px;
  direction:ltr;
  text-align:right;
}
#accountPage .page-head h1{
  font-size:26px;
  line-height:1.2;
  letter-spacing:-.25px;
}
#accountPage .page-head p{
  margin-top:5px;
  max-width:440px;
  color:#8b8d92;
  font-size:9.5px;
  line-height:1.65;
}
#accountPage>.box{
  margin:10px 12px 0;
  padding:14px;
  border:1px solid #ececef;
  border-radius:22px;
  background:#fff;
  box-shadow:0 5px 20px rgba(7,21,34,.025);
}
#accountLoggedIn::before{
  content:'بيانات الحساب';
  display:block;
  margin:1px 2px 10px;
  font-size:15px;
  font-weight:700;
}
#accountPage .account-user{
  display:grid;
  grid-template-columns:auto minmax(0,1fr) 46px;
  align-items:center;
  gap:10px;
  margin:0 0 14px;
  padding:12px;
  border-radius:17px;
  background:linear-gradient(135deg,#071522,#0d2c48);
  color:#fff;
}
#accountPage .account-user::before{
  content:'M';
  grid-column:3;
  grid-row:1;
  width:46px;
  height:46px;
  border-radius:14px;
  display:grid;
  place-items:center;
  background:linear-gradient(145deg,#d8aa52,#f0ca76);
  color:#071522;
  font-size:20px;
  font-weight:900;
  direction:ltr;
}
#accountPage .account-user>div{
  grid-column:2;
  grid-row:1;
  min-width:0;
  text-align:right;
}
#accountPage .account-user small{
  color:#aeb8c2;
  font-size:8px;
}
#accountPage .account-user strong{
  margin-top:3px;
  color:#fff;
  font-size:10.5px;
  font-weight:600;
  overflow-wrap:anywhere;
  direction:ltr;
  text-align:right;
}
#accountPage .account-logout{
  grid-column:1;
  grid-row:1;
  align-self:center;
  border:1px solid rgba(255,255,255,.16);
  background:rgba(255,255,255,.09);
  color:#fff;
  border-radius:11px;
  padding:8px 9px;
  font-size:8.5px;
}
#accountPage .field{
  margin-bottom:10px;
}
#accountPage .field label{
  margin:0 4px 6px;
  color:#777a80;
  font-size:9px;
  font-weight:500;
}
#accountPage .field input{
  height:50px;
  padding:0 14px;
  border:1px solid #e3e4e7;
  border-radius:14px;
  background:#fafafa;
  font-size:13px;
  outline:0;
  transition:border-color .18s ease,box-shadow .18s ease,background .18s ease;
}
#accountPage .field input:focus{
  background:#fff;
  border-color:#d3a44d;
  box-shadow:0 0 0 3px rgba(211,164,77,.10);
}
#accountPage #accountSaveBtn{
  min-height:50px;
  margin-top:2px;
  border-radius:14px;
  background:linear-gradient(135deg,#071522,#0d2d4b);
  font-size:13px;
  font-weight:700;
  box-shadow:0 8px 20px rgba(7,21,34,.13);
}
#accountPage #accountStatus{
  margin-top:9px;
  border-radius:11px;
}
#accountPage .favorites-head{
  margin:0 0 12px;
  padding:1px 2px 10px;
  border-bottom:1px solid #efeff1;
}
#accountPage .favorites-head h2{
  font-size:17px;
  font-weight:700;
}
#accountPage .favorites-count{
  min-width:29px;
  height:25px;
  padding:0 9px;
  display:grid;
  place-items:center;
  border-radius:20px;
  background:#f2f3f5;
  color:#555;
  font-size:9px;
  font-weight:700;
}
#accountPage #favoritesList{
  gap:9px;
}
#accountPage #favoritesList .product{
  border-radius:17px;
  box-shadow:none;
}
#accountPage #favoritesList .product-img{
  height:145px;
  border-radius:13px;
}
#accountPage .policy-menu h2{
  margin:0 2px 11px;
  font-size:17px;
  font-weight:700;
}
#accountPage .policy-grid{
  gap:8px;
}
#accountPage .policy-link{
  min-height:54px;
  padding:12px;
  border:1px solid #e9eaed;
  border-radius:14px;
  background:#f8f8fa;
  font-size:10px;
  font-weight:600;
}
#accountPage .policy-link:active{
  background:#f1f2f4;
}
#accountPage .account-auth{
  padding:8px 4px 4px;
}
#accountPage .account-avatar{
  width:60px;
  height:60px;
  border-radius:18px;
  margin-bottom:12px;
  background:linear-gradient(145deg,#071522,#17324c);
  color:var(--gold);
  box-shadow:0 8px 24px rgba(7,21,34,.12);
}
#accountPage .account-auth h2{
  font-size:19px;
}
#accountPage .account-auth p{
  margin-top:7px;
  font-size:9.5px;
}
#accountPage #customerLoginBtn{
  min-height:49px;
  border-radius:14px;
  background:linear-gradient(135deg,#071522,#0d2d4b);
  font-size:12px;
}
@media(max-width:390px){
  #accountPage .page-head{padding:18px 11px 12px}
  #accountPage .page-head h1{font-size:24px}
  #accountPage>.box{margin-left:10px;margin-right:10px;padding:12px;border-radius:19px}
  #accountPage .account-user{grid-template-columns:auto minmax(0,1fr) 42px;padding:10px}
  #accountPage .account-user::before{width:42px;height:42px;border-radius:13px;font-size:18px}
  #accountPage .account-user strong{font-size:9.5px}
  #accountPage .field input{height:47px;font-size:12px}
  #accountPage #favoritesList .product-img{height:132px}
}
'''
s = s.replace('</style>', css + '\n</style>', 1)
path.write_text(s, encoding='utf-8')
