from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from utils.file_upload import avatar_path


class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}: {self.username}'

    # def save(self, *args, **kwargs):
    #     self.username = self.username.lower()
    #     super(MainUser, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=300, blank=True)
    avatar = models.ImageField(upload_to=avatar_path, blank=True, null=True, validators=[
                                             FileExtensionValidator(
                                                 allowed_extensions=[
                                                     'png',
                                                     'jpg', 'jpeg'])])
    web_site = models.CharField(max_length=200, blank=True)