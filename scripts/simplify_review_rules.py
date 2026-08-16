from pathlib import Path
p=Path('firestore.rules')
s=p.read_text(encoding='utf-8')
helper='''    function validReviewPurchase(orderId, productId) {\n      let order = get(\n        /databases/$(database)/documents/orders/$(orderId)\n      ).data;\n\n      return signedIn()\n        && order.customerUid == request.auth.uid\n        && order.status == 'delivered'\n        && order.inventory is map\n        && order.inventory.get(productId, 0) > 0;\n    }\n\n'''
s=s.replace(helper,'')
create_old='''        && request.resource.data.createdAt == request.time\n        && request.resource.data.updatedAt == request.time\n        && validReviewPurchase(\n          request.resource.data.orderId,\n          request.resource.data.productId\n        );'''
create_new='''        && request.resource.data.createdAt == request.time\n        && request.resource.data.updatedAt == request.time\n        && get(\n          /databases/$(database)/documents/orders/$(request.resource.data.orderId)\n        ).data.customerUid == request.auth.uid\n        && get(\n          /databases/$(database)/documents/orders/$(request.resource.data.orderId)\n        ).data.status == 'delivered'\n        && get(\n          /databases/$(database)/documents/orders/$(request.resource.data.orderId)\n        ).data.inventory is map\n        && get(\n          /databases/$(database)/documents/orders/$(request.resource.data.orderId)\n        ).data.inventory.get(request.resource.data.productId, 0) > 0;'''
update_old='''        && request.resource.data.createdAt == resource.data.createdAt\n        && request.resource.data.updatedAt == request.time\n        && validReviewPurchase(\n          resource.data.orderId,\n          resource.data.productId\n        );'''
update_new='''        && request.resource.data.createdAt == resource.data.createdAt\n        && request.resource.data.updatedAt == request.time\n        && get(\n          /databases/$(database)/documents/orders/$(resource.data.orderId)\n        ).data.customerUid == request.auth.uid\n        && get(\n          /databases/$(database)/documents/orders/$(resource.data.orderId)\n        ).data.status == 'delivered'\n        && get(\n          /databases/$(database)/documents/orders/$(resource.data.orderId)\n        ).data.inventory is map\n        && get(\n          /databases/$(database)/documents/orders/$(resource.data.orderId)\n        ).data.inventory.get(resource.data.productId, 0) > 0;'''
if create_old not in s or update_old not in s:
    raise SystemExit('review rule markers not found')
s=s.replace(create_old,create_new,1).replace(update_old,update_new,1)
if 'validReviewPurchase' in s:
    raise SystemExit('helper still present')
p.write_text(s,encoding='utf-8')
print('review rules simplified')
