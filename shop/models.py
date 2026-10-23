import os
import uuid
import jdatetime
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import ShopUser
from django.db.models import Avg
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug'])
        ]
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def get_absolute_url(self):
        return reverse('shop:products_list_by_category',args=[self.slug])

    def __str__(self):
        return self.name



def get_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('product_image', jdatetime.datetime.now().strftime('%Y/%m'), filename)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name="دسته بندی")
    name = models.CharField(max_length=200,verbose_name="نام")
    description = models.TextField(verbose_name="توضیحات")
    slug = models.SlugField(max_length=200, verbose_name="اسلاگ")
    inventory = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    price = models.PositiveIntegerField(default=0,verbose_name="قیمت")
    weight = models.PositiveIntegerField(default=0, verbose_name="وزن")
    off = models.PositiveIntegerField(default=0, verbose_name="تخفیف")
    new_price = models.PositiveIntegerField(default=0, verbose_name="قیمت پس از تخفیف")
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")
    saved_by = models.ManyToManyField(ShopUser,'saved_products')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id','slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    @property
    def average_rating(self):
        return self.comments.filter(active=True).aggregate(avg=Avg('rating'))['avg']

    def get_absolute_url(self):
        return reverse('shop:product_detail',args=[self.id,self.slug])

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="images", verbose_name="عکس محصول")
    file = models.ImageField(upload_to=get_upload_path)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصویر ها'


class ProductFeature(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام ویژگی')
    value = models.CharField(max_length=200, verbose_name='مقدار ویژگی')
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE,verbose_name="ویژگی ها")

    def __str__(self):
        return self.name + ':' + self.value



class DiscountCode(models.Model):
    code = models.CharField(max_length=50 , unique=True)
    discount = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class DiscountUsage(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    discount = models.ForeignKey(DiscountCode,on_delete=models.CASCADE)
    order = models.OneToOneField('orders.Order',related_name='discount_usage',on_delete=models.CASCADE)
    used = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}:{self.discount}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','discount'],
                name='unique_user_discount'
            ),
        ]


class Comment(models.Model):
    user = models.ForeignKey(ShopUser,related_name="comments",on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name="comments",on_delete=models.CASCADE)
    text = models.TextField()
    active = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=2,decimal_places=1,default=1,validators=[MinValueValidator(1), MaxValueValidator(5),])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}:{self.text[:30]}"

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_user_product_comment'
            )
        ]
    @property
    def rating_stars(self):
        stars = []

        for i in range(1, 6):
            if self.rating >= i:
                stars.append('full')
            elif self.rating >= i - 0.5:
                stars.append('half')
            else:
                stars.append('empty')

        return stars

