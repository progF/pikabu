from django.db.models.signals import pre_delete
from django.dispatch import receiver

from post.models import PostMedia
from utils.file_upload import media_delete_path


@receiver(pre_delete, sender=PostMedia)
def media_deleted(sender, instance, *args, **kwargs):
    if instance.file:
        media_delete_path(instance.file)