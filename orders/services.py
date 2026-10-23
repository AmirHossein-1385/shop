from django.db import transaction


def approve_return(order):
    with transaction.atomic():
        for item in order.items.all():
            item.product.inventory += item.quantity
            item.product.save()

