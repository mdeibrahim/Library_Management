from django.urls import path
from .views import AllProfilesView, home, ProfileView

urlpatterns = [
    path('', home, name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('all-profiles/', AllProfilesView.as_view(), name='all_profiles'),
]
