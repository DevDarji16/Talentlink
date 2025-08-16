from django.shortcuts import render
from .models import JobStatus
from .serializers import JobStatusSerializer
from rest_framework.decorators import api_view

@api_view(['GET'])
def ongoing_freelancer_jobs(request):
    jobs = JobStatus.objects.filter(
        status='ongoing',
        freelancer=request.user.profile
    )
    return Response(JobStatusSerializer(jobs, many=True).data)


@api_view(['GET'])
def ongoing_client_jobs(request):
    jobs = JobStatus.objects.filter(
        status='ongoing',
        client=request.user.profile
    )
    return Response(JobStatusSerializer(jobs, many=True).data)

@api_view(['GET'])
def completed_freelancer_jobs(request):
    jobs = JobStatus.objects.filter(
        status='completed',
        freelancer=request.user.profile
    )
    return Response(JobStatusSerializer(jobs, many=True).data)

@api_view(['GET'])
def completed_client_jobs(request):
    jobs = JobStatus.objects.filter(
        status='completed',
        client=request.user.profile
    )
    return Response(JobStatusSerializer(jobs, many=True).data)