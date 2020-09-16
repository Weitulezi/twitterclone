from django.shortcuts import render, Http404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

from .models import Tweet, TweetLike, FollowUser, TweetComment
from .forms import TweetForm


@login_required
def home_view(request):
    form = TweetForm()
    context = {"form": form}
    if request.method == "POST":
        form = TweetForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
            form = TweetForm()
    return render(request, 'tweet/home.html', context)


@login_required
def tweet_detail(request, tweet_author, pk):
    userTweets = Tweet.objects.all().filter(author=request.user)
    try:
        author = User.objects.get(username=tweet_author)
        tweet = Tweet.objects.get(pk=pk, author=author)
    except:
        raise Http404
    try:
        userLike = TweetLike.objects.get(author=request.user, tweet=tweet)
        likeState = userLike.state
    except:
        likeState = False
    print(likeState)
    rtState = False
    for item in userTweets:
        if tweet == item.retweet:
            rtState = True
    context = {'tweet': tweet, "rtState": rtState, "likeState": likeState}
    return render(request, 'tweet/tweet_detail.html', context)
    

def handle_like(request):
    data = json.loads(request.body)
    tweet = Tweet.objects.get(pk=data['tweetId'])
    try:
        like = TweetLike.objects.get(author=request.user, tweet=tweet)
    except:
        like = TweetLike.objects.create(author=request.user, tweet=tweet,)
    if like.state == False:
        like.state = True
        like.save()
    else:
        like.state = False
        like.save()
    likeTotal = tweet.tweetlike_set.all().filter(state=True).count()
    data = {
        'likeTotal': likeTotal,
        'state': like.state
    }
    return JsonResponse(data, safe=False)


def handle_retweet_no_comment(request):
    data = json.loads(request.body)
    userId = data["userId"]
    tweetId = data["tweetId"]
    user = User.objects.get(pk=userId)
    if user == request.user:
        getTweet = Tweet.objects.get(pk=tweetId)
        try:
            new_tweet = Tweet.objects.get(author=user, retweet=getTweet)     
        except:       
            new_tweet = Tweet.objects.create(author=user, retweet=getTweet)
            new_tweet.save()
        data = {
            "tweet_rt_total": getTweet.tweet_rt_total
        }
    return JsonResponse(data)
    

def handle_retweet_with_comment(request):
    data = json.loads(request.body)
    userId = data["userId"]
    tweetId = data["tweetId"]
    tweetContent = data["tweetContent"]
    user = User.objects.get(pk=userId)
    if user == request.user:
        tweet_to_be_retweeted = Tweet.objects.get(pk=tweetId)
        try:
            new_tweet = Tweet.objects.get(author=user, content=tweetContent, retweet=tweet_to_be_retweeted)
        except:
            new_tweet = Tweet.objects.create(author=user, content=tweetContent, retweet=tweet_to_be_retweeted)
            new_tweet.save()
        data = {"tweet_rt_total": tweet_to_be_retweeted.tweet_rt_total}
    else:
        data = {"message": "faiiled"}
    return JsonResponse(data)


def handle_change_retweet_comment(request):
    msg_response = ""
    data = json.loads(request.body)
    userId = data["userId"]
    tweetId = data["tweetId"]
    tweetContent = data["tweetContent"]
    user = User.objects.get(pk=userId)
    if request.user == user:
        tweet = Tweet.objects.get(pk=tweetId)
        if tweet.author == user:
            tweet.content = tweetContent
            tweet.save()
            msg_response = "tweet content changed successfully"
        else:
            tweet_to_be_retweeted = Tweet.objects.get(pk=tweetId)
            try:
                tweet = Tweet.objects.get(author=user, retweet=tweet_to_be_retweeted.id)
                tweet.content = tweetContent
                tweet.save()
                data = {"tweet_rt_total": tweet_to_be_retweeted.tweet_rt_total}
            except:
                print("something went wrong")
    return JsonResponse(data, safe=False)


def handle_unretweet(request):
    data = json.loads(request.body)
    userId = data["userId"]
    tweetId = data["tweetId"]
    user = User.objects.get(pk=userId)
    tweet = Tweet.objects.get(pk=tweetId)
    if tweet.author == user and tweet.content != None:
        tweet.delete()
        data = {"tweet_rt_total": 0}
    else:
        tweet_to_delete = Tweet.objects.get(author=user, retweet=tweet)
        tweet_to_delete.delete()
        data = {"tweet_rt_total": tweet.tweet_rt_total}
    return JsonResponse(data, safe=False)


def handle_comment(request):
    msg_response = "failed"
    data = json.loads(request.body)
    print(data)
    userId = data["userId"]
    tweetId = data["tweetId"]
    commentContent = data["commentContent"]
    user = User.objects.get(pk=userId)
    if user == request.user:
        tweet = Tweet.objects.get(pk=tweetId)
        try:
            new_comment = TweetComment.objects.get(author=user, tweet=tweet, content=commentContent)
        except:
            new_comment = TweetComment.objects.create(author=user, tweet=tweet, content=commentContent)
            new_comment.save()
        msg_response = "comment successfully created"
    return JsonResponse(msg_response, safe=False)


def delete_comment(request):
    data = json.loads(request.body)
    userId = data["userId"]
    commentId = data["commentId"]
    user = User.objects.get(pk=userId)
    if request.user == user:
        comment = TweetComment.objects.get(pk=commentId, author=user)
        comment.delete()
    return JsonResponse(data="comment Deleted", safe=False)


