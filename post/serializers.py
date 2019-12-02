from rest_framework import serializers

from post.models import Post, PostMedia, Comment, SavedPost
from users.serializers import ProfileShortSerializer


class PostShortSerializer(serializers.ModelSerializer):
    creator = ProfileShortSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'rating', 'creator')

    def validate_title(self, value):
        if len(value) >= 100:
            raise serializers.ValidationError("Post length can't exceed 200 chars.")
        return value


class PostFullSerializer(PostShortSerializer):
    # community = CommunitySerizilaser(read_only=True)

    class Meta(PostShortSerializer.Meta):
        fields = PostShortSerializer.Meta.fields + ('text', 'medias', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = '__all__'


class SavedPostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SavedPost
        fields = '__all__'


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    rating = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    creator = ProfileShortSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField()

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.post_id = validated_data.get('post_id', instance.post_id)

        instance.save()
        return instance

    def validate_text(self, value):
        if len(value) >= 200:
            raise serializers.ValidationError("Comment length can't exceed 200 chars.")
        return value

