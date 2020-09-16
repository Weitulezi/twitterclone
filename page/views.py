from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from tweet.models import FollowUser
from .forms import LoginForm, CreateUserForm

def index(request):
    context = {}
    return render(request, "landing_page.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                print("user is authenticated")
                user = User.objects.get(username=username)
                try:
                    get_following = FollowUser.objects.get(follower=user, followed=user)
                except:
                    create_following = FollowUser.objects.create(follower=user, followed=user)
                    create_following.save()
                login(request, user)
                return redirect("home")
        else:
            print("form is not valid")
    context = {"form":LoginForm}
    return render(request, "login.html", context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            form = CreateUserForm()
            return redirect("login_page")
        else:
            print("form is not valid")
    context = {"form":form}
    return render(request, "register.html", context)


def logout_page(request):
    context = {}
    logout(request)
    return redirect("login_page")

















