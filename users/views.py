from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@csrf_exempt
@api_view(['POST'])
def signup_redirect(request):
    role=request.data.get('role')
    request.session['role']=role
    return Response({'url':'https://talentlink-nloa.onrender.com/authentication/accounts/google/login/'})