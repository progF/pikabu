from rest_framework import serializers
from tag.models import Tag, PostTagMap


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PostTagMapSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = PostTagMap
        fields = ('tag', )
