from django.urls import path
from .views import (
    apply_to_gig,
    freelancer_applications,
    client_applications,
    respond_to_gig_application
)

urlpatterns = [
    # Application endpoints
    path('gigs/<int:gig_id>/apply/', apply_to_gig, name='apply-to-gig'),
    path('applications/freelancer/', freelancer_applications, name='freelancer-applications'),
    path('applications/client/', client_applications, name='client-applications'),
    path('applications/<int:application_id>/respond/', respond_to_gig_application, name='respond-to-application'),
]