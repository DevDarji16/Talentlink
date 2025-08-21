from django.urls import path
from . import views

urlpatterns = [
   
    path("jobstatus/<int:job_id>/reviews/", views.leave_review, name="leave_review"),
    path("reviews/<int:user_id>/", views.user_reviews, name="user-reviews"),
    path("reviews/job/<int:job_id>/mine/", views.my_job_review, name="my_job_review"),
    path("reviews/gig/<int:gig_id>/", views.gig_reviews, name="gig-reviews"),
]
