from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile,Gig,Job,Application,FreelanceGroup
from allauth.socialaccount.models import SocialAccount
from .serializers import UserProfileSerializer,SocialAccountSerializer,GigSerializer,JobSerializer,ApplicationSerializer,FreelanceGroupSerializer
from rest_framework import generics
# Create your views here.

class FreelanceGroupDetailView(generics.RetrieveAPIView):
    queryset = FreelanceGroup.objects.all()
    serializer_class = FreelanceGroupSerializer

@api_view(['GET'])
def get_groups(request):
    data=FreelanceGroup.objects.all()
    serializer=FreelanceGroupSerializer(data,many=True)
    return Response({'groups':serializer.data})

@api_view(['POST'])
def create_group(request):
    serializer=FreelanceGroupSerializer(data=request.data)
    if serializer.is_valid():
        group=serializer.save(leader=request.user.profile)
        group.members.add(request.user.profile) 
        return Response({'message':'success',"data":serializer.data})
    return Response({'message':'group not created (create_group)!','error':serializer.errors})


@api_view(['GET'])
def my_groups(request):
    user_groups=request.user.profile.led_groups.all()
    serializer=FreelanceGroupSerializer(user_groups,many=True)
    return Response({'groups':serializer.data})


@api_view(['GET'])
def joined_groups(request):
    user_joined_groups=request.user.profile.groups.all()
    serializer=FreelanceGroupSerializer(user_joined_groups,many=True)
    return Response({'groups':serializer.data})

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
        try:
            data=UserProfile.objects.get(user=request.user)
            details=UserProfileSerializer(data).data
            return Response({
                'authenticated':True,
                'username': request.user.username,
                'email': request.user.email,
                'details':details

            })
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found."})
    return Response({
        'authenticated':False
    })


@api_view(['PATCH'])
def update_profile(request):
    if request.user.is_authenticated:
        try:
            user=UserProfile.objects.get(user=request.user)
            serializer=UserProfileSerializer(user,data=request.data,partial=True)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"})
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Profile Updated Successfully'})

@api_view(['POST'])
def add_project(request):
    profile = UserProfile.objects.get(user=request.user)
    project = {
        "title": request.data.get("title"),
        "link": request.data.get("link"),
        "description": request.data.get("description"),
        "skills": request.data.get("skills"),
        "image": request.data.get("image")

    }
    if profile.projects is None:
        profile.projects=[]

    profile.projects.append(project)
    profile.save()
    return Response({'message': 'Project added successfully'})

@api_view(['PATCH'])
def edit_project(request):
    profile = UserProfile.objects.get(user=request.user)


    index = int(request.data.get("index", -1))
    updated_project = request.data.get("project", {})

    if profile.projects is None or index < 0 or index >= len(profile.projects):
        return Response({"error": "Invalid index"}, status=400)

    profile.projects[index] = updated_project
    profile.save()

    return Response({"message": "Project updated"})


@api_view(['DELETE'])
def delete_project(request):
    profile = UserProfile.objects.get(user=request.user)
    index = int(request.data.get("index", -1))

    if profile.projects is None or index < 0 or index >= len(profile.projects):
        return Response({"error": "Invalid project index"}, status=400)

    profile.projects.pop(index)
    profile.save()

    return Response({"message": "Project deleted successfully"})



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
            serializer.save(freelancer=request.user.profile)
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
            serializer.save(client=request.user.profile)
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET'])
def get_all_freelancers(request):
    freelancers = UserProfile.objects.filter(role__in=['freelancer', 'both'])
    serializer = UserProfileSerializer(freelancers, many=True)
    return Response({'freelancers': serializer.data})


@api_view(['GET'])
def get_freelancer_by_username(request, username):
    try:
        
        profile = UserProfile.objects.get(username=username,role__in=['freelancer','both'])
        serializer = UserProfileSerializer(profile)
        return Response({'userprofile': serializer.data})
    except UserProfile.DoesNotExist:
        return Response({'error': 'Freelancer not found'})


@api_view(['GET'])
def get_person_by_username(request, username):
    try:
        
        profile = UserProfile.objects.get(username=username,role__in=['freelancer','both','client'])
        serializer = UserProfileSerializer(profile)
        return Response({'userprofile': serializer.data})
    except UserProfile.DoesNotExist:
        return Response({'error': 'Freelancer not found'})

@api_view(['GET'])
def get_client_by_username(request, username):
    try:
        
        profile = UserProfile.objects.get(username=username,role__in=['client'])
        serializer = UserProfileSerializer(profile)
        return Response({'userprofile': serializer.data})
    except UserProfile.DoesNotExist:
        return Response({'error': 'Freelancer not found'})

@api_view(['GET'])
def get_gig_by_id(request,id):
    try:
        gig=Gig.objects.get(id=id)
        serializer=GigSerializer(gig)
        return Response({'gig':serializer.data})
    except Gig.DoesNotExist:
        return Response({'error':'Gig not found'})


@api_view(['GET'])
def get_job_by_id(request,id):
    try:
        job=Job.objects.get(id=id)
        serializer=JobSerializer(job)
        return Response({'job':serializer.data})
    except Job.DoesNotExist:
        return Response({'error':'Job not found'})


        
@api_view(['POST'])
def apply_to_job(request, job_id):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role not in ['freelancer', 'both']:
        return Response({"detail": "Only freelancers can apply."}, status=403)
    
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({"detail": "Job not found."}, status=404)

    if Application.objects.filter(job=job, freelancer=user_profile).exists():
        return Response({"detail": "You have already applied."}, status=400)

    data = request.data.copy()
    data['freelancer'] = user_profile.id
    data['client'] = job.client.id
    data['job'] = job.id

    serializer = ApplicationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)



