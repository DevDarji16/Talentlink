from django.shortcuts import render
from .models import GigApplication
from .serializers import GigApplicationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from jobstatus.models import JobStatus
from rest_framework import generics,status
from users.models import Gig
from wallet.models import WalletTransaction
from wallet.serializers import WalletTransactionSerializer
# Create your views here.

@api_view(['POST'])
def apply_to_gig(request, gig_id):
    try:
        gig = Gig.objects.get(id=gig_id)
    except Gig.DoesNotExist:
        return Response({"error": "Gig not found"}, status=404)

    client = request.user.profile

    # ✅ Step 1: Wallet Balance Check
    if client.wallet_balance < float(gig.price):
        return Response(
            {"error": "Insufficient wallet balance"},
            status=400
        )

    data = request.data.copy()
    data['price'] = gig.price

    serializer = GigApplicationSerializer(data={
        'message': data.get('message'),
        'price': data['price']
    })

    if serializer.is_valid():
        # ✅ Step 2: Deduct money from client wallet
        client.wallet_balance -= gig.price
        client.save()

        # ✅ Step 3: Record transaction
        WalletTransaction.objects.create(
            user=client,
            tx_type="debit",
            amount=gig.price,
            balance_after=client.wallet_balance,
            reference=f"Applied to Gig #{gig.id}"
        )

        # ✅ Step 4: Save application
        application = serializer.save(
            client=client,
            freelancer=gig.freelancer,
            gig=gig
        )

        return Response(
            {
                'message': 'Application submitted successfully, payment deducted.',
                'data': GigApplicationSerializer(application).data,
                'balance': client.wallet_balance
            },
            status=201
        )

    return Response({'error': serializer.errors}, status=400)


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

    action = request.data.get('action')  # 'accepted' or 'rejected'
    client = application.client  

    if action == 'accepted':
        # ✅ Create JobStatus before deleting
        JobStatus.objects.create(
            gig=application.gig,
            client=application.client,
            freelancer=application.freelancer,
            price=application.price,
            status='ongoing',
            is_gig=True
        )
        application.delete()
        return Response({"message": "Application accepted and job created"})

    elif action == 'rejected':
        # ✅ Refund money back to client
        client.wallet_balance += application.price
        client.save()

        # ✅ Record refund transaction
        WalletTransaction.objects.create(
            user=client,
            tx_type="credit",
            amount=application.price,
            balance_after=client.wallet_balance,
            reference=f"Refund for rejected Gig Application #{application.id}"
        )

        application.delete()
        return Response({
            "message": "Application rejected, payment refunded.",
            "balance": client.wallet_balance
        })

    return Response({"error": "Invalid action. Use 'accepted' or 'rejected'"}, status=400)


from jobstatus.models import JobStatus

@api_view(['GET'])
def gig_application_status(request, gig_id):
    try:
        gig = Gig.objects.get(id=gig_id)
    except Gig.DoesNotExist:
        return Response({"error": "Gig not found"}, status=404)

    # ✅ Check if job is already ongoing
    job = JobStatus.objects.filter(gig=gig, status="ongoing").first()
    if job:
        return Response({
            "in_progress": True,
            "job_id": job.id,
            "status": job.status
        })

    # ✅ Otherwise check if application exists
    application = GigApplication.objects.filter(
        gig=gig,
        client=request.user.profile
    ).first()

    if application:
        return Response({
            "applied": True,
            "status": application.status,
            "application_id": application.id
        })
    else:
        return Response({"applied": False})
