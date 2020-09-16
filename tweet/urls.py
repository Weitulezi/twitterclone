from django.urls import path

from . import views
from . import api

urlpatterns = [
    path('home/', views.home_view, name="home"),
    path('home/<str:tweet_author>/<int:pk>/', views.tweet_detail, name="tweet_detail"),

    path('handle_like/', views.handle_like, name='handle_like'),
    path('handle_retweet_no_comment/', views.handle_retweet_no_comment, name='handle_retweet_no_comment'),
    path('handle_retweet_with_comment/', views.handle_retweet_with_comment, name='handle_retweet_with_comment'),
    path('handle_change_retweet_comment/', views.handle_change_retweet_comment, name='handle_change_retweet_comment'),
    path('handle_unretweet/', views.handle_unretweet, name='handle_unretweet'),
    path('handle_comment/', views.handle_comment, name='handle_comment'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),

    # API
    path('api/tweet_list/', api.TweetList.as_view(), name="tweet_list_api"),
    path('api/tweet_like_list/', api.TweetLikeList.as_view(), name="tweet_like_list"),
    path('api/user_tweet_list/', api.UserTweetList.as_view(), name="tweet_likeuser_tweet_list_list"),
    path('api/tweet_comment/', api.TweetCommentList.as_view(), name="TweetCommentList"),
    path('api/tweet_comment/<int:tweetId>/', api.SingleTweetComment.as_view(), name="SingleTweetComment"),
]