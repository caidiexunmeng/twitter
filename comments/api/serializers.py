from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from comments.models import Comment
from tweets.models import Tweet
from accounts.api.serializers import UserSerializer
from likes.services import LikeService


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    likes_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'tweet_id', 'user', 'content', 'created_at', 'likes_count', 'has_liked',)

    def get_likes_count(self, obj):
        return obj.like_set.count()

    def get_has_liked(self, obj):
        return LikeService.has_liked(self.context['request'].user, obj)

class CommentSerializerForCreate(serializers.ModelSerializer):
    tweet_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ('content', 'tweet_id', 'user_id')

    def validate(self, attrs):
        tweet_id = attrs['tweet_id']
        if not Tweet.objects.filter(id=tweet_id).exists():
            raise ValidationError({
                'message': 'tweet does not exist'
            })
        return attrs

    def create(self, validated_data):
        comment = Comment.objects.create(
            user_id=validated_data['user_id'],
            tweet_id=validated_data['tweet_id'],
            content=validated_data['content'],
        )
        return comment

class CommentSerializerForUpdate(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content', )

    def update(self, instance, validated_data):
        instance.content = validated_data['content']
        instance.save()
        return instance