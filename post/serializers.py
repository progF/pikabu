from django.db import transaction
from rest_framework import serializers

from community.serializers import CommunitySerializer
from post.models import Post, PostMedia, Comment, SavedPost
from tag.models import PostTagMap, Tag
from tag.serializers import PostTagMapSerializer
from users.serializers import MainUserSerializer


class PostShortSerializer(serializers.ModelSerializer):
    creator = MainUserSerializer(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'creator', 'rating')

    def validate_title(self, value):
        if len(value) >= 100:
            raise serializers.ValidationError("Post length can't exceed 200 chars.")
        return value

    def get_rating(self, post):
        return post.ratings.count()


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ('file', )


class PostFullSerializer(PostShortSerializer):
    community_id = serializers.IntegerField(required=False, write_only=True)
    community = CommunitySerializer(read_only=True)
    documents_uploaded = serializers.ListField(child=serializers.FileField(), required=False, write_only=True)
    medias = PostMediaSerializer(read_only=True, many=True)
    tag_names = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    tags = PostTagMapSerializer(many=True, read_only=True)

    class Meta(PostShortSerializer.Meta):
        fields = PostShortSerializer.Meta.fields + ('text', 'documents_uploaded', 'medias', 'created_at', 'updated_at',
                                                    'community_id', 'community', 'tags', 'tag_names')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        with transaction.atomic():
            documents = []
            tag_names = []
            if 'documents_uploaded' in validated_data:
                documents = validated_data.pop('documents_uploaded')
            if 'tag_names' in validated_data:
                tag_names = validated_data.pop('tag_names')
            post = Post(**validated_data)
            post.save()
            PostMedia.objects.bulk_create([PostMedia(post=post, file=doc) for doc in documents])
            tags = []
            for tag in tag_names:
                try:
                    t = Tag.objects.get(name=tag)
                except Tag.DoesNotExist:
                    t = Tag.objects.create(name=tag)
                tags.append(t)
            PostTagMap.objects.bulk_create([PostTagMap(post=post, tag=tag) for tag in tags])
            return post


class PostFullSerializer2(PostFullSerializer):
    text = serializers.CharField(required=False)
    title = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        with transaction.atomic():
            documents = []
            tag_names = []
            if 'documents_uploaded' in validated_data:
                documents = validated_data.pop('documents_uploaded')
            if 'tag_names' in validated_data:
                tag_names = validated_data.pop('tag_names')
            instance.title = validated_data.get('title', instance.title)
            instance.text = validated_data.get('text', instance.text)
            instance.save()
            PostMedia.objects.bulk_create([PostMedia(post=instance, file=doc) for doc in documents])
            tags = []
            for tag in tag_names:
                try:
                    t = Tag.objects.get(name=tag)
                except Tag.DoesNotExist:
                    t = Tag.objects.create(name=tag)
                tags.append(t)
            PostTagMap.objects.bulk_create([PostTagMap(post=instance, tag=tag) for tag in tags])
            return instance


class SavedPostSerializer(serializers.ModelSerializer):
    post = PostFullSerializer()

    class Meta:
        model = SavedPost
        fields = ('post', )


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance

    def validate_text(self, value):
        if len(value) >= 200:
            raise serializers.ValidationError("Comment length can't exceed 200 chars.")
        return value


class CommentWithCreatorSerializer(CommentSerializer):
    creator = MainUserSerializer(read_only=True)


class CommentFullSerializer(CommentSerializer):
    post = PostShortSerializer(read_only=True)


class PostWithCommentsSerializer(PostFullSerializer):
    comments = CommentSerializer(many=True)

    class Meta(PostFullSerializer.Meta):
        fields = PostFullSerializer.Meta.fields + ('comments', )
