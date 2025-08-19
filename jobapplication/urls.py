from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_to_job, name='apply-to-job'),
    path("pending/", views.pending_applications, name="pending_applications"),
    path('status/<int:job_id>/', views.check_application_status, name='check-application-status'),
    path('freelancer/pending/', views.freelancer_applications, name='freelancer-applications'),


]
