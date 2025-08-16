from django.db import models
from users.models import UserProfile,FreelanceGroup
# Create your models here.
class Draft(models.Model):
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='freelancer_drafts')
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_drafts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    group = models.ForeignKey(FreelanceGroup, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)


