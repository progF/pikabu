from django.db import transaction
from rest_framework import serializers

from post.models import Post, PostMedia, Comment, SavedPost
from users.serializers import ProfileShortSerializer


class PostShortSerializer(serializers.ModelSerializer):
    creator = ProfileShortSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'creator')

    def validate_title(self, value):
        if len(value) >= 100:
            raise serializers.ValidationError("Post length can't exceed 200 chars.")
        return value


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ('file', )


class PostFullSerializer(PostShortSerializer):
    # community = CommunitySerizilaser(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    documents_uploaded = serializers.ListField(child=serializers.FileField(), required=False)
    medias = PostMediaSerializer(read_only=True, many=True)

    class Meta(PostShortSerializer.Meta):
        fields = PostShortSerializer.Meta.fields + ('text', 'documents_uploaded', 'medias', 'created_at', 'updated_at', 'rating')
        read_only_fields = ('created_at', 'updated_at')

    def get_rating(self, post):
        return post.ratings.count()

    def create(self, validated_data):
        with transaction.atomic():
            documents = []
            if 'documents_uploaded' in validated_data:
                documents = validated_data.pop('documents_uploaded')
            post = Post(**validated_data)
            post.save()
            for j in documents:
                post_document = PostMedia(post=post, file=j)
                post_document.save()
            return post


class SavedPostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SavedPost
        fields = '__all__'


class PostRatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SavedPost
        fields = '__all__'


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    creator_id = serializers.PrimaryKeyRelatedField(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.post_id = validated_data.get('post_id', instance.post_id)
        instance.post_id = validated_data.get('user_id', instance.user_id)
        instance.save()
        return instance

    def validate_text(self, value):
        if len(value) >= 200:
            raise serializers.ValidationError("Comment length can't exceed 200 chars.")
        return value

