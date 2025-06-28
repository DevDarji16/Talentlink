from django.urls import path
from .views import signup_redirect

urlpatterns=[
    path('signup_redirect/',signup_redirect)
]