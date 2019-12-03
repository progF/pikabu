from django.db import models
from users.models import MainUser
from utils.file_upload import community_path
from django.core.validators import FileExtensionValidator


class Community(models.Model):
    creator = models.ForeignKey(MainUser, on_delete=models.SET_NULL, related_name='communities', null=True)
    name = models.CharField(max_length=20, unique=True)
    about = models.TextField(max_length=500, blank=True)
    community_image = models.ImageField(upload_to=community_path, blank=True, null=True, validators=[
                                             FileExtensionValidator(
                                                 allowed_extensions=[
                                                     'png',
                                                     'jpg', 'jpeg'])])
    background_image = models.ImageField(upload_to=community_path, blank=True, null=True, validators=[
                                             FileExtensionValidator(
                                                 allowed_extensions=[
                                                     'png',
                                                     'jpg', 'jpeg'])])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Community"
        verbose_name_plural = "Communities"


class CommunityMember(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='my_communities')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='my_users')
