from django.urls import path
from .views import AllProfilesView, home
from apps.member.views import BorrowBookView, ReturnBookView

urlpatterns = [
    path('', home, name='home'),
    path('all-profiles/', AllProfilesView.as_view(), name='all_profiles'),
    path('borrow/', BorrowBookView.as_view(), name='borrow'),
    path('return/', ReturnBookView.as_view(), name='return'),
]

