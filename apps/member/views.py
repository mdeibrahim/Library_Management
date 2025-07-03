from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.member.models import Member
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
def home(request):
    return render(request, 'index.html')

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):

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
    permission_classes = [IsAdminUser]

    def get(self, request):
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
