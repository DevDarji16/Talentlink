from django.urls import path
from . import views

urlpatterns = [
   
    path("jobstatus/<int:job_id>/review/", views.leave_review, name="leave_review"),
    path("reviews/<int:user_id>/", views.user_reviews, name="user-reviews"),
]
