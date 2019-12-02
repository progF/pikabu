from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import MainUser, Profile
from utils.file_upload import avatar_delete_path


@receiver(post_save, sender=MainUser, dispatch_uid="_uid")
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_delete, sender=Profile)
def delete_profile(sender,instance, **kwargs):
        if instance.avatar:
            avatar_delete_path(instance.avatar)
