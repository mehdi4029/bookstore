from django.contrib import admin
from homePage.models import *
from homePage.templatetags.custom_filter import register


# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('bookName', 'price', 'author', 'get_category_name',)
    search_fields = ('bookName', 'price', 'author',)

    def get_category_name(self, obj):
        return obj.category.name

    get_category_name.short_description = 'Category'
    get_category_name.admin_order_field = 'category__name'



@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'uniqueMail', 'phoneNumber',)
    search_fields = ('username', 'uniqueMail', 'phoneNumber',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['categoryName']
    search_fields = ['categoryName']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'get_related_book_name',)
    search_fields = ('author__username', 'bodyText',)

    def get_related_book_name(self, obj):
        return obj.relatedBook.bookName
    get_related_book_name.short_description = 'Related Book'
    get_related_book_name.admin_order_field = 'relatedBook__name'

    def get_author_name(self, obj):
        return obj.author.username
    get_author_name.short_description = 'Author'
    get_author_name.admin_order_field = 'author__username'



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('ref_id', 'total_price', 'customerName', 'customerPhone', 'address',)
    search_fields = ('ref_id', 'total_price', 'customerName', 'customerPhone', 'address',)
