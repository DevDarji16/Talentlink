from django.shortcuts import render
from jobstatus.models import JobStatus
from users.models import UserProfile,Gig
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg
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
    # if Review.objects.filter(reviewer=reviewer, job=job).exists():
    #     return Response({"error": "You already reviewed this job"})

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

# ✅ Get MY review on a job (to check if already submitted)
@api_view(["GET"])
def my_job_review(request, job_id):
    reviewer = request.user.profile
    try:
        job = JobStatus.objects.get(id=job_id)
    except JobStatus.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

    review = Review.objects.filter(job=job, reviewer=reviewer).first()
    if not review:
        return Response({"message": "No review yet"}, status=200)

    return Response(ReviewSerializer(review).data)


@api_view(["GET"])
def gig_reviews(request, gig_id):
    try:
        gig = Gig.objects.get(id=gig_id)
    except Gig.DoesNotExist:
        return Response({"error": "Gig not found"}, status=404)

    # ✅ fetch all completed jobstatus records linked to this gig
    jobs = JobStatus.objects.filter(gig=gig, status="completed")
    if not jobs.exists():
        return Response({
            "gig_id": gig_id,
            "gig_title": gig.title,
            "avg_rating": 0,
            "reviews": []
        })

    reviews = Review.objects.filter(job__in=jobs).order_by("-created_at")
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0

    return Response({
        "gig_id": gig_id,
        "gig_title": gig.title,
        "avg_rating": round(avg_rating, 2),
        "reviews": ReviewSerializer(reviews, many=True).data
    })