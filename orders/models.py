from random import choices

from django.db import models
from account.models import ShopUser
from shop.models import Product


# Create your models here.


class Order(models.Model):
    CHOICES = [
        ('در صف بررسی','در صف بررسی'),
        ('تایید سفارش','تایید سفارش'),
        ('دریافت از فروشنده','دریافت از فروشنده'),
        ('اماده سازی سفارش','اماده سازی سفارش'),
        ('تحویل به پست','تحویل به پست'),
        ('تحویل مرسوله به مشتری','تحویل مرسوله به مشتری'),
        ('عودت هزینه به دلیل عدم موجودی','عودت هزینه به دلیل عدم موجودی')
    ]
    buyer = models.ForeignKey(ShopUser, related_name='orders', on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50,choices=CHOICES,default="در صف بررسی")
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f"order {self.id}"


    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_post_cost(self):
        weight = sum(item.get_weight() for item in self.items.all())
        if weight < 1000:
            return 20000
        elif  1000 <= weight <= 2000:
            return 30000
        else:
            return 50000

    def get_final_cost(self):
        price = self.get_post_cost() + self.get_total_cost()
        return price

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_weight(self):
        return self.weight * self.quantity


class SuccessfulTransaction(models.Model):
    order = models.ForeignKey(Order, related_name='transactions', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    transaction_id = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id

    class Meta:
        verbose_name = "Successful Transaction"
        verbose_name_plural = "Successful Transactions"


class ReturnRequest(models.Model):
    CHOICES = [
        ('رد کردن','رد کردن'),
        ('تایید کردن','تایید کردن'),
        ('در حال بررسی','در حال بررسی')
    ]
    order = models.ForeignKey(Order, related_name='return_requests', on_delete=models.CASCADE)
    status = models.CharField(choices=CHOICES, max_length=30, default="در حال بررسی")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order.id}:{self.created}"

    class Meta:
        verbose_name = "Return request"
        verbose_name_plural = "Return requests"

