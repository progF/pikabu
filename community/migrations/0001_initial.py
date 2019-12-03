# Generated by Django 2.2.7 on 2019-12-02 18:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utils.file_upload


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('about', models.TextField(blank=True, max_length=500)),
                ('community_image', models.ImageField(blank=True, null=True, upload_to=utils.file_upload.community_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])),
                ('background_image', models.ImageField(blank=True, null=True, upload_to=utils.file_upload.community_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Community',
                'verbose_name_plural': 'Communities',
            },
        ),
        migrations.CreateModel(
            name='CommunityMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_users', to='community.Community')),
            ],
        ),
    ]
