from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.member.models import Member
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.member.serializers import BorrowBookSerializer, ReturnBookSerializer
from drf_yasg.utils import swagger_auto_schema

class BorrowBookView(APIView):
    """
    Allow authenticated members to borrow books from the library.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Borrow a book from the library",
        request_body=BorrowBookSerializer,
        responses={
            200: "Book borrowed successfully",
            400: "Invalid request data",
            401: "Authentication required"
        }
    )
    def post(self, request):
        """
        Borrow a book from the library.
        
        Members can borrow available books using this endpoint.
        """
        serializer = BorrowBookSerializer(data=request.data)
        if serializer.is_valid():
            # Logic for borrowing a book
            return Response({
                "success": True,
                "message": "Book borrowed successfully",
                "status code": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReturnBookView(APIView):
    """
    Allow authenticated members to return borrowed books to the library.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Return a borrowed book to the library",
        request_body=ReturnBookSerializer,
        responses={
            200: "Book returned successfully",
            400: "Invalid request data",
            401: "Authentication required"
        }
    )

    def post(self, request):
        """
        Return a borrowed book to the library.
        
        Members can return their borrowed books using this endpoint.
        """
        serializer = ReturnBookSerializer(data=request.data)
        if serializer.is_valid():
            # Logic for returning a book
            return Response({
                "success": True,
                "message": "Book returned successfully",
                "status code": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    """
    Render the home page template.
    """
    return render(request, 'index.html')

class ProfileView(APIView):
    """
    Retrieve the current user's profile information.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get current user profile information",
        responses={
            200: "Profile information retrieved successfully",
            401: "Authentication required"
        }
    )
    def get(self, request):
        """
        Get the authenticated user's profile information.
        
        Returns detailed profile data including personal information.
        """
        user = Member.objects.filter(email=request.user.email).first()

        return Response({
            "success": True,
            "message": "Profile data",
            "status code": status.HTTP_200_OK,
            "user_id": user.id,
            "user_email": user.email,
            "profile": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "bio": user.bio,
                "age": user.profile.age,
                "gender": user.profile.gender,
                "address": user.profile.address,
                "phone": user.profile.phone,
                "is_active": user.is_active
            },
            
        }, status=status.HTTP_200_OK)
        
        
class AllProfilesView(APIView):
    """
    Retrieve all user profiles (Admin only).
    """
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Get all user profiles (admin only)",
        responses={
            200: "All profiles retrieved successfully",
            403: "Admin access required"
        }
    )
    def get(self, request):
        """
        Get all user profiles in the system.
        
        Only accessible by admin users. Returns detailed information
        about all registered users.
        """
        users = Member.objects.all()
        user_data = []
        for user in users:
            user_data.append({
                "user_id": user.id,
                "user_email": user.email,
                "profile": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "bio": user.bio,
                    "age": user.profile.age,
                    "gender": user.profile.gender,
                    "address": user.profile.address,
                    "phone": user.profile.phone,
                    "is_active": user.is_active
                }
            })
        return Response({
            "success": True,
            "message": "All profiles data",
            "status code": status.HTTP_200_OK,
            "profiles": user_data
        }, status=status.HTTP_200_OK)


