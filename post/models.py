from django.db import models
from django.db.models import Count
from django.utils.datetime_safe import datetime

from community.models import Community
from users.models import MainUser
from utils.file_upload import post_media_path


class Publishable(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PostManager(models.Manager):
    def search_by_title(self, value):
        return self.filter(title__contains=value)

    def get_posts_by_date(self, value):
        date = datetime.strptime(value, "%d-%m-%Y")  # 18-02-1999
        return self.filter(created_at__day=date.day,
                           created_at__month=date.month,
                           created_at__year=date.year)

    def order_by_date(self, desc):
        field = 'created_at'
        if desc:
            field = '-{}'.format(field)
        return self.all().order_by(field)

    def sort_by_field(self, value):
        date = datetime.now()
        posts = self.all().filter(created_at__day=date.day,
                                  created_at__month=date.month,
                                  created_at__year=date.year)
        if value == 'rating':
            posts = posts.annotate(rating=Count('ratings'))

        return posts.order_by('-%s' % value)


class Post(Publishable):
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='posts')
    community = models.ForeignKey(Community, null=True, on_delete=models.SET_NULL, related_name='posts')

    objects = models.Manager()
    posts = PostManager()


class PostRating(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='rated')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')


class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='medias')
    file = models.FileField(upload_to=post_media_path, null=True)


class SavedPost(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved')

    def __str__(self):
        return '{} saved postId {}.'.format(self.user.username, self.post.id)


class Comment(Publishable):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='comments')
