from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Order
from django.utils import timezone

@receiver(pre_save, sender=Order)
def status_old_order(sender, instance, **kwargs):
    instance.status_changed = False

    if kwargs.get("raw", False):
        return

    if instance.id:
        old_order = Order.objects.filter(id=instance.id).first()

        if old_order and old_order.status != instance.status:
            instance.status_changed = True


@receiver(post_save, sender=Order)
def status(sender, instance, **kwargs):
    if instance.status_changed:
        print(instance.status, ':', instance.first_name + ' ' + instance.last_name)



@receiver(pre_save, sender=Order)
def delivery_time(sender, instance, **kwargs):
    if instance.status == "تحویل مرسوله به مشتری":
        instance.delivery_time = timezone.now()

