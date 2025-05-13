from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


def check_token(get_response):
    def middleware(request):
         if request.COOKIES.get('sessionid') and request.path== '/':
              new_segment = f'authHome'
              request.path += new_segment  # Append to the path
              request.path_info += new_segment  # Append to path_info
              request.META['PATH_INFO'] += new_segment
              response = get_response(request)
              return response

         if request.path == '/' :
              new_access_token = None
              access_token = request.COOKIES.get('access')
              refresh_token = request.COOKIES.get('refresh')
              if access_token :
                   access_token_obj = AccessToken(access_token)
                   new_segment = 'authHome'
                   request.path += new_segment  # Append to the path
                   request.path_info += new_segment  # Append to path_info
                   request.META['PATH_INFO'] += new_segment

              elif refresh_token :
                   refresh_token_obj = RefreshToken(refresh_token)
                   new_access_token = refresh_token_obj.access_token
                   new_segment = f'authHome'
                   request.path += new_segment  # Append to the path
                   request.path_info += new_segment  # Append to path_info
                   request.META['PATH_INFO'] += new_segment
              else :
                   new_segment = f'anonymousHome'
                   request.path += new_segment
                   request.path_info += new_segment  # Append to path_info
                   request.META['PATH_INFO'] += new_segment


         response = get_response(request)
         if (request.path=='/anonymousHome' or  request.path=='/authHome') and new_access_token :
              response.set_cookie(key='access', value=new_access_token , httponly=True , max_age=1800)
         return response


    return middleware