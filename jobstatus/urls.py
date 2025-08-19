from django.urls import path
from .views import ongoing_freelancer_jobs, ongoing_client_jobs,completed_freelancer_jobs,completed_client_jobs
from . import views

urlpatterns = [
    # Freelancer endpoints
    path('jobstatus/freelancer/ongoing/', ongoing_freelancer_jobs, name='ongoing-freelancer-jobs'),
    path('jobstatus/freelancer/completed/', completed_freelancer_jobs, name='completed-freelancer-jobs'),
    
    path('jobstatus/client/ongoing/', ongoing_client_jobs, name='ongoing-client-jobs'),
    path('jobstatus/client/completed/', completed_client_jobs, name='completed-client-jobs'),


    path('job/<int:job_id>/submit/', views.submit_work, name="submit-work"),

    path('jobstatus/<int:job_id>/', views.job_detail, name="job-detail"),

    path('jobstatus/<int:job_id>/respond/', views.respond_submission, name="respond-submission"),

    path('jobs/completed/<str:role>/', views.completed_jobs, name="completed-jobs"),
    path('jobstatus/client/submitted/', views.client_submitted_jobs),
    path('jobstatus/freelancer/submitted/', views.freelancer_submitted_jobs),

]