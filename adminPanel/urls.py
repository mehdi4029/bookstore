from django.urls import path
from adminPanel import views


urlpatterns = [
    path('login' , views.checkLogin , name='login'),
    path('createbook' , views.bookCreation , name='createbook'),
    path('createcategory' , views.categoryCreation , name='createcategory'),
]


