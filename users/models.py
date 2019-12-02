from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from utils.file_upload import avatar_path
from utils.constants import (
    GENDER_TYPES,
    OTHER,
    COMMENT_SORT_TYPES,
    BY_RATING
)


class MainUser(AbstractUser):
    is_blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return '{}: {}'.format(self.id,self.username)


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE, related_name='profile')
    gender = models.IntegerField(choices=GENDER_TYPES, default=OTHER)
    about = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to=avatar_path, blank=True, null=True, validators=[
                                             FileExtensionValidator(
                                                 allowed_extensions=[
                                                     'png',
                                                     'jpg', 'jpeg'])])
    background_image = models.ImageField(upload_to=avatar_path, blank=True, null=True, validators=[
                                             FileExtensionValidator(
                                                 allowed_extensions=[
                                                     'png',
                                                     'jpg', 'jpeg'])])
    rating = models.IntegerField(default=0)
    post_rating = models.IntegerField(default=0)
    comment_rating = models.IntegerField(default=0)
    comment_sorting = models.IntegerField(choices=COMMENT_SORT_TYPES, default=BY_RATING)
