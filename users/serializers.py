from rest_framework.serializers import ModelSerializer
from users.models import MainUser, Profile
from rest_framework import serializers

class MainUserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = MainUser
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        user = MainUser.objects.create_user(**validated_data)
        return user

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_image','about','gender','background_image')
