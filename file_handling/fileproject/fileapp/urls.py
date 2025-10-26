from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.list_files, name='list_files'),
    path('files/<int:pk>/', views.get_file, name='get_file'),
    path('files/<int:pk>/update/', views.update_file, name='update_file'),
    path('files/<int:pk>/delete/', views.delete_file, name='delete_file'),
]
