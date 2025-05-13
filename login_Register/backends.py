from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend, UserModel
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class MyUserAuthBackend(BaseBackend):
    def authenticate(self,request, uniqueMail=None, password=None, phoneNumber=None, **kwargs):
        UserModel = get_user_model()

        try:
            if uniqueMail and phoneNumber and password :
                 user = UserModel.objects.get(uniqueMail=uniqueMail, phoneNumber=phoneNumber)
                 if user.check_password(password):
                     return user
                 else :
                     return None


        except UserModel.DoesNotExist:
            return None  # User not found

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None