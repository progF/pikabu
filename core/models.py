from django.db import models
from users.models import MainUser



class Community(models.Model):
    administrator = models.ForeignKey(MainUser, on_delete=models.SET_NULL, related_name='communities' , null=True)
    name = models.CharField(max_length=30)
    community_image = models.ImageField(upload_to='community_images')
    background_image = models.ImageField(upload_to='community_background_images')
    about = models.TextField()
    users = models.ManyToManyField(MainUser, related_name='user_communities')


class Tag(models.Model):
    name = models.CharField(max_length=20)
    users = models.ManyToManyField(MainUser, related_name='tags')


class Post(models.Model):
    author = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    post_rating = models.IntegerField(default=0)
    title = models.CharField(max_length=300)
    text = models.TextField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')


class PostMedia(models.Model):
    media = models.FileField(upload_to='postmedia')
    post = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='files')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='user_comments')
    rating = models.IntegerField(default=0)
    body = models.TextField(max_length=1000)
    




