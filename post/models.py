from django.contrib.auth.models import User
from django.db import models


class Publishable(models.Model):
    rating = models.IntegerField(default=0)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        abstract = True


class Post(Publishable):
    title = models.CharField(max_length=100)
    # community = models.ForeignKey(Community, on_delete=models.SET_NULL, related_name='posts')


class Comment(Publishable):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')