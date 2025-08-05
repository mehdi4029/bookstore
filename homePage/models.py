from calendar import month
from datetime import timedelta
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_jalali.db import models as jmodels
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    categoryName = models.CharField(max_length=100, verbose_name="نام دسته بندی")

    class Meta:
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.categoryName

class Book(models.Model):
    bookName = models.CharField(max_length=100, verbose_name="نام کتاب")
    author = models.CharField(max_length=100,  verbose_name="نام نویسنده")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    description = models.TextField(verbose_name="توضیحات")
    category = models.ManyToManyField(Category,  verbose_name="دسته بندی ها")
    production_year = models.CharField(max_length=11, default='1404',  verbose_name="سال انتشار")
    publicated_from = models.CharField(max_length=100, default='فرهنگ و قلم' ,  verbose_name="انتشاراتی")
    image = models.FileField(upload_to='books-image/')
    sell_count = models.BigIntegerField(default=0,  verbose_name="تعداد فروش")
    hotDeal = models.BooleanField(default=False,  verbose_name="پشنهاد ویژه")
    available_count = models.PositiveIntegerField(default=0, verbose_name="تعداد موجودی")
    is_available = models.BooleanField(default=True,  verbose_name="موجود بودن")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,  verbose_name="به روز رسانی شده در تاریخ :")

    def __str__(self):
        return self.bookName

    class Meta:
        verbose_name_plural = "کتاب ها"


    @property
    def getPrice(self):
        price = str(self.price)
        start = len(price) - 3
        end = len(price) - 1
        finalStr = ''
        while start > 0:
            finalStr = ',' + price[start:end + 1] + finalStr
            start -= 3
            end -= 3
        return price[0:end + 1] + finalStr + '  تومان'

    @property
    def getCategory(self):
        mainString = ''
        for x in self.category.all():
            mainString += str(x) + ' / '
        return mainString[0:len(mainString) - 2]


class MyUser(AbstractUser) :
       favBooks = models.ManyToManyField(Book , blank=False, verbose_name="کتاب های مورد علاقه")
       phoneNumber = models.CharField( max_length=11,
           validators=[
               RegexValidator(
                   regex='^\d{10}$' ,
               ),
           ],
           null=True ,
           blank=True ,  verbose_name="شماره تلفن همراه"
       )
       uniqueMail = models.EmailField(unique=True , default='<EMAIL>' , blank=False,  verbose_name="ایمیل یکتا")

       class Meta :
           verbose_name_plural = "کاربر ها"


       def __str__(self):
           return self.username





class CartItem(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE , default=None)
    book = models.ForeignKey(Book, on_delete=models.CASCADE , default=None)
    count = models.PositiveIntegerField(default=1)

    


class Order(models.Model) :
     items = models.ManyToManyField(Book,  verbose_name="کتاب ها")
     counts = models.JSONField(default=dict ,  verbose_name="تعداد آیتم های سفارش شده")
     user = models.ForeignKey(MyUser, on_delete=models.CASCADE,  verbose_name="کاربر سفارش دهنده")
     customerPhone = models.CharField(max_length=20, default='',  verbose_name="شماره تلفن سفارش دهنده")
     customerName = models.CharField(max_length=100 , default='anonymous',  verbose_name="نام سفارش دهنده")
     address = models.TextField(max_length=1000 , default='',  verbose_name="آدرس ارسال")
     total_price = models.IntegerField(default=0,  verbose_name="مبلغ کل سفارش")
     is_paid = models.BooleanField(default=False,  verbose_name="وضعیت پرداخت")
     created_at = jmodels.jDateField(auto_now_add=True,  verbose_name="ایجاد شده در :")
     ref_id = models.PositiveIntegerField(default=0,  verbose_name="کد یکتای پرداخت از سمت زرین پال")

     class Meta :
         verbose_name_plural = "سفارشات"



class Comment(models.Model):
    bodyText = models.TextField(max_length=900,  verbose_name="متن نظر")
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE,  verbose_name="نوسنده نظر")
    relatedBook = models.ForeignKey(Book, on_delete=models.CASCADE,  verbose_name="کتاب مربوطه")
    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="ایجاد شده در :")


    class Meta :
        verbose_name_plural = "نظرات کاربران"


    @property
    def commentAge(self):
        age = timezone.now() - self.created_at
        if age < timedelta(hours=1) :
                return str(int(age.total_seconds() / 60)) + 'دقیقه پیش'
        if age < timedelta(hours=24) and age > timedelta(hours=1):
            return str(int(age.total_seconds() / 60 / 60)) + 'ساعت پیش'

        if  age > timedelta(hours=24) :
                return str(int( (age.total_seconds() / 60) / 60 / 24 )) + 'روز پیش'
        if age > timedelta(days=30) :
                return str(int(age.days / 30)) + 'ماه پیش'
