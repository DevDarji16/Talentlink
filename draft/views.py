from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Draft
from users.models import UserProfile, FreelanceGroup
from .serializers import DraftSerializer
from wallet.models import WalletTransaction
from jobstatus.models import JobStatus

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
    drafts = Draft.objects.filter(client=request.user.profile,is_accepted=False)
    return Response({"drafts": DraftSerializer(drafts, many=True).data})


@api_view(['POST'])
def respond_to_draft(request, draft_id):
    action = request.data.get('action')  # 'accept' or 'reject'

    try:
        draft = Draft.objects.get(id=draft_id, client=request.user.profile)
    except Draft.DoesNotExist:
        return Response({"error": "Draft not found"}, status=404)

    if action == 'accept':
        client = request.user.profile

        # ✅ Check wallet balance
        if client.wallet_balance < draft.price:
            return Response(
                {"error": "Insufficient balance in wallet"},
                status=400
            )

        # ✅ Deduct money from wallet
        client.wallet_balance -= draft.price
        client.save()

        # ✅ Record wallet transaction
        WalletTransaction.objects.create(
            user=client,
            tx_type="debit",
            amount=draft.price,
            balance_after=client.wallet_balance,
            reference=f"Payment for draft #{draft.id}"
        )

        # ✅ Create JobStatus with price stored
        JobStatus.objects.create(
            draft=draft,
            client=draft.client,
            freelancer=draft.freelancer,
            group=draft.group,
            status='ongoing',
            price=draft.price, # store the money value
            is_draft=True
        )

        draft.is_accepted = True
        draft.save()

        message = "Draft accepted! Project started and payment deducted."
    else:
        message = "Draft rejected."

    return Response({"message": message})


@api_view(['GET'])
def search_clients(request):
    username = request.GET.get('username', '')
    clients = UserProfile.objects.filter(
        username__icontains=username,
        role__in=['client', 'both']
    )

    data = [
        {
            "id": c.id,
            "username": c.username,
            "fullname": c.fullname,
            "profilepic": c.profilepic,  # ✅ send photo
        }
        for c in clients
    ]
    return Response({"results": data})


@api_view(['GET'])
def draft_detail(request, draft_id):
    try:
        draft = Draft.objects.get(id=draft_id)
    except Draft.DoesNotExist:
        return Response({"error": "Draft not found"}, status=404)

    serializer = DraftSerializer(draft)
    return Response({"draft": serializer.data})
