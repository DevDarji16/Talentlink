from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
# Create your views here.

@csrf_exempt
@api_view(['POST'])
def signup_redirect(request):
    role=request.data.get('role')
    request.session['role']=role
    return redirect('/authentication/accounts/google/login/')