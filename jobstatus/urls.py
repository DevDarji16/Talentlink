from django.urls import path
from .views import ongoing_freelancer_jobs, ongoing_client_jobs,completed_freelancer_jobs,completed_client_jobs


urlpatterns = [
    # Freelancer endpoints
    path('freelancer/ongoing/', ongoing_freelancer_jobs, name='ongoing-freelancer-jobs'),
    path('freelancer/completed/', completed_freelancer_jobs, name='completed-freelancer-jobs'),
    
    # Client endpoints
    path('client/ongoing/', ongoing_client_jobs, name='ongoing-client-jobs'),
    path('client/completed/', completed_client_jobs, name='completed-client-jobs'),
]