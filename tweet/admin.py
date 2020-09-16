from django.contrib import admin

from .models import Tweet, TweetLike, FollowUser, TweetComment

admin.site.register(Tweet)
admin.site.register(TweetLike)
admin.site.register(FollowUser)
admin.site.register(TweetComment)
