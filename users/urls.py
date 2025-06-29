from django.urls import path
from .views import check_user

urlpatterns=[

    path('check_user/',check_user),#not used

]
