from django.urls import path
from login_Register.views import *


urlpatterns = [
    path('<str:path>' , authentication , name='authenticate'),
    path('api/login', login_view , name='login') ,
    path('api/register' , register_view , name='register') ,
    path('api/retrieve' , retrieve_view , name='retrieve') ,
    path('api/checkValidationCode' , checkCode_view , name='checkCode') ,
    path('api/submitPassword' , submit_passwd_view , name='submitPassword') ,
]