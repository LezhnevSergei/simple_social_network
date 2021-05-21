from rest_framework import serializers

from posts.models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    count_likes = serializers.IntegerField(default=0)
    is_liked = serializers.BooleanField(default=False)

    class Meta:
        model = Post
        fields = ('id', 'creator_id', 'text', 'created_at', 'count_likes', 'is_liked')


class PostLikeSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField(default=False)

    class Meta:
        model = PostLike
        fields = ('creator_id', 'is_liked')
