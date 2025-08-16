from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Draft
from users.models import UserProfile, FreelanceGroup
from .serializers import DraftSerializer

@api_view(['POST'])
def create_draft(request):
    data = request.data
    client_id = data.get('client_id')
    group_id = data.get('group_id', None)  # Optional

    # Validate client exists
    try:
        client = UserProfile.objects.get(id=client_id, role__in=['client', 'both'])
    except UserProfile.DoesNotExist:
        return Response({"error": "Client not found"}, status=404)

    # Validate group (if provided)
    group = None
    if group_id:
        try:
            group = FreelanceGroup.objects.get(id=group_id, leader=request.user.profile)
        except FreelanceGroup.DoesNotExist:
            return Response({"error": "Group not found or you're not the leader"}, status=403)

    # Create draft
    draft = Draft.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        price=data.get('price'),
        freelancer=request.user.profile,
        client=client,
        group=group
    )

    return Response({"id": draft.id}, status=201)


@api_view(['GET'])
def my_drafts(request):
    drafts = Draft.objects.filter(freelancer=request.user.profile)
    return Response({"drafts": DraftSerializer(drafts, many=True).data})

@api_view(['GET'])
def drafts_for_client(request):
    drafts = Draft.objects.filter(client=request.user.profile)
    return Response({"drafts": DraftSerializer(drafts, many=True).data})


@api_view(['POST'])
def respond_to_draft(request, draft_id):
    action = request.data.get('action')  # 'accept' or 'reject'
    
    try:
        draft = Draft.objects.get(id=draft_id, client=request.user.profile)
    except Draft.DoesNotExist:
        return Response({"error": "Draft not found"}, status=404)

    if action == 'accept':
        # Create JobStatus entry
        JobStatus.objects.create(
            draft=draft,
            client=draft.client,
            freelancer=draft.freelancer,
            group=draft.group,
            status='ongoing'
        )
        draft.is_accepted = True
        draft.save()
        message = "Draft accepted! Project started."
    else:
        message = "Draft rejected."

    return Response({"message": message})