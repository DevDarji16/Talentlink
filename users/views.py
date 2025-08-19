from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile,Gig,Job,Application,FreelanceGroup,Notification,GroupInvite
from allauth.socialaccount.models import SocialAccount
from .serializers import UserProfileSerializer,SocialAccountSerializer,GigSerializer,JobSerializer,ApplicationSerializer,FreelanceGroupSerializer,NotificationSerializer,GroupInviteSerializer
from rest_framework import generics,status
from wallet.models import WalletTransaction
from jobstatus.models import JobStatus
# Create your views here.

class FreelanceGroupDetailView(generics.RetrieveAPIView):
    queryset = FreelanceGroup.objects.all()
    serializer_class = FreelanceGroupSerializer

@api_view(['GET'])
def get_groups(request):
    data=FreelanceGroup.objects.all().order_by('-created_at')
    serializer=FreelanceGroupSerializer(data,many=True)
    return Response({'groups':serializer.data})

@api_view(['POST'])
def create_group(request):
    serializer = FreelanceGroupSerializer(data=request.data)
    if serializer.is_valid():
        group = serializer.save(leader=request.user.profile)
        # group.members.add(request.user.profile)
        
        group_data = {
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'leader_id': request.user.profile.id,
            'created_at': group.created_at.isoformat()
        }
        
        profile = request.user.profile
        if not profile.leader_of:  # Initialize if empty
            profile.leader_of = []
        
        profile.leader_of.append(group_data)  # Append full group data
        profile.save()
        
        return Response({
            'message': 'success',
            'group': group_data  # Return same format for frontend
        })
    
    return Response({'error': serializer.errors}, status=400)

@api_view(['GET'])
def search_users(request):
    query=request.GET.get('q')
    if not query:
        return Response({"results": []})
    users=UserProfile.objects.filter(role='freelancer').filter(username__icontains=query) | UserProfile.objects.filter(role='freelancer').filter(fullname__icontains=query) 
    users = users.exclude(id=request.user.profile.id)
    serializer = UserProfileSerializer(users, many=True)

    return Response({'results':serializer.data})


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
        gigs = Gig.objects.filter(is_active=True).order_by('-created_at')
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
        jobs = Job.objects.filter(status="pending").order_by('-created_at')
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
def send_group_invite(request, group_id):
    sender_profile = UserProfile.objects.get(user=request.user)
    receiver_id = request.data.get("receiver_id")

    # 1. Get group
    try:
        group = FreelanceGroup.objects.get(id=group_id)
    except FreelanceGroup.DoesNotExist:
        return Response({"error": "Group not found"}, status=404)

    # 2. Check leader
    if group.leader != sender_profile:
        return Response({"error": "Only leader can send invites"}, status=403)

    # 3. Get receiver
    try:
        receiver_profile = UserProfile.objects.get(id=receiver_id)
    except UserProfile.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    # 4. Already a member?
    if receiver_profile in group.members.all():
        return Response({"error": "User already in group"}, status=400)

    # 5. Already invited?
    if GroupInvite.objects.filter(
        sender=sender_profile,
        receiver=receiver_profile,
        group=group,
        status="pending"
    ).exists():
        return Response({"error": "Invite already pending"}, status=400)

    # 6. Create invite
    invite = GroupInvite.objects.create(
        sender=sender_profile,
        receiver=receiver_profile,
        group=group
    )

    # 7. Create notification
    Notification.objects.create(
        user=receiver_profile,
        type="group_invite",
        message=f"{sender_profile.username} invited you to join {group.name}",
        related_group=group,
        related_invite=invite
    )

    return Response({"message": "Invite sent", "invite_id": invite.id}, status=201)


@api_view(['POST'])
def respond_group_invite(request, invite_id):
    action = request.data.get("action")  
    notification_id = request.data.get("n_id")  
    user_profile = UserProfile.objects.get(user=request.user)
    
    try:
        invite = GroupInvite.objects.get(id=invite_id)
        n_id = Notification.objects.get(id=notification_id)
    except GroupInvite.DoesNotExist:
        return Response({"error": "Invite not found"}, status=404)

    # Only receiver can respond
    if invite.receiver != user_profile:
        return Response({"error": "Not your invite"}, status=403)

    if action == "accept":
        invite.group.members.add(user_profile)
        Notification.objects.create(
            user=invite.sender,
            type="group_update",
            message=f"{user_profile.username} accepted your invite to {invite.group.name}",
            related_group=invite.group
        )
        invite.delete()  
        n_id.delete()
    elif action == "decline":
        invite.delete() 
        n_id.delete()
    else:
        return Response({"error": "Invalid action"}, status=400)

    return Response({"message": f"Invite {action}ed and removed"}, status=200)


@api_view(['PATCH'])
def mark_notification_read(request, pk):
    try:
        notification = Notification.objects.get(pk=pk, user=request.user.profile)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

    notification.is_read = True
    notification.save()
    return Response({"message": "Notification marked as read"})

@api_view(['GET'])
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user.profile).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def create_application(request):
    # Get required data
    job_id = request.data.get('job_id')
    proposal_text = request.data.get('proposal_text')
    apply_as = request.data.get('apply_as', 'individual')  # 'individual' or 'group'
    group_id = request.data.get('group_id')

    # Validate job exists
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

    # Validate group (if applying as group)
    group = None
    if apply_as == 'group':
        if not group_id:
            return Response({"error": "Group ID required for group applications"}, status=400)
        try:
            group = FreelanceGroup.objects.get(id=group_id, leader=request.user.profile)
        except FreelanceGroup.DoesNotExist:
            return Response({"error": "Group not found or you're not the leader"}, status=403)

    # Create application
    application = Application.objects.create(
        job=job,
        freelancer=request.user.profile,
        client=job.client,
        proposal_text=proposal_text,
        is_group=(apply_as == 'group'),
        is_individual=(apply_as == 'individual'),
        group=group
    )

    return Response({
        "message": "Application submitted!",
        "application_id": application.id
    }, status=201)


@api_view(['GET'])
def list_job_applications(request, job_id):
    # Check if job exists and user is the owner
    try:
        job = Job.objects.get(id=job_id, client=request.user.profile)
    except Job.DoesNotExist:
        return Response({"error": "Job not found or unauthorized"}, status=404)

    # Split applications by type
    individual_apps = job.applications.filter(is_individual=True)
    group_apps = job.applications.filter(is_group=True)

    return Response({
        "individual": ApplicationSerializer(individual_apps, many=True).data,
        "groups": ApplicationSerializer(group_apps, many=True).data
    })

@api_view(['POST'])
def respond_to_application(request, application_id):
    action = request.data.get('action')  # 'accept' or 'reject'

    try:
        application = Application.objects.get(id=application_id, client=request.user.profile)
    except Application.DoesNotExist:
        return Response({"error": "Application not found"}, status=404)

    if action == 'accept':
        client = request.user.profile

        # ✅ Check wallet balance
        if client.wallet_balance < application.proposed_price:
            return Response(
                {"error": "Insufficient balance in wallet"},
                status=400
            )

        # ✅ Deduct money from wallet
        client.wallet_balance -= application.proposed_price
        client.save()

        # ✅ Record wallet transaction
        WalletTransaction.objects.create(
            user=client,
            tx_type="debit",
            amount=application.proposed_price,
            balance_after=client.wallet_balance,
            reference=f"Payment for application #{application.id}"
        )

        # ✅ Create JobStatus entry
        JobStatus.objects.create(
            job=application,
            client=application.job.client,
            freelancer=application.freelancer,
            group=application.group,
            status='ongoing',
            price=application.proposed_price,  # store the money value
            is_job=True  # distinguish from draft flow
        )

        application.status = 'hired'
        application.job.status = "hired"  # update Job too
        application.job.save()
        application.save()

        message = "Application accepted! Project started and payment deducted."
    else:
        message = "Application rejected."
        application.status = "rejected"
        application.save()

    return Response({"message": message})



@api_view(['POST'])
def disable_gig(request, gig_id):
    try:
        gig = Gig.objects.get(id=gig_id, freelancer=request.user.profile)
    except Gig.DoesNotExist:
        return Response({"error": "Gig not found"}, status=404)

    gig.is_active = False
    gig.save()
    return Response({"message": "Gig disabled successfully"})


@api_view(['POST'])
def enable_gig(request, gig_id):
    try:
        gig = Gig.objects.get(id=gig_id, freelancer=request.user.profile)
    except Gig.DoesNotExist:
        return Response({"error": "Gig not found"}, status=404)

    gig.is_active = True
    gig.save()
    return Response({"message": "Gig Enabled successfully"})

@api_view(['POST'])
def edit_gig(request, gig_id):
    try:
        gig = Gig.objects.get(id=gig_id, freelancer=request.user.profile)
    except Gig.DoesNotExist:
        return Response({"error": "Gig not found"}, status=404)

    gig.title = request.data.get("title", gig.title)
    gig.description = request.data.get("description", gig.description)
    gig.price = request.data.get("price", gig.price)
    gig.save()

    return Response({"message": "Gig updated", "gig": GigSerializer(gig).data})

    