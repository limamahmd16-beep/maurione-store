from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

marker='/* MauriOne home redesign v2 */'
if marker not in s:
    css=r'''
/* MauriOne home redesign v2 */
#home{background:#fff}
#home .hero{margin:12px 12px 0;min-height:228px;border-radius:26px;box-shadow:0 12px 34px rgba(7,21,34,.08)}
#home .hero-copy{padding:25px 20px 22px;max-width:72%}
#home .hero .label{font-size:10px;font-weight:700;letter-spacing:.2px}
#home .hero h1{font-size:28px;line-height:1.18;margin-top:7px;letter-spacing:-.4px}
#home .hero p{margin-top:10px;max-width:250px;font-size:11.5px;line-height:1.7;color:#d2d5da}
#home .hero button{margin-top:14px;padding:10px 16px;border-radius:12px;font-size:11px;font-weight:800}
#home .section{padding:22px 12px 0}
#home .section-head{align-items:center}
#home .section h2{font-size:22px;letter-spacing:-.2px}
#home .view-all{font-size:11px;padding:6px 0}
#siteProductsSection{padding-top:22px!important}
#home .products{margin-top:13px;gap:11px;padding-bottom:14px}
#home .product{border:1px solid #ededf0;border-radius:20px;padding:9px;background:#fff;box-shadow:0 4px 16px rgba(0,0,0,.025)}
#home .product-img{height:142px;border-radius:15px;background:#fafafa}
#home .product h3{font-size:13px;line-height:1.45;min-height:38px}
#home .price{font-size:15px}
#home .add{border-radius:11px;padding:10px;font-size:11px}
#siteCategoriesSection{padding-top:18px!important}
#home .categories{margin-top:12px;gap:8px;padding-bottom:3px;scrollbar-width:none}
#home .categories::-webkit-scrollbar{display:none}
#home .category{flex:0 0 84px;border:0;border-radius:18px;padding:8px 6px;background:#f7f7f8}
#home .category-art{height:54px;border-radius:14px;background:#fff}
#home .category-art svg{width:28px;height:28px}
#home .category strong{font-size:10.5px;margin-top:7px}
#siteTrust{display:flex;gap:8px;overflow-x:auto;padding:20px 12px 2px;scrollbar-width:none}
#siteTrust::-webkit-scrollbar{display:none}
#siteTrust .trust-card{flex:0 0 158px;min-height:78px;border-radius:17px;padding:10px;display:grid;grid-template-columns:38px 1fr;grid-template-rows:auto auto;column-gap:9px;align-items:center;text-align:right;background:#f7f7f8}
#siteTrust .icon-box{grid-row:1/3;grid-column:1;width:38px;height:38px;margin:0;border-radius:12px;box-shadow:none;background:#fff}
#siteTrust .icon-box svg{width:23px;height:23px}
#siteTrust .trust-card strong{grid-column:2;grid-row:1;font-size:11.5px;line-height:1.25;align-self:end}
#siteTrust .trust-card p{grid-column:2;grid-row:2;margin-top:2px;font-size:9px;line-height:1.4;align-self:start}
#home .home-info{margin-top:24px}
@media(max-width:390px){
  #home .hero{min-height:214px}
  #home .hero-copy{max-width:76%;padding:22px 18px 18px}
  #home .hero h1{font-size:25px}
  #home .hero p{font-size:10.5px}
  #siteTrust .trust-card{flex-basis:150px}
}
'''
    assert '</style>' in s
    s=s.replace('</style>',css+'\n</style>',1)

# Commerce-first homepage: hero -> products -> categories -> compact trust -> policies.
trust_start=s.find('<section id="siteTrust" class="trust">')
products_start=s.find('<section id="siteProductsSection" class="section">')
policies_start=s.find('<section class="home-info" id="homePolicies">')
if trust_start!=-1 and products_start!=-1 and policies_start!=-1 and trust_start < products_start < policies_start:
    trust_block=s[trust_start:products_start]
    s=s[:trust_start]+s[products_start:policies_start]+trust_block+s[policies_start:]

p.write_text(s,encoding='utf-8')
