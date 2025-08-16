from django.urls import path
from . import views

urlpatterns = [
    path('canvases/', views.list_canvases), 
    path('canvas/create/', views.create_canvas),
    path('canvas/<int:canvas_id>/', views.get_canvas),  
    path('canvas/<int:canvas_id>/update/', views.update_canvas),  
    path('canvas/<int:canvas_id>/delete/', views.delete_canvas),
]