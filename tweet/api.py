from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import Tweet, TweetLike, FollowUser, TweetComment
from .serializer import TweetSerializer, TweetLikeSerializer, TweetCommentSerializer


class TweetList(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            tweets = Tweet.objects.all().order_by('-id')
            user = User.objects.get(pk=request.user.pk)
            followed = FollowUser.objects.all().filter(follower=user)
            followed_username = []
            for eachuser in followed:
                if eachuser.follower == user:
                    followed_username.append(eachuser.followed.username)
            filter_tweet = []
            for tweet in tweets:
                for i in range(len(followed_username)):
                    if tweet.author.username == followed_username[i]:
                        filter_tweet.append(tweet)
            serializer = TweetSerializer(filter_tweet, many=True)
            return Response(serializer.data)
        else:
            raise Http404
        

class TweetLikeList(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            like = TweetLike.objects.all().order_by('-id')
            serializer = TweetLikeSerializer(like, many=True)
            return Response(serializer.data)
        else:
            raise Http404


class UserTweetList(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            userTweets = Tweet.objects.all().filter(author=request.user)
            serializer = TweetSerializer(userTweets, many=True)
            return Response(serializer.data)
        else:
            raise Http404


# Filtering comments of tweet, which the author follow by log in user
class TweetCommentList(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            comments = TweetComment.objects.all()
            user = User.objects.get(pk=request.user.pk)
            followed = FollowUser.objects.all().filter(follower=user)
            followed_username = []
            for eachuser in followed:
                if eachuser.follower == user:
                    followed_username.append(eachuser.followed.username)
            filter_comment = []
            for i in range(len(comments)):
                for j in range(len(followed_username)):
                    if comments[i].author.username == followed_username[j]:
                        filter_comment.append(comments[i])
            serializer = TweetCommentSerializer(filter_comment, many=True)
            return Response(serializer.data)


# List of comment from single Tweet
class SingleTweetComment(APIView):
    def get(self, request, tweetId, format=None):
        if request.user.is_authenticated:
            tweet = Tweet.objects.get(pk=tweetId)
            tweet_comments = TweetComment.objects.all().filter(tweet=tweet)
            serializer = TweetCommentSerializer(tweet_comments, many=True)
            return Response(serializer.data)
        
    



















