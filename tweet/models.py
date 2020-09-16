from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField(max_length=1000, blank=True, null=True)
    retweet = models.ForeignKey("Tweet", blank=True, null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username + "'s Tweet " + str(self.id)

    @property
    def author_name(self):
        return self.author.username

    @property
    def tweet_like_total(self):
        return self.tweetlike_set.all().filter(state=True).count()

    @property
    def tweet_rt_total(self):
        return self.tweet_set.all().filter(retweet=self.id).count()

    @property
    def retweet_author_id(self):
        return self.retweet.author.id

    @property
    def retweet_author_name(self):
        return self.retweet.author.username

    @property
    def retweet_content(self):
        return self.retweet.content

    @property
    def retweet_like_total(self):
        return self.retweet.tweetlike_set.all().filter(state=True).count()

    @property
    def retweet_rt_total(self):
        return self.retweet.tweet_set.all().filter(retweet=self.retweet.id).count()


class TweetLike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)

    @property
    def author_name(self):
        return self.author.username


class FollowUser(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")


class TweetComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def author_name(self):
        return self.author.username




