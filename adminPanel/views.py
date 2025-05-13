from django.template.loader import render_to_string

from homePage.models import MyUser
from login_Register.backends import MyUserAuthBackend
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import success,error
from homePage.models import *
from adminPanel.forms import *
from django.contrib.auth.models import User
# Create your views here.


def checkLogin(request):
    if request.method == 'GET':
        return render(request,'adminLogin.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try :
                user = MyUser.objects.get(username=username)
                if user is not None and user.is_superuser :
                    if user.check_password(password):
                        response = render(request,'adminPanel.html' )
                        response.set_cookie(key='as' , value='ok')
                        return response
        except Exception as e:
              messages.error(request,'مشخصات وارد شده صحیح نمیباشد')
              return redirect('/adminPanel/login')


def bookCreation(request):
    if request.COOKIES.get('as') == 'ok' and request.method == 'GET' :
        form = BookForm()
        return render(request,'adminPanel.html' , {'form':form})
    if request.COOKIES.get('as') == 'ok' and request.method == 'POST' :
         book = BookForm(request.POST,request.FILES)
         if book.is_valid() :
             book.save()
         return redirect('/adminPanel/createbook')
    else :
         return redirect('/adminPanel/login')


def categoryCreation(request):
    if request.COOKIES.get('as') == 'ok' and request.method == 'GET' :
        form = CategoryForm()
        return render(request,'adminPanel.html' , {'form':form})
    if request.COOKIES.get('as') == 'ok' and request.method == 'POST' :
         category = CategoryForm(request.POST)
         category.save()
         return redirect('/adminPanel/createcategory')
    else :
         return redirect('/adminPanel/login')

