from django.contrib import admin
from homePage.models import *
from homePage.templatetags.custom_filter import register


# Register your models here.


@admin.register(Book, MyUser, Category, Comment, Order)
class BookStoreAdmin(admin.ModelAdmin):
    pass