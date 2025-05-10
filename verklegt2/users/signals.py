# users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, BuyerProfile, SellerProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    After each new User is saved, auto-create exactly one
    BuyerProfile or SellerProfile, based on user_type.
    """
    if not created:
        return

    if instance.user_type == User.BUYER:
        BuyerProfile.objects.create(user=instance)
    else:
        SellerProfile.objects.create(user=instance)