from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from allauth.socialaccount.models import SocialAccount
from rest_framework_simplejwt.tokens import RefreshToken


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        # Check if the Google account is already linked to a user
        google_id = sociallogin.account.extra_data.get('sub')

        # Extract data from Google
        email = sociallogin.account.extra_data.get('email')
        first_name = sociallogin.account.extra_data.get('given_name')
        last_name = sociallogin.account.extra_data.get('family_name')
        profile_picture_url = sociallogin.account.extra_data.get('picture')

        try:
           social_account = SocialAccount.objects.get(provider="google", uid=google_id)
           user = social_account.user
        except Exception as e :
                 try :
                        # Create a new user
                        MyUser = get_user_model()
                        user = MyUser(
                            uniqueMail=email,
                            username=first_name + last_name + str(google_id)[0:6],
                        )
                        user.set_unusable_password()
                        user.save()
                        sociallogin.connect(request, user)
                 except Exception as e :
                        MyUser = get_user_model()
                        user = MyUser.objects.get(uniqueMail=email)
                        sociallogin.connect(request,user)





    def save_user(self, request, sociallogin, form=None):
        # Do nothing here to prevent automatic user creation
        return None