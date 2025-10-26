from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer

# CREATE (POST)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):
    serializer = DocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "File uploaded successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# READ (GET all)
@api_view(['GET'])
def list_files(request):
    files = Document.objects.all()
    serializer = DocumentSerializer(files, many=True)
    return Response(serializer.data)

# READ (GET one)
@api_view(['GET'])
def get_file(request, pk):
    try:
        file = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = DocumentSerializer(file)
    return Response(serializer.data)

# UPDATE (PATCH)
@api_view(['PATCH'])
@parser_classes([MultiPartParser, FormParser])
def update_file(request, pk):
    try:
        file = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = DocumentSerializer(file, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "File updated successfully!"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE
@api_view(['DELETE'])
def delete_file(request, pk):
    try:
        file = Document.objects.get(pk=pk)
        file.delete()
        return Response({"message": "File deleted successfully!"})
    except Document.DoesNotExist:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
