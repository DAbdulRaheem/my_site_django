from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 👈 This handles the root URL
    path('students/', views.read_students),
    path('students/create/', views.create_student),
    path('students/update/<int:id>/', views.update_student),
    path('students/delete/<int:id>/', views.delete_student),
]

