from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TalentLinkReview
from .serializers import TalentLinkReviewSerializer

# Add a review
@api_view(['POST'])
def add_review(request):
    name = request.data.get('name')
    comment = request.data.get('comment')

    if not name or not comment:
        return Response({"detail": "Name and comment are required"}, status=status.HTTP_400_BAD_REQUEST)

    review = TalentLinkReview.objects.create(name=name, comment=comment)
    serializer = TalentLinkReviewSerializer(review)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# Get latest 4 reviews
@api_view(['GET'])
def get_reviews(request):
    reviews = TalentLinkReview.objects.order_by('-created_at')[:4]
    serializer = TalentLinkReviewSerializer(reviews, many=True)
    return Response(serializer.data)
