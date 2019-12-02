from django.db.models.signals import post_delete
from django.dispatch import receiver
from community.models import Community
from utils.file_upload import media_delete_path


@receiver(post_delete, sender=Community)
def delete_community_image(sender, instance, **kwargs):
    if instance.community_image or instance.background_image:
        try:
            media_delete_path(instance.community_image)
        except Exception:
            media_delete_path(instance.background_image)
