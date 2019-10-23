import os
from users.models import MainUser, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=MainUser, dispatch_uid='_profile')
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(instance)
