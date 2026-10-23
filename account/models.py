from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
# Create your models here.


class ShopUserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('you must provide a phone')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be True')

        return self.create_user(phone, password, **extra_fields)


class ShopUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, unique=True,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = ShopUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.phone


class Address(models.Model):
    user = models.ForeignKey(ShopUser,related_name="addresses",on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    province = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class Wallet(models.Model):
    user = models.OneToOneField(ShopUser,related_name="wallet",on_delete=models.CASCADE)
    balance = models.DecimalField(default=0,max_digits=9,decimal_places=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}:{self.balance}"


class WalletTransaction(models.Model):
    CHOICES = (
        ('deposit','شارژ کیف پول'),
        ('purchase','خرید با کیف پول')
    )
    wallet = models.ForeignKey(Wallet,related_name="transactions",on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9,decimal_places=0)
    type = models.CharField(max_length=50,choices=CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user} - {self.get_type_display()}-{self.amount}"