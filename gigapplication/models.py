from django.db import models
from users.models import Gig,UserProfile
# Create your models here.
class GigApplication(models.Model):
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='applied_gigs')
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='received_gig_applications')
    message = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)