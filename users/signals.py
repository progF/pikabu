from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import MainUser, Profile
from utils.file_upload import media_delete_path


@receiver(post_save, sender=MainUser, dispatch_uid="_uid")
def create_profile(_, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_delete, sender=Profile)
def delete_profile(_, instance, **kwargs):
    if instance.profile_image:
        media_delete_path(instance.profile_image)
    if instance.background_image:
        media_delete_path(instance.background_image)
