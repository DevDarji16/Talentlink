from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from users.models import Application,Job
from users.serializers import ApplicationSerializer,ApplicationDetailSerializer
from users.models import UserProfile
from jobstatus.models import JobStatus

@api_view(['POST'])
def apply_to_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.role != "freelancer":
        return Response({"error": "Only freelancers can apply"}, status=status.HTTP_403_FORBIDDEN)

    if Application.objects.filter(job=job, freelancer=user_profile).exists():
        return Response({"error": "You already applied"}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data.copy()
    data["job"] = job.id   # This will now work (expects ID, not dict)

    serializer = ApplicationSerializer(data=data)
    if serializer.is_valid():
        serializer.save(
            freelancer=user_profile,
            client=job.client,
            status='pending'
        )
        # Return with nested detail serializer for response
        return Response(ApplicationDetailSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def pending_applications(request):
    user_profile = UserProfile.objects.get(user=request.user)  # safer than request.user.profile
    applications = Application.objects.filter(
        client=user_profile, status="pending"
    ).order_by('-created_at')

    serializer = ApplicationDetailSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_application_status(request, job_id):
    user_profile = request.user.profile  # current freelancer
    
    # 1. Check if job exists
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

    # 2. Check if freelancer has applied
    application = Application.objects.filter(
        job=job,
        freelancer=user_profile
    ).first()

    if not application:
        return Response({"status": "not_applied"})

    # 3. If application exists, check status
    if application.status == "pending":
        return Response({"status": "pending"})

    if application.status == "hired":
        # Check if there's an active JobStatus record
        ongoing = JobStatus.objects.filter(
            job=job,
            freelancer=user_profile
        ).exists()
        if ongoing:
            return Response({"status": "ongoing"})
        return Response({"status": "hired"})

    if application.status == "rejected":
        return Response({"status": "rejected"})

    # fallback
    return Response({"status": application.status})

@api_view(['GET'])
def freelancer_applications(request):
    try:
        freelancer = request.user.profile
        applications = Application.objects.filter(
            freelancer=freelancer,
            status='pending'
        ).order_by('-created_at')
        
        serializer = ApplicationDetailSerializer(applications, many=True)
        return Response({
            "applications": serializer.data,
            "count": applications.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)