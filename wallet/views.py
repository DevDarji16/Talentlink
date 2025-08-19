from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.models import UserProfile
from .models import WalletTransaction
from .serializers import WalletTransactionSerializer

# 👉 Add money to wallet
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_money(request):
    try:
        amount = request.data.get("amount")
        if not amount:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = request.user.profile
        user_profile.wallet_balance += amount
        user_profile.save()

        # record transaction
        tx = WalletTransaction.objects.create(
            user=user_profile,
            tx_type="credit",
            amount=amount,
            balance_after=user_profile.wallet_balance,
            reference="Wallet top-up"
        )

        return Response({
            "message": "Money added successfully",
            "balance": user_profile.wallet_balance,
            "transaction": WalletTransactionSerializer(tx).data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# 👉 Get wallet details (balance + transactions)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wallet_details(request):
    user_profile = request.user.profile
    transactions = WalletTransaction.objects.filter(user=user_profile).order_by("-created_at")
    serializer = WalletTransactionSerializer(transactions, many=True)
    
    return Response({
        "balance": user_profile.wallet_balance,
        "transactions": serializer.data
    })
