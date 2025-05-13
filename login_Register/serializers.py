from rest_framework import serializers
from django.contrib.auth.models import User
from homePage.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username' , 'uniqueMail' , 'phoneNumber' , 'password']

    def create(self, validated_data):
         user = MyUser(username=validated_data['username'] , uniqueMail=validated_data['uniqueMail'] , phoneNumber=validated_data['phoneNumber'])
         user.set_password(validated_data['password'])
         user.save()
         return user

