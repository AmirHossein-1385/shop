from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.forms import ShopUserCreationForm, ShopUserChangeForm
from account.models import *


# Register your models here.

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0

@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    ordering = ['phone']
    add_form = ShopUserCreationForm
    form = ShopUserChangeForm
    model = ShopUser
    inlines = (AddressInline,)
    list_display = ('phone', 'first_name', 'last_name','email', 'is_active', 'is_staff')
    fieldsets =(
        (None, {'fields': ('phone','password','email')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets =(
        (None, {'fields': ('phone', 'password1','password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name','email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ['title','province','city','postal_code']

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user','balance','created','updated']