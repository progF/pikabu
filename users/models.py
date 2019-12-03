from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from utils.file_upload import avatar_path
from utils.constants import (
    GENDER_TYPES,
    OTHER,
    COMMENT_SORT_TYPES,
    BY_TIME_ASC)
from utils.validators import comment_sort, profile_gender


class MainUser(AbstractUser):
    is_blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return '{}: {}'.format(self.id, self.username)


class ProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('user__username')

    def filter_by_gender(self, gender):
        return self.filter(gender=gender)

    def top_profiles(self):
        return super().get_queryset().order_by('rating')[:5]

    def get_moderators(self):
        return self.filter(user__is_staff=True)


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE, related_name='profile')
    gender = models.IntegerField(choices=GENDER_TYPES, default=OTHER, validators=[profile_gender])
    about = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to=avatar_path, default='default_avatar.png', blank=True, null=True,
                                      validators=[FileExtensionValidator(
                                                      allowed_extensions=[
                                                          'png',
                                                          'jpg',
                                                          'jpeg'])])
    background_image = models.ImageField(upload_to=avatar_path, blank=True, null=True,
                                         validators=[FileExtensionValidator(
                                                         allowed_extensions=[
                                                             'png',
                                                             'jpg',
                                                             'jpeg'])])
    rating = models.IntegerField(default=0)
    post_rating = models.IntegerField(default=0)
    comment_rating = models.IntegerField(default=0)
    comment_sorting = models.IntegerField(choices=COMMENT_SORT_TYPES, default=BY_TIME_ASC, validators=[comment_sort])

    objects = models.Manager()
    profiles = ProfileManager()


class UserRelation(models.Model):
    subscriber = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='my_subscriptions')
    subscribed_to = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='my_subscribers')
