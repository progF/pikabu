from django.db import models

from users.models import MainUser
from utils.file_upload import post_media_path


class Publishable(models.Model):
    rating = models.IntegerField(default=0)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(Publishable):
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='posts')
    # community = models.ForeignKey(Community, on_delete=models.SET_NULL, related_name='posts')


class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='medias')
    file = models.FileField(upload_to=post_media_path, null=True)


class SavedPost(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved')


class Comment(Publishable):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='comments')