from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_student(request):
    if request.method == "POST":
        data = json.loads(request.body)
        Student.objects.create(
            name=data['name'],
            email=data['email'],
            age=data['age'],
            course=data['course']
        )
        return HttpResponse("Student created successfully!")

@csrf_exempt
def read_students(request):
    students = list(Student.objects.values())
    return HttpResponse(json.dumps(students), content_type="application/json")

@csrf_exempt
def update_student(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        student = Student.objects.get(id=id)
        student.name = data.get('name', student.name)
        student.email = data.get('email', student.email)
        student.age = data.get('age', student.age)
        student.course = data.get('course', student.course)
        student.save()
        return HttpResponse("Student updated successfully!")

@csrf_exempt
def delete_student(request, id):
    if request.method == "DELETE":
        student = Student.objects.get(id=id)
        student.delete()
        return HttpResponse("Student deleted successfully!")
