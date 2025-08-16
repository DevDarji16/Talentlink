from django.shortcuts import render
from .models import GigApplication
from .serializers import GigApplicationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from jobstatus.models import JobStatus
from rest_framework import generics,status
# Create your views here.

@api_view(['POST'])
def apply_to_gig(request, gig_id):
    try:
        gig = Gig.objects.get(id=gig_id)
    except Gig.DoesNotExist:
        return Response({"error": "Gig not found"}, status=404)

    # Auto-fill price from gig (frontend can override if needed)
    data = request.data.copy()
    data['price'] = gig.price
    
    serializer = GigApplicationSerializer(data={
        'gig': gig.id,
        'client': request.user.profile,
        'freelancer': gig.freelancer,
        'message': data.get('message'),
        'price': data['price']
    })

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def freelancer_applications(request):
    applications = GigApplication.objects.filter(
        freelancer=request.user.profile
    ).order_by('-created_at')
    serializer = GigApplicationSerializer(applications, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def client_applications(request):
    applications = GigApplication.objects.filter(
        client=request.user.profile
    ).order_by('-created_at')
    serializer = GigApplicationSerializer(applications, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def respond_to_gig_application(request, application_id):
    try:
        application = GigApplication.objects.get(
            id=application_id,
            freelancer=request.user.profile
        )
    except GigApplication.DoesNotExist:
        return Response({"error": "Application not found"}, status=404)

    action = request.data.get('action')  # 'accept' or 'reject'
    
    if action == 'accept':
        application.status = 'accepted'
        application.save()
        
        # Create JobStatus
        JobStatus.objects.create(
            gig=application.gig,
            client=application.client,
            freelancer=application.freelancer,
            status='ongoing'
        )
        
        return Response({"message": "Application accepted!"})
    
    elif action == 'reject':
        application.status = 'rejected'
        application.save()
        return Response({"message": "Application rejected"})
    
    return Response({"error": "Invalid action"}, status=400)