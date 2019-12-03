from django.db import models
from users.models import MainUser

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    subscribed_users = models.ManyToManyField( MainUser, related_name='tags', blank=True)


class PostTagMap(models.Model):
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE, related_name='tag_users')
    user = models.ForeignKey(MainUser,on_delete=models.CASCADE, related_name='user_tags')
