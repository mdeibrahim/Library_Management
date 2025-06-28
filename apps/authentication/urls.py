from django.urls import path
from apps.authentication.views import UserRegistrationView,OTPVerificationView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('otp-verify/', OTPVerificationView.as_view(), name='otp-verification'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLoginView.as_view(), name='user-logout'),
]