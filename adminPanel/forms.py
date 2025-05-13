from django import forms
from homePage.models import *
from django.core.validators import MinValueValidator


class BookForm(forms.ModelForm) :
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['sell_count']
        labels = {
            'hotDeal' : 'پیشنهاد ویژه' ,
            'is_available' : 'موجود بودن کتاب در انبار :'
        }
        widgets = {
            'bookName' : forms.TextInput(attrs={'placeholder':'نام کتاب'}),
            'publicated_from' : forms.TextInput(attrs={'placeholder' : 'نام انتشارات'}),
            'production_year' : forms.TextInput(attrs={'placeholder' : 'سال تولید'}) ,
            'author': forms.TextInput(attrs={'placeholder': 'نام نویسنده'}),
            'price': forms.NumberInput(attrs={'min':'0','placeholder': 'قیمت کتاب'}),
            'description': forms.TextInput(attrs={'placeholder': 'توضیحات کتاب'}),
            'category' : forms.CheckboxSelectMultiple()
        }

class CategoryForm(forms.ModelForm):
       class Meta:
            model = Category
            fields = '__all__'