from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.response import Response
from apps.authentication.serializers import MemberRegistrationSerializer
from apps.member.models import Member
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserRegistrationView(APIView):
    serializer_class = MemberRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "success": True,
                "message": "User registered successfully.",
                "status code": status.HTTP_201_CREATED,
                "id": user.id,
                "user": MemberRegistrationSerializer(user).data,
                "user status": user.is_active, 
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": serializer.errors,
            "status code": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)
        


class OTPVerificationView(APIView):

    def post(self, request):
        email = request.data.get('email')
        submitted_otp = request.data.get('otp')  # get the OTP submitted by user
        print(email, submitted_otp)

        member = Member.objects.filter(email=email).first()

        if not member:
            return Response({
                "success": False,
                "message": "Member with this email does not exist.",
                "status code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)


        if member.otp != str(submitted_otp):
            print("Stored OTP:", member.otp, "| Submitted OTP:", submitted_otp)
            return Response({
                "success": False,
                "message": "Invalid OTP.",
                "status code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        member.otp_verified = True
        member.is_active = True
        member.save()

        return Response({
            "success": True,
            "message": "OTP verified successfully.",
            "status code": status.HTTP_200_OK,
            "id": member.id,
            "status": member.is_active,
            "user": {
                "id": member.id,
                "email": member.email,
                "name": member.profile.name,
                "is_active": member.is_active
            }
        }, status=status.HTTP_200_OK)
        
        
class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                "success": False,
                "message": "Email and password are required.",
                "status code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        user = Member.objects.filter(email=email).first()

        if not user:
            return Response({
                "success": False,
                "message": "User with this email does not exist.",
                "status code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({
                "success": False,
                "message": "Incorrect password.",
                "status code": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "success": True,
            "message": "Login successful.",
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
            "access_token": str(RefreshToken.for_user(user).access_token),
            "refresh_token": str(RefreshToken.for_user(user))
        }, status=status.HTTP_200_OK)
        
        
class UserLogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            tocken = RefreshToken(refresh_token)
            tocken.blacklist()  

            # Blacklist the refresh token
            return Response({
                "success": True,
                "message": "User logged out successfully.",
                "status code": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except KeyError:
            return Response({
                "success": False,
                "message": "Refresh token not provided.",
                "status code": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        