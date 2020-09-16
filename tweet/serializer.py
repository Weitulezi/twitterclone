from rest_framework import serializers

from .models import Tweet, TweetLike, TweetComment

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = [
            "id",
            "author", 
            "author_name", 
            "content", 
            "tweet_like_total",
            "tweet_rt_total",
            "retweet", 
            "retweet_author_id", 
            "retweet_author_name", 
            "retweet_content",
            "retweet_like_total",
            "retweet_rt_total",
            "created_on",
        ]


class TweetLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetLike
        fields = ['author', 'author_name', 'tweet', 'state']


class TweetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetComment
        fields = ["id", 'author', 'author_name', 'tweet', 'content', 'created_on']