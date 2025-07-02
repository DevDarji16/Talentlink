from django.urls import path
from .views import check_user,check_username,create_profile,get_profile,check_login

urlpatterns=[

    path('check_user/',check_user),
    path('check_username/',check_username),
    path('create_profile/',create_profile),
    path('get_profile/',get_profile),
    path('check_login/',check_login),

]
