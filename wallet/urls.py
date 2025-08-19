from django.urls import path
from .views import add_money, wallet_details

urlpatterns = [
    path("add/", add_money, name="add-money"),
    path("details/", wallet_details, name="wallet-details"),
]