from django.shortcuts import render
from jobstatus.models import JobStatus
from users.models import UserProfile
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(["POST"])
def leave_review(request, job_id):
    try:
        job = JobStatus.objects.get(id=job_id,status='completed')
    except JobStatus.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

    if job.status != "completed":
        return Response({"error": "Can only review completed jobs"}, status=400)

    reviewer = request.user.profile
    print('reviewer',reviewer)
    print('reviewer data',request.data)
    rating = request.data.get("rating")
    comment = request.data.get("comment", "")

    # Decide whether to review group or individual
    reviewee_user = None
    reviewee_group = None

    if job.group:  
        reviewee_group = job.group
    else:
        # client reviews freelancer, freelancer reviews client
        if reviewer == job.client:
            reviewee_user = job.freelancer
        elif reviewer == job.freelancer:
            reviewee_user = job.client
        else:
            return Response({"error": "You are not part of this job"}, status=403)

    # prevent duplicate reviews
    if Review.objects.filter(reviewer=reviewer, job=job).exists():
        return Response({"error": "You already reviewed this job"}, status=400)

    review = Review.objects.create(
        reviewer=reviewer,
        reviewee_user=reviewee_user,
        reviewee_group=reviewee_group,
        job=job,
        rating=rating,
        comment=comment
    )

    return Response(ReviewSerializer(review).data, status=201)

@api_view(['GET'])
def user_reviews(request, user_id):
    try:
        profile = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    reviews = profile.received_reviews.all().order_by("-created_at")
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0

    return Response({
        "user": profile.fullname,
        "avg_rating": round(avg_rating, 2),
        "reviews": ReviewSerializer(reviews, many=True).data
    })

