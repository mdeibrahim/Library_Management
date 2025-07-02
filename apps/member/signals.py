from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member, Profile

@receiver(post_save, sender=Member)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            member=instance,
            name=f"{instance.first_name} {instance.last_name}".strip() or "No Name",
            age=0,  # default age
            gender='other',  # default gender
            address='',
            phone=''
        )