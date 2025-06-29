from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile
# Create your views here.



@api_view(['GET'])
def check_user(request):
    exists=UserProfile.objects.filter(user=request.user).exists()
    return Response({'exists':exists})