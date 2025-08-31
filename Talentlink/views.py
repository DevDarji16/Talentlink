from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

def ping(request):
    return JsonResponse({'status':'ok'})

@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"detail": "CSRF cookie set"})