from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Documents


# CREATE (POST)
@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        title = request.POST.get('title', '')

        if not file:
            return JsonResponse({"error": "No file provided"}, status=400)

        document = Documents.objects.create(title=title, file=file)
        return JsonResponse({"message": "File uploaded successfully!", "id": document.id}, status=201)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


# READ (GET all)
@csrf_exempt
def list_files(request):
    if request.method == "GET":
        files = Documents.objects.all().values('id', 'title', 'file')
        return JsonResponse(list(files), safe=False)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


# READ (GET one)
@csrf_exempt
def get_file(request, pk):
    if request.method == "GET":
        try:
            file = Documents.objects.get(pk=pk)
            data = {"id": file.id, "title": file.title, "file": file.file.url}
            return JsonResponse(data)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "File not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# UPDATE (PATCH/POST)
@csrf_exempt
def update_file(request, pk):
    if request.method in ["POST", "PATCH"]:
        try:
            file = Documents.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "File not found"}, status=404)

        title = request.POST.get('title', file.title)
        new_file = request.FILES.get('file')

        if new_file:
            file.file = new_file
        file.title = title
        file.save()

        return JsonResponse({"message": "File updated successfully!"})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


# DELETE
@csrf_exempt
def delete_file(request, pk):
    if request.method == "DELETE":
        try:
            file = Documents.objects.get(pk=pk)
            file.delete()
            return JsonResponse({"message": "File deleted successfully!"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "File not found"}, status=404)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)
