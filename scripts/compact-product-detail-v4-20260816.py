from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
css='''
/* MauriOne product detail v4 — compact */
body.product-open{padding-bottom:150px}
.detail-v2{padding:0 10px 176px}
.detail-topbar{height:46px}
.detail-v2 .detail-back,.detail-topshare{width:36px;height:36px}
.detail-v2 .detail-back svg,.detail-topshare svg{width:19px;height:19px}
.detail-summary{padding:14px;border-radius:18px;margin-bottom:8px}
.detail-v2 .detail-category{font-size:9px}
.detail-v2 .detail-summary h1{font-size:20px;line-height:1.25;margin-top:4px}
.detail-v2 .detail-meta{font-size:9.5px;margin-top:5px}
.detail-price-row{margin-top:10px}
.detail-v2 .detail-price{font-size:20px}
.detail-v2 .detail-stock{font-size:9px}
.detail-rating-jump{margin-top:9px;padding-top:8px;font-size:9px}
.detail-rating-jump #detailRatingStars{font-size:14px}
.detail-v2 .detail-gallery{padding:8px;border-radius:18px;margin-bottom:8px}
.detail-v2 .detail-main{height:205px;border-radius:14px}
.detail-v2 .detail-thumbs{margin-top:7px;gap:6px}
.detail-v2 .detail-thumb{flex-basis:44px;height:44px;border-radius:9px}
.detail-v2 .detail-info{padding:13px;border-radius:18px}
.detail-v2 .detail-specs{gap:7px}.detail-v2 .detail-spec{padding:9px;border-radius:11px}.detail-v2 .detail-spec small{font-size:8px}.detail-v2 .detail-spec strong{font-size:10.5px;margin-top:3px}
.detail-v2 .detail-description{margin-top:11px;padding-top:11px}.detail-v2 .detail-description h3{font-size:13px}.detail-v2 .detail-description p{font-size:10px;line-height:1.75}
.detail-secondary-actions{margin-top:11px;gap:6px}.detail-v2 .detail-favorite,.detail-v2 .detail-share{padding:9px 6px;font-size:9px;border-radius:10px}
.detail-v2 .review-section{margin-top:13px;padding-top:13px}
.detail-related{margin-top:8px;padding:12px;border-radius:18px}
.detail-related-head{margin-bottom:9px}.detail-related-head small{font-size:8px}.detail-related-head h2{font-size:16px}.detail-related-head button{font-size:9px}
.detail-related-grid{display:flex!important;grid-template-columns:none!important;overflow-x:auto;gap:8px!important;padding:0 0 4px!important;scrollbar-width:none}
.detail-related-grid::-webkit-scrollbar{display:none}
.detail-related-grid .product{flex:0 0 132px;border-radius:14px;padding:6px}
.detail-related-grid .product-img{height:92px;border-radius:10px}
.detail-related-grid .favorite-btn{width:28px;height:28px;top:9px;left:9px;font-size:15px}
.detail-related-grid .product small{font-size:8px;margin-top:5px}
.detail-related-grid .product h3{font-size:10.5px;min-height:30px;margin-top:3px}
.detail-related-grid .product-rating{font-size:8px;margin-top:4px}
.detail-related-grid .price{font-size:12px;margin-top:5px}
.detail-related-grid .stock{font-size:8px;margin-top:4px}
.detail-related-grid .add{font-size:9px;padding:7px;margin-top:7px;border-radius:9px}
.detail-buybar{padding:8px 10px calc(8px + env(safe-area-inset-bottom));gap:8px}
.detail-buybar>div{min-width:94px}.detail-buybar small{font-size:8px}.detail-buybar strong{font-size:12.5px}.detail-v2 .detail-buybar .detail-add{padding:11px 14px;font-size:12px;border-radius:11px}
@media(max-width:390px){.detail-v2 .detail-main{height:190px}.detail-v2 .detail-summary h1{font-size:19px}.detail-v2 .detail-price{font-size:19px}.detail-related-grid .product{flex-basis:124px}}
'''
if '/* MauriOne product detail v4 — compact */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)
p.write_text(s,encoding='utf-8')
