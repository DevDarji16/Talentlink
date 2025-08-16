from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Canvas
from .serializers import CanvasSerializer

@api_view(['GET'])
def list_canvases(request):
    canvases = request.user.canvas.all()
    serializer = CanvasSerializer(canvases, many=True)
    return Response({"canvases": serializer.data})

@api_view(['GET'])
def get_canvas(request, canvas_id):
    try:
        canvas = Canvas.objects.get(id=canvas_id, user=request.user)
        return Response({
            'id': canvas.id,
            'title': canvas.title,
            'data': canvas.data,
            'created_at': canvas.created_at
        })
    except Canvas.DoesNotExist:
        return Response({'error': 'Canvas not found'}, status=404)

@api_view(['POST'])
def create_canvas(request):
    new_canvas = Canvas.objects.create(
        user=request.user,
        title=request.data.get("title",'Untitled Canvas'),  
         
    )
    return Response({
        "id": new_canvas.id,
        "title": new_canvas.title
    })


@api_view(['PUT'])
def update_canvas(request, canvas_id):
    canvas = Canvas.objects.get(id=canvas_id, user=request.user)
    if 'title' in request.data:
        canvas.title = request.data['title']
    if 'data' in request.data:
        canvas.data = request.data['data']
    
    canvas.save()
    return Response({
        'status': 'success',
    })

@api_view(['DELETE'])
def delete_canvas(request, canvas_id):
    try:
        canvas = Canvas.objects.get(id=canvas_id, user=request.user)
    except Canvas.DoesNotExist:
        return Response({"error": "Canvas not found"})

    canvas.delete()
    return Response({"success": True, "message": "Canvas deleted successfully"})