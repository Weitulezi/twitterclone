from django.shortcuts import render, Http404
from django.contrib.auth.models import User


def profile_view(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404
    context = {"user": user}
    return render(request, "user/profile.html", context)
