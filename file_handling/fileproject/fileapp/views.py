from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Mobiles

# CREATE (POST)
@csrf_exempt
def create_mobile(request):
    if request.method == "POST":
        title = request.POST.get('title', '')
        brand = request.POST.get('brand', '')
        image = request.FILES.get('image')  # handle file upload

        if not image or not brand:
            return JsonResponse({"error": "Brand and image file are required"}, status=400)

        mobile = Mobiles.objects.create(title=title, brand=brand, image=image)
        return JsonResponse({
            "message": "Mobile created successfully!",
            "id": mobile.id,
            "image_url": mobile.image.url  # Cloudinary URL
        }, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# READ (GET all)
@csrf_exempt
def list_mobiles(request):
    if request.method == "GET":
        mobiles = Mobiles.objects.all()
        data = [
            {"id": m.id, "title": m.title, "brand": m.brand, "image_url": m.image.url}
            for m in mobiles
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# READ (GET one)
@csrf_exempt
def get_mobile(request, pk):
    if request.method == "GET":
        try:
            mobile = Mobiles.objects.get(pk=pk)
            data = {
                "id": mobile.id,
                "title": mobile.title,
                "brand": mobile.brand,
                "image_url": mobile.image.url
            }
            return JsonResponse(data)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Mobile not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# UPDATE (POST/PATCH)
@csrf_exempt
def update_mobile(request, pk):
    if request.method in ["POST", "PATCH"]:
        try:
            mobile = Mobiles.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Mobile not found"}, status=404)

        title = request.POST.get('title', mobile.title)
        brand = request.POST.get('brand', mobile.brand)
        image = request.FILES.get('image')

        mobile.title = title
        mobile.brand = brand
        if image:
            mobile.image = image
        mobile.save()

        return JsonResponse({"message": "Mobile updated successfully!", "image_url": mobile.image.url})

    return JsonResponse({"error": "Invalid request method"}, status=405)


# DELETE
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
