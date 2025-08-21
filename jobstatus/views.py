from django.shortcuts import render
from .models import JobStatus
from .serializers import JobStatusSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wallet.models import WalletTransaction

@api_view(['GET'])
def ongoing_freelancer_jobs(request):
    jobs = JobStatus.objects.filter(
        status='ongoing',
        freelancer=request.user.profile
    ).order_by("-created_at")

    print('jobs=>',jobs)
    return Response({'data':JobStatusSerializer(jobs, many=True).data})


@api_view(['GET'])
def ongoing_client_jobs(request):
    jobs = JobStatus.objects.filter(
        status='ongoing',
        client=request.user.profile
    ).order_by("-created_at")

    print('jobs=>',jobs)
    return Response({'data':JobStatusSerializer(jobs, many=True).data})

@api_view(['GET'])
def completed_freelancer_jobs(request):
    jobs = JobStatus.objects.filter(
        status='completed',
        freelancer=request.user.profile
    ).order_by('-created_at')
    return Response(JobStatusSerializer(jobs, many=True).data)

@api_view(['GET'])
def completed_client_jobs(request):
    jobs = JobStatus.objects.filter(
        status='completed',
        client=request.user.profile
    ).order_by('-created_at')
    return Response(JobStatusSerializer(jobs, many=True).data)

@api_view(['POST'])
def submit_work(request, job_id):
    try:
        job = JobStatus.objects.get(id=job_id, freelancer=request.user.profile)
    except JobStatus.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

    if job.status != "ongoing":
        return Response({"error": "Job not in ongoing state"}, status=400)

    job.submission_message = request.data.get("message", "")
    job.submitted_file = request.data.get("file_url")  # ✅ Cloudinary URL
    job.status = "submitted"
    job.save()

    return Response({"message": "Work submitted successfully!", "file_url": job.submitted_file})



@api_view(['GET'])
def job_detail(request, job_id):
    try:
        job = JobStatus.objects.get(id=job_id)
    except JobStatus.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

    return Response(JobStatusSerializer(job).data)


@api_view(['POST'])
def respond_submission(request, job_id):
    try:
        job = JobStatus.objects.get(id=job_id, client=request.user.profile)
    except JobStatus.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

    action = request.data.get("action")  # "accept" or "request_changes"

    if action == "accept":
        job.status = "completed"
        job.save()

        # ✅ Credit freelancer’s wallet
        freelancer = job.freelancer
        freelancer.wallet_balance += job.price
        freelancer.save()

        WalletTransaction.objects.create(
            user=freelancer,
            tx_type="credit",
            amount=job.price,
            balance_after=freelancer.wallet_balance,
            reference=f"Completed job #{job.id}"
        )

        return Response({"message": "Job marked completed. Payment released."})

    elif action == "request_changes":
        job.status = "ongoing"
        job.save()
        return Response({"message": "Client requested changes. Job set back to ongoing."})

    return Response({"error": "Invalid action. Use 'accept' or 'request_changes'"}, status=400)

@api_view(['GET'])
def completed_jobs(request, role):
    if role == "client":
        jobs = JobStatus.objects.filter(client=request.user.profile, status="completed").order_by("-created_at")
    else:
        jobs = JobStatus.objects.filter(freelancer=request.user.profile, status="completed").order_by("-created_at")

    return Response(JobStatusSerializer(jobs, many=True).data)


@api_view(['GET'])
def client_submitted_jobs(request):
    jobs = JobStatus.objects.filter(
        client=request.user.profile,
        status="submitted"
    ).order_by("-created_at")
    return Response(JobStatusSerializer(jobs, many=True).data)


# 🔹 Freelancer submitted jobs (all jobs submitted by this freelancer)
@api_view(['GET'])
def freelancer_submitted_jobs(request):
    jobs = JobStatus.objects.filter(
        freelancer=request.user.profile,
        status="submitted"
    ).order_by("-created_at")
    return Response(JobStatusSerializer(jobs, many=True).data)