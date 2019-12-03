from rest_framework import serializers
from tag.models import Tag, PostTagMap
from users.serializers import MainUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
