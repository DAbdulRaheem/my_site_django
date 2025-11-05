from django.urls import path
from . import views

urlpatterns = [
    path('mobiles/create/', views.create_mobile, name='create_mobile'),
    path('mobiles/', views.list_mobiles, name='list_mobiles'),
    path('mobiles/<int:pk>/', views.get_mobile, name='get_mobile'),
    path('mobiles/<int:pk>/update/', views.update_mobile, name='update_mobile'),
    path('mobiles/<int:pk>/delete/', views.delete_mobile, name='delete_mobile'),
]
