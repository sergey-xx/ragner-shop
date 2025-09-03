from payments.smileone import so_api
from items.models import Item
from codes.models import Activator


def update_smileone_items():
    pl = so_api.get_product_list('mobilelegends')
    for p in pl:
        if Item.objects.filter(category=Item.Category.DIAMOND, data__id=p.id).exists():
            continue
        Item.objects.get_or_create(
            title=p.spu,
            category=Item.Category.DIAMOND,
            price=100,
            amount=None,
            is_active=False,
            activator=Activator.SMILEONE,
            data=p.to_dict(),
        )
