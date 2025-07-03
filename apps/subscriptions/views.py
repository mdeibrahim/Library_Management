# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import StripeCustomer
import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Check if stripe customer exists, if not create
        stripe_customer, created = StripeCustomer.objects.get_or_create(member=user)
        if created or not stripe_customer.stripeCustomerId:
            customer = stripe.Customer.create(email=user.email)
            stripe_customer.stripeCustomerId = customer['id']
            stripe_customer.save()

        session = stripe.checkout.Session.create(
            customer=stripe_customer.stripeCustomerId,
            client_reference_id=user.id,
            success_url='http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8000/cancel/',
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': settings.STRIPE_PRICE_ID,
                'quantity': 1,
            }],
        )
        return Response({'sessionId': session.id, 'checkout_url': session.url})


@csrf_exempt
def stripe_webhook(request):
    try:
        event = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON", status=400)

    if event.get('type') == 'checkout.session.completed':
        session = event['data']['object']
        customer_id = session.get('customer')
        subscription_id = session.get('subscription')

        from .models import StripeCustomer
        stripe_customer = StripeCustomer.objects.filter(stripeCustomerId=customer_id).first()
        if stripe_customer:
            stripe_customer.stripeSubscriptionId = subscription_id
            stripe_customer.save()

    return HttpResponse("Webhook received", status=200)


