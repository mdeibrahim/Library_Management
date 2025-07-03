
from django.db import models
from apps.member.models import Member

# models.py
class StripeCustomer(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.member.email
