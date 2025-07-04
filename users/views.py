from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile
from allauth.socialaccount.models import SocialAccount
from .serializers import UserProfileSerializer,SocialAccountSerializer

# Create your views here.


@api_view(['GET'])
def check_user(request):
    exists=UserProfile.objects.filter(user=request.user).exists()
    return Response({'exists':exists})

@api_view(["POST"])
def check_username(request):
    username=request.data.get('username')
    exist=UserProfile.objects.filter(username=username).exists()
    return Response({'available':not exist})

@api_view(['POST'])
def create_profile(request):
    print(request.data)
    serializer=UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def get_profile(request):
    userprofile=UserProfile.objects.get(user=request.user)
    socialprofile=SocialAccount.objects.get(user=request.user)
    userserialized=UserProfileSerializer(userprofile).data
    socialserialized=SocialAccountSerializer(socialprofile).data
    return Response({'userprofile':userserialized,'social':socialserialized})


@api_view(['GET'])
def check_login(request):
    if request.user.is_authenticated:
        data=UserProfile.objects.get(user=request.user)
        details=UserProfileSerializer(data).data
        return Response({
            'authenticated':True,
            'username': request.user.username,
            'email': request.user.email,
            'details':details

        })
    return Response({
        'authenticated':False
    })


@api_view(['GET', 'POST'])
def gigs_view(request):
    if request.method == 'GET':
        gigs = Gig.objects.all()
        serializer = GigSerializer(gigs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['freelancer'] = request.user.profile.id
        serializer = GigSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



@api_view(['GET', 'POST'])
def jobs_view(request):
    if request.method == 'GET':
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['client'] = request.user.profile.id
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)