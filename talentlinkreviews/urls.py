from django.urls import path
from .views import add_review, get_reviews

urlpatterns = [
    path('reviews/', get_reviews, name='get_reviews'),
    path('reviews/add/', add_review, name='add_review'),
]
