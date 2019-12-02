from django.db.models.signals import pre_delete
from django.dispatch import receiver

from post.models import Post
from utils.file_upload import media_delete_path


@receiver(pre_delete, sender=Post)
def media_deleted(sender, instance, *args, **kwargs):
    media = instance.medias.first()
    if media:
        media_delete_path(media.file)
