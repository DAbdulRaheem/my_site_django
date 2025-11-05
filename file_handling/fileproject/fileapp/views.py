from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from cloudinary.uploader import upload
from .models import Mobiles

# CREATE (POST)
@csrf_exempt
def create_mobile(request):
    if request.method == "POST":
        title = request.POST.get('title', '')
        brand = request.POST.get('brand', '')
        image_file = request.FILES.get('image')  

        if not image_file or not brand:
            return JsonResponse({"error": "Brand and image file are required"}, status=400)

        try:
            # Upload image to Cloudinary
            upload_result = upload(image_file)
            image_url = upload_result.get('secure_url')

            # Save in database
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


# READ (GET all)
@csrf_exempt
def list_mobiles(request):
    if request.method == "GET":
        mobiles = Mobiles.objects.all()
        data = [
            {
                "id": m.id,
                "title": m.title,
                "brand": m.brand,
                "image_url": m.image  # stored Cloudinary URL
            }
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
                "image_url": mobile.image
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
        image_file = request.FILES.get('image')

        try:
            if image_file:
                # Upload new image to Cloudinary
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
