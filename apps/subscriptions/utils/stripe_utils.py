# utils/stripe_utils.py
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_customer(member):
    customer = stripe.Customer.create(
        email=member.email,
        name=f"{member.first_name} {member.last_name}"
    )
    return customer
