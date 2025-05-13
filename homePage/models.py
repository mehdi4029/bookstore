from calendar import month
from datetime import timedelta
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    categoryName = models.CharField(max_length=100)

    def __str__(self):
        return self.categoryName

class Book(models.Model):
    bookName = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    category = models.ManyToManyField(Category)
    production_year = models.CharField(max_length=11, default='1404')
    publicated_from = models.CharField(max_length=100, default='فرهنگ و قلم')
    image = models.FileField(upload_to='books-image/')
    sell_count = models.BigIntegerField(default=0)
    hotDeal = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
       favBooks = models.ManyToManyField(Book , blank=False)
       phoneNumber = models.CharField( max_length=11,
           validators=[
               RegexValidator(
                   regex='^\d{10}$' ,
               ),
           ],
           null=True ,
           blank=True
       )
       uniqueMail = models.EmailField(unique=True , default='<EMAIL>' , blank=False)
       def __str__(self):
           return self.username





class CartItem(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE , default=None)
    book = models.ForeignKey(Book, on_delete=models.CASCADE , default=None)
    count = models.PositiveIntegerField(default=1)

    






class Order(models.Model) :
     items = models.ManyToManyField(CartItem)
     user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
     customerName = models.CharField(max_length=100 , default='anonymous')
     address = models.TextField(max_length=1000 , default='')
     is_paid = models.BooleanField(default=False)
     created_at = models.DateTimeField(auto_now_add=True)



class Comment(models.Model):
    bodyText = models.TextField(max_length=900)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    relatedBook = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

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
