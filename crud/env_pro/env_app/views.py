from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Student
import bcrypt
import json
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return JsonResponse({"message": "Hello! This is the home page."})


@csrf_exempt
def create_student(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            name = data.get('name')
            email = data.get('email')
            age = data.get('age')
            course = data.get('course')

            # ✅ Print incoming values (same as your example)
            print("Received name:", name)
            print("Received email:", email)

            if not name or not email:
                return JsonResponse({"error": "Name and email are required."}, status=400)

            # ✅ MANUAL HASHING using bcrypt (same style as your password hashing)
            hashed_email = bcrypt.hashpw(email.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')

            # ✅ Save to database
            student = Student(
                name=name,
                email=hashed_email,   # store hashed email
                age=age,
                course=course
            )
            student.save()

            return JsonResponse({"message": "Student created successfully with hashed email!"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)

    return JsonResponse({"error": "POST request required."}, status=405)

@csrf_exempt
# def read_students(request):
#     students = list(Student.objects.values())
#     return HttpResponse(json.dumps(students), content_type="application/json")
def read_students(request):
    students = list(Student.objects.values('id', 'name', 'age', 'course'))
    return JsonResponse(students, safe=False)

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
