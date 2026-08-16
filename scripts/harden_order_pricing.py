from pathlib import Path

rules_path = Path('firestore.rules')
index_path = Path('index.html')
rules = rules_path.read_text(encoding='utf-8')
index = index_path.read_text(encoding='utf-8')

old_block = '''    function reservationProductMatches(productId, reservationId) {
      let product = getAfter(
        /databases/$(database)/documents/products/$(productId)
      ).data;

      return product.lastInventoryReservationId == reservationId;
    }
'''

new_block = '''    function validOrderItem(orderId, item) {
      let product = getAfter(
        /databases/$(database)/documents/products/$(item.productId)
      ).data;

      return item is map
        && item.keys().hasAll([
          'productId',
          'name',
          'price',
          'qty',
          'image'
        ])
        && item.keys().hasOnly([
          'productId',
          'name',
          'price',
          'qty',
          'image'
        ])
        && item.productId is string
        && item.productId.size() > 0
        && item.productId.size() <= 200
        && item.name is string
        && item.name.size() > 0
        && item.name.size() <= 300
        && item.price is number
        && item.price > 0
        && item.price <= 100000000
        && item.qty is int
        && item.qty > 0
        && item.qty <= 1000
        && item.image is string
        && item.image.size() <= 2000
        && product.get('active', true) != false
        && product.name == item.name
        && product.price == item.price
        && product.lastInventoryReservationId == orderId + '_' + item.productId
        && request.resource.data.inventory.get(item.productId, 0) == item.qty;
    }

    function validOrderPricing(orderId) {
      let items = request.resource.data.items;
      let subtotal = request.resource.data.subtotal;

      return (
          items.size() == 1
          && validOrderItem(orderId, items[0])
          && subtotal == items[0].price * items[0].qty
        )
        || (
          items.size() == 2
          && validOrderItem(orderId, items[0])
          && validOrderItem(orderId, items[1])
          && subtotal == items[0].price * items[0].qty
            + items[1].price * items[1].qty
        )
        || (
          items.size() == 3
          && validOrderItem(orderId, items[0])
          && validOrderItem(orderId, items[1])
          && validOrderItem(orderId, items[2])
          && subtotal == items[0].price * items[0].qty
            + items[1].price * items[1].qty
            + items[2].price * items[2].qty
        )
        || (
          items.size() == 4
          && validOrderItem(orderId, items[0])
          && validOrderItem(orderId, items[1])
          && validOrderItem(orderId, items[2])
          && validOrderItem(orderId, items[3])
          && subtotal == items[0].price * items[0].qty
            + items[1].price * items[1].qty
            + items[2].price * items[2].qty
            + items[3].price * items[3].qty
        )
        || (
          items.size() == 5
          && validOrderItem(orderId, items[0])
          && validOrderItem(orderId, items[1])
          && validOrderItem(orderId, items[2])
          && validOrderItem(orderId, items[3])
          && validOrderItem(orderId, items[4])
          && subtotal == items[0].price * items[0].qty
            + items[1].price * items[1].qty
            + items[2].price * items[2].qty
            + items[3].price * items[3].qty
            + items[4].price * items[4].qty
        )
        || (
          items.size() == 6
          && validOrderItem(orderId, items[0])
          && validOrderItem(orderId, items[1])
          && validOrderItem(orderId, items[2])
          && validOrderItem(orderId, items[3])
          && validOrderItem(orderId, items[4])
          && validOrderItem(orderId, items[5])
          && subtotal == items[0].price * items[0].qty
            + items[1].price * items[1].qty
            + items[2].price * items[2].qty
            + items[3].price * items[3].qty
            + items[4].price * items[4].qty
            + items[5].price * items[5].qty
        );
    }

    function validDeliveryFee() {
      let general = get(
        /databases/$(database)/documents/storeSettings/general
      ).data;
      let rates = general.get('deliveryRates', {});
      let defaultFee = general.get('deliveryDefaultFee', 0);
      let expectedFee = rates.get(request.resource.data.customer.city, defaultFee);

      return expectedFee is number
        && expectedFee >= 0
        && request.resource.data.deliveryFee == expectedFee;
    }
'''

if old_block not in rules:
    raise SystemExit('reservationProductMatches block not found')
rules = rules.replace(old_block, new_block, 1)

old_order_anchor = '''        && request.resource.data.inventory.size() == request.resource.data.items.size()
        && request.resource.data.inventoryManaged == true
        && request.resource.data.subtotal is number
'''
new_order_anchor = '''        && request.resource.data.inventory.size() == request.resource.data.items.size()
        && request.resource.data.inventoryManaged == true
        && validOrderPricing(orderId)
        && request.resource.data.subtotal is number
'''
if old_order_anchor not in rules:
    raise SystemExit('order pricing anchor not found')
rules = rules.replace(old_order_anchor, new_order_anchor, 1)

old_fee_anchor = '''        && request.resource.data.deliveryFee is number
        && request.resource.data.deliveryFee >= 0
        && request.resource.data.deliveryFee <= 1000000
        && request.resource.data.total == request.resource.data.subtotal + request.resource.data.deliveryFee
'''
new_fee_anchor = '''        && request.resource.data.deliveryFee is number
        && request.resource.data.deliveryFee >= 0
        && request.resource.data.deliveryFee <= 1000000
        && validDeliveryFee()
        && request.resource.data.total == request.resource.data.subtotal + request.resource.data.deliveryFee
'''
if old_fee_anchor not in rules:
    raise SystemExit('delivery fee anchor not found')
rules = rules.replace(old_fee_anchor, new_fee_anchor, 1)

old_reservation_tail = '''        && validReservationOrder(
          request.resource.data.orderId,
          request.resource.data.productId,
          request.resource.data.qty
        )
        && reservationProductMatches(
          request.resource.data.productId,
          reservationId
        );
'''
new_reservation_tail = '''        && validReservationOrder(
          request.resource.data.orderId,
          request.resource.data.productId,
          request.resource.data.qty
        );
'''
if old_reservation_tail not in rules:
    raise SystemExit('reservation tail not found')
rules = rules.replace(old_reservation_tail, new_reservation_tail, 1)

old_norm = "function normalizeZone(v){return String(v||'').trim().toLocaleLowerCase('ar').replace(/\\s+/g,' ')}"
new_norm = "function normalizeZone(v){return String(v||'').trim()}"
if old_norm not in index:
    raise SystemExit('normalizeZone function not found')
index = index.replace(old_norm, new_norm, 1)

rules_path.write_text(rules, encoding='utf-8')
index_path.write_text(index, encoding='utf-8')
print('Order price, item identity, stock reservation, and delivery fee validation hardened.')
