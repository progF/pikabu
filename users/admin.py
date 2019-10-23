from django.contrib import admin
from users.models import MainUser, Profile

admin.site.register(MainUser)
admin.site.register(Profile)