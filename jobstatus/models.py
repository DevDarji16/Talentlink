from django.db import models
from users.models import UserProfile,FreelanceGroup,Job,Gig,Application
from draft.models import Draft
# Create your models here.

class JobStatus(models.Model):
    # Job Sources (only one will be set)
    job = models.ForeignKey(Application, null=True, blank=True, on_delete=models.SET_NULL)  
    gig = models.ForeignKey(Gig, null=True, blank=True, on_delete=models.SET_NULL)  
    draft = models.ForeignKey(Draft, null=True, blank=True, on_delete=models.SET_NULL)
    is_gig= models.BooleanField(default=False)
    is_job= models.BooleanField(default=False)
    is_draft= models.BooleanField(default=False)
    # Participants
    client = models.ForeignKey(UserProfile, related_name='client_jobs', on_delete=models.CASCADE)
    freelancer = models.ForeignKey(UserProfile, related_name='freelancer_jobs', on_delete=models.CASCADE)
    group = models.ForeignKey(FreelanceGroup, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status Tracking
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('Submitted', 'Submitted'),
        ('cancelled', 'Cancelled')
    ]
    submitted_file = models.URLField(null=True, blank=True)
    submission_message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    created_at = models.DateTimeField(auto_now_add=True)