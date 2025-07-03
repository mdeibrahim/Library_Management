from django.urls import path
from .views import CreateCheckoutSessionView
from .views import stripe_webhook

urlpatterns = [
    # path('subscriptions/', views.home, name='subscriptions'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]