from django.shortcuts import get_object_or_404
from apps.member.models import Book
from .serializers import AddBookSerializer, EditBookSerializer

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.member.permissions import IsLibrarian
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class AddBookView(generics.CreateAPIView):
    permission_classes = [IsLibrarian, IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = AddBookSerializer

    @swagger_auto_schema(
        operation_description="Add a new book or increase quantity of existing book",
        responses={
            201: "Book successfully created",
            200: "Book quantity increased",
            400: "Bad request - invalid data",
            403: "Permission denied - librarian access required"
        }
    )
    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        author = request.data.get('author')
        
        book = Book.objects.filter(title=title, author=author).first()
        if book:
            book.quantity += 1
            book.save()
            serializer = self.get_serializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@swagger_auto_schema(
    method='put',
    operation_description="Update book information (full update)",
    responses={200: "Book successfully updated", 400: "Invalid data", 403: "Permission denied", 404: "Book not found"}
)
@swagger_auto_schema(
    method='patch',
    operation_description="Partially update book information",
    responses={200: "Book successfully updated", 400: "Invalid data", 403: "Permission denied", 404: "Book not found"}
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsLibrarian, IsAdminUser])
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    serializer = EditBookSerializer(book, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_description="Retrieve detailed information about a specific book",
    responses={200: "Book details retrieved successfully", 404: "Book not found"}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    serializer = AddBookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='delete',
    operation_description="Delete a book from the library system",
    responses={204: "Book successfully deleted", 403: "Permission denied", 404: "Book not found"}
)
@api_view(['DELETE'])
@permission_classes([IsLibrarian, IsAdminUser])
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
