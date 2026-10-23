from django import template
from shop.models import *
from django.db.models import Count,Max,Min
register = template.Library()
from markdown import markdown
from django.utils.safestring import mark_safe


@register.simple_tag()
def cheapest_products():
    products = Product.objects.order_by('new_price')[:4]
    return products


@register.simple_tag()
def most_expensive_products():
    products = Product.objects.order_by('-new_price')[:4]
    return products

@register.simple_tag()
def latest_products():
    products = Product.objects.order_by('-created')[:4]
    return products