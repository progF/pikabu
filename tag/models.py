from django.db import models
from django.db.models import Count

from post.models import Post
from users.models import MainUser
from utils.validators import validate_tag


class TagManager(models.Manager):
    def find_by_name(self, value):
        return self.filter(name__iexact=value)

    def contains(self, value):
        return self.filter(name__contains=value)

    def order_by_name(self):
        return self.order_by('name')

    def popular_tags(self):
        return self.annotate(rating=Count('posts'))[:11]


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True, validators=[validate_tag])
    subscribed_users = models.ManyToManyField(MainUser, related_name='subscribed_tags', blank=True)


class PostTagMap(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tags')
