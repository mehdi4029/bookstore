import json
import random
import ghasedak_sms
from enum import unique
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib.auth import authenticate
from django.contrib.messages.context_processors import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import requests
from django.template.loader import render_to_string
from rest_framework import status
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework.response import Response
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from login_Register.backends import MyUserAuthBackend
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages
from builtins import Exception
from homePage.models import *
from login_Register.models import RandomCode
import logging

# sms_api = ghasedak_sms.Ghasedak(api_key='31246dbc41559df43229db9a4f091143a6379cc20b4827b12ba5fed4b4c7600cVZDNtgwdHC9ZZ89v')
def send_message(phoneNumber,random_code) :

    # response = sms_api.send_single_sms(
    #     ghasedak_sms.SendSingleSmsInput(
    #         message=f'{random_code.value}',
    #         receptor=f'0{phoneNumber}',
    #         line_number='30006703189189',
    #         send_date='',
    #         client_reference_id=''
    #     )
    # )
    # print(response)
    url = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpSMS"

    payload = json.dumps({
        "sendDate": timezone.now().isoformat(),
        "receptors": [
            {
                "mobile": f'0{phoneNumber}',  # Ensure phoneNumber is properly defined
            }
        ],
        "templateName": "verification",
        "inputs": [
            {
                "param": "code",
                "value": str(random_code.value)  # Explicit string conversion
            }
        ],
        "udh": False
    })

    headers = {
        'Content-Type': 'application/json',
        'ApiKey': "31246dbc41559df43229db9a4f091143a6379cc20b4827b12ba5fed4b4c7600cVZDNtgwdHC9ZZ89v"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)
    return {
        'refresh' : str(refresh) ,
        'access' : str(refresh.access_token)
    }


def dropPrevTokens(refresh_token):

       if refresh_token :
             refresh = RefreshToken(refresh_token)
             if refresh :
                     refresh.blacklist()
                     newRef = RefreshToken.for_user(refresh.user)
                     newAC = newRef.access_token
                     return {
                         'refresh' : str(newRef) ,
                         'access' : str(newAC)
                     }
             else :
                  return {
                      'error' : 'token is not validated'
                  }
       else :
            return {
                'error' : 'there is not a token'
            }


def deleteUserCodes(data) :
     username = data['username']
     try :
         qurey = RandomCode.objects.filter(related_to=username)
         qurey.delete()
     except Exception as e :
          pass

@api_view(['POST'])
def submit_passwd_view(request):

    data = JSONParser().parse(request)
    user_data = request.COOKIES.get('temporary-data' , '{}')
    user_data = json.loads(user_data)
    try:
        pswd = data['password']
        username = user_data['username']
        phoneNumber = user_data['phoneNumber']
        user = MyUser.objects.get(username=username, phoneNumber=phoneNumber)
        if pswd and request.COOKIES.get('flag')=='True' :
            user.set_password(pswd)
            user.save()
            messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد')
            return JsonResponse({'success': True} , status=200)
        else :
            messages.error(request, 'درخواست شما مجاز نیست')
            return JsonResponse({'success': False} , status=500)

    except Exception as e :
        messages.error(request, f'پروسه تغییر پسوورد به دلیل تاخیر لغو شد ، مجددا امتحان فرمایید')
        return JsonResponse({'success': False} , status=404)


@api_view(['POST'])
def checkCode_view(request):

    data = JSONParser().parse(request)
    validation_code = data['validation']
    user_data = request.COOKIES.get('temporary-data', '{}')
    user_data = json.loads(user_data)
    username = user_data['username']
    try :
        codeObj = RandomCode.objects.get(related_to=username , value=int(validation_code))
        if codeObj.is_valid():
              codeObj.delete()
              if user_data['mode'] == 'Register' :
                  user = UserSerializer(data=user_data)
                  if user.is_valid():
                      user = user.save()
              elif user_data['mode'] == 'Login' :
                  user = MyUser.objects.get(username=username)
              response = JsonResponse({'path' : request.GET.get('next')} , status=200)
              if request.GET.get('next') == '/' :
                   tokens = get_tokens_for_user(user)
                   response.set_cookie(key='refresh' , value=tokens['refresh'] , max_age=7 * 24 * 60 * 60 , httponly=True)
              return response
        else :
              codeObj.delete()
              messages.error(request,'کد وارد شده منقضی شده است ، کد جدید برای شما ارسال شد')
              return Response({'success': False} , status=404)
    except Exception as e :
        messages.error(request, f'   کد وارد شده معتبر نیست   ')
        return Response({'success': False} , status=404)


@api_view(['POST'])
def retrieve_view(request) :

    data = JSONParser().parse(request)
    username = data['username']
    phone_number = data['phoneNumber']

    try :
        user = MyUser.objects.get(username=username)
        response = Response(status=200)
        response.set_cookie(key='flag' , value='True' , max_age=10*60 , httponly=True)
        response.set_cookie(key='temporary-data' , value=json.dumps({'username' : user.username , 'phoneNumber' : user.phoneNumber , 'mode' : 'ChangePass'}) , max_age=10*60, httponly=True)
        return response

    except MyUser.DoesNotExist :
        messages.error(request,'چنین کاربری وجود ندارد')
        return Response({'success': False} , status=404)



@api_view(['POST'])
def login_view(request):
       try :
                data = JSONParser().parse(request)
                user = authenticate(request=request , uniqueMail=data['uniqueMail'] , password=data['password'] , phoneNumber=data['phoneNumber'])
                if user is not None :
                    response = JsonResponse({
                        'user' : str(user)
                    }, status=status.HTTP_200_OK)
                    response.set_cookie(key='temporary-data',  value=json.dumps({
                        'username' : user.username ,
                        'phoneNumber' : user.phoneNumber,
                        'mode' : 'Login'
                    }) , max_age=10*60, httponly=True)
                    return response
                else :
                     messages.error(request, 'اطلاعات وارد شده صحیح نیست')
                     return JsonResponse({
                         'user' : str(user)
                     }, status=status.HTTP_400_BAD_REQUEST)
       except Exception as e :
                messages.error(request,'خطایی در ورود کاربر رخ داده است')
                return JsonResponse({
                    'user' : str(None)
                } , status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def register_view(request):
        data = JSONParser().parse(request)
        user = UserSerializer(data=data)
        if user.is_valid() :
             response = Response({'data': user.data}, status=201)
             data = user.data
             data['mode'] = 'Register'
             response.set_cookie(key='temporary-data' , value=json.dumps(data), max_age=10*60)
             return response
        else:
             if (not data['uniqueMail']) or (not data['username']) : messages.error(request , 'ایمیل و نام کاربری باید وارد شود')
             elif ('username' in user.errors and data['username']) or ('uniqueMail' in user.errors and data['uniqueMail']) : messages.error(request , f'ایمیل یا نام کاربری از قبل وجود دارد')
             elif 'phoneNumber' in user.errors : messages.error(request , 'شماره وارد شده باید ده رقمی و بدون صفر اول وارد شود')






def authentication(request , path) :
    if path == 'login' :
         template = render_to_string('loginTemplate.html' , request=request)
    if path == 'register' :
         template = render_to_string('register.html' , request=request)
    if path == 'retrievePass' :
         template = render_to_string('password-retrieve.html' , request=request)

    if path == 'retrieveCodeValidation' :
       try :
             data = request.COOKIES.get('temporary-data' , '{}')
             data = json.loads(data)
             phoneNumber = data['phoneNumber']
             deleteUserCodes(data)
             random_code = RandomCode(related_to=data['username'])
             random_code.save()
             send_message(phoneNumber, random_code)
             template = render_to_string('retrieveCodeValidation.html', request=request)
       except Exception as e :
             messages.error(request, f'   درخواست به دلیل طولانی شدن پروسه منقضی شده ، مجددا امتحان فرمایید')
             return redirect('/auth/login')

    if path == 'makeNewPassword' :
         template = render_to_string('makeNewPassword.html' , request=request)

    return render(request, 'auth.html', {'template': template})

