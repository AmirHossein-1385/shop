from django.contrib import admin
from .models import *
# Register your models here.


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

class FeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug':('name',)}
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','inventory','new_price','created','updated']
    list_filter = ['created','updated']
    inlines = [ImageInline,FeatureInline]


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code','discount','start_date','end_date','active','created']
    list_editable = ['active']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','product','text','active','rating']
    list_editable = ['active']
