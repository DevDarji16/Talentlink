from django.db import models
from jobstatus.models import JobStatus
from users.models import UserProfile,FreelanceGroup
# Create your models here.
class Review(models.Model):
    reviewer = models.ForeignKey(UserProfile, related_name="written_reviews", on_delete=models.CASCADE)
    reviewee_user = models.ForeignKey(UserProfile, null=True, blank=True, related_name="received_reviews", on_delete=models.CASCADE)
    reviewee_group = models.ForeignKey(FreelanceGroup, null=True, blank=True, related_name="received_reviews", on_delete=models.CASCADE)

    job = models.ForeignKey(JobStatus, on_delete=models.CASCADE)  # ✅ ties review to a completed job

    rating = models.IntegerField()  # 1–5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reviewer", "job")  # one review per person per job
