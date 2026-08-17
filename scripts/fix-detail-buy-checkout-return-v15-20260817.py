from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')
    s = s.replace(old, new, 1)

# 1) Product detail: add Buy Now beside Add to cart.
old_detail_button = '<button id="detailAdd" class="detail-add detail-inline-add" onclick="addDetailToCart()">أضف للسلة</button>'
new_detail_buttons = '<div class="detail-purchase-actions"><button id="detailAdd" class="detail-add detail-inline-add" onclick="addDetailToCart()">أضف للسلة</button><button id="detailBuyNow" class="detail-buy-now" onclick="buyDetailNow()">اشتري الآن</button></div>'
replace_once(old_detail_button, new_detail_buttons, 'detail purchase buttons')

old_add_fn = 'window.addDetailToCart=()=>{if(selectedProductId)addCart(selectedProductId)};'
new_add_fn = old_add_fn + '\nwindow.buyDetailNow=()=>{if(selectedProductId)buyNow(selectedProductId)};'
replace_once(old_add_fn, new_add_fn, 'detail buy function')

old_detail_state = "detailAdd.textContent=ct('addCartText');detailAdd.disabled=!available;"
new_detail_state = old_detail_state + "const detailBuyNow=document.getElementById('detailBuyNow');if(detailBuyNow)detailBuyNow.disabled=!available;"
replace_once(old_detail_state, new_detail_state, 'detail buy stock state')

# 2) Checkout: use an explicit back button instead of an ambiguous X.
old_checkout_close = '<button class="checkout-close" onclick="closeOverlay(\'checkoutOverlay\')" aria-label="إغلاق">×</button>'
new_checkout_back = '<button class="checkout-back" onclick="closeOverlay(\'checkoutOverlay\')" aria-label="رجوع"><span aria-hidden="true">‹</span><b>رجوع</b></button>'
replace_once(old_checkout_close, new_checkout_back, 'checkout back button')

# 3) After successful order, close checkout and show My Orders automatically.
old_success = "checkoutStatus.textContent=tpl(isTransfer?'orderSuccessTransferTemplate':'orderSuccessCodTemplate',{orderNo});placeOrderBtn.style.display='none'}catch(e){"
new_success = "checkoutStatus.textContent=tpl(isTransfer?'orderSuccessTransferTemplate':'orderSuccessCodTemplate',{orderNo});placeOrderBtn.style.display='none';setTimeout(()=>{closeOverlay('checkoutOverlay');openStore('cartPage','navCart');setCartView('orders')},900)}catch(e){"
replace_once(old_success, new_success, 'checkout success close')

css = r'''

/* MauriOne detail purchase + checkout return v15 */
.detail-purchase-actions{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:14px}
.detail-purchase-actions .detail-add{width:100%;margin-top:0!important;min-height:50px}
.detail-buy-now{width:100%;min-height:50px;border:0;border-radius:12px;background:linear-gradient(135deg,#e5b85d,#c99337);color:#fff;font-weight:800;font-size:13px;padding:12px 10px;box-shadow:0 7px 18px rgba(201,147,55,.18)}
.detail-buy-now:disabled{opacity:.42}
.checkout-top{grid-template-columns:78px 1fr auto!important}
.checkout-back{height:40px;border:0;border-radius:12px;background:#f4f4f6;padding:0 10px;display:flex;align-items:center;justify-content:center;gap:5px;font-size:12px;font-weight:700;white-space:nowrap}
.checkout-back span{font-size:21px;line-height:1}
.checkout-back b{font:inherit}
@media(max-width:430px){.checkout-top{grid-template-columns:72px 1fr auto!important}.checkout-back{height:38px;padding:0 8px;font-size:11px}.detail-purchase-actions{gap:8px}}
'''
if 'MauriOne detail purchase + checkout return v15' in s:
    raise SystemExit('v15 patch already present')
if '</style>' not in s:
    raise SystemExit('style end not found')
s = s.replace('</style>', css + '\n</style>', 1)

path.write_text(s, encoding='utf-8')
print('patched product detail buy-now and checkout return flow')
