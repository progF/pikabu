from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, UserManager
from utils.constants import GENDER_TYPES, OTHER

class MainUserManager(UserManager):
    def _create_user(self, username ,email, password, **extra_fields):
        if not username or not email:
            raise ValueError('The given username and email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, username, email,  password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)


    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class MainUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_staff =  models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MainUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class ProfileManager(models.Manager):
    def create(self, user):
        profile = self.model(user=user)
        profile.save()


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    about = models.TextField(max_length=1000, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPES, default=OTHER)
    background_image = models.ImageField(upload_to='background_images/', blank=True)
    raiting = models.IntegerField(default=0)
    is_administrator = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    objects = ProfileManager()
