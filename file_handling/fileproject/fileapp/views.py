from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from cloudinary.uploader import upload
from .models import Mobiles


# -----------------------------------------------------
# USER REGISTER
# -----------------------------------------------------
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")

        if not username or not email or not password:
            return JsonResponse({"error": "All fields are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"message": "User registered successfully!", "username": user.username}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)



# -----------------------------------------------------
# USER LOGIN
# -----------------------------------------------------
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if not username or not password:
            return JsonResponse({"error": "Username and password are required"}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            return JsonResponse({"message": "Login successful!", "username": username})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Invalid request method"}, status=405)



# -----------------------------------------------------
# CREATE MOBILE
# -----------------------------------------------------
@csrf_exempt
def create_mobile(request):
    if request.method == "POST":
        title = request.POST.get('title', '')
        brand = request.POST.get('brand', '')
        image_file = request.FILES.get('image')

        if not image_file or not brand:
            return JsonResponse({"error": "Brand and image file are required"}, status=400)

        try:
            upload_result = upload(image_file)
            image_url = upload_result.get('secure_url')

            mobile = Mobiles.objects.create(title=title, brand=brand, image=image_url)

            return JsonResponse({
                "message": "Mobile created successfully!",
                "id": mobile.id,
                "title": mobile.title,
                "brand": mobile.brand,
                "image_url": image_url
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)



# -----------------------------------------------------
# LIST ALL MOBILES
# -----------------------------------------------------
@csrf_exempt
def list_mobiles(request):
    if request.method == "GET":
        mobiles = Mobiles.objects.all()
        data = [
            {
                "id": m.id,
                "title": m.title,
                "brand": m.brand,
                "image_url": m.image
            }
            for m in mobiles
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)



# -----------------------------------------------------
# GET SINGLE MOBILE
# -----------------------------------------------------
@csrf_exempt
def get_mobile(request, pk):
    if request.method == "GET":
        try:
            mobile = Mobiles.objects.get(pk=pk)
            return JsonResponse({
                "id": mobile.id,
                "title": mobile.title,
                "brand": mobile.brand,
                "image_url": mobile.image
            })
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Mobile not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)



# -----------------------------------------------------
# UPDATE MOBILE
# -----------------------------------------------------
@csrf_exempt
def update_mobile(request, pk):
    if request.method in ["POST", "PATCH"]:
        try:
            mobile = Mobiles.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Mobile not found"}, status=404)

        title = request.POST.get('title', mobile.title)
        brand = request.POST.get('brand', mobile.brand)
        image_file = request.FILES.get('image')

        try:
            if image_file:
                upload_result = upload(image_file)
                mobile.image = upload_result.get('secure_url')

            mobile.title = title
            mobile.brand = brand
            mobile.save()

            return JsonResponse({
                "message": "Mobile updated successfully!",
                "id": mobile.id,
                "title": mobile.title,
                "brand": mobile.brand,
                "image_url": mobile.image
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)



# -----------------------------------------------------
# DELETE MOBILE
# -----------------------------------------------------
@csrf_exempt
def delete_mobile(request, pk):
    if request.method == "DELETE":
        try:
            mobile = Mobiles.objects.get(pk=pk)
            mobile.delete()
            return JsonResponse({"message": "Mobile deleted successfully!"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Mobile not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)
