from django.urls import path
from . import views

urlpatterns = [
    path('subscriptions/', views.home, name='subscriptions'),
]