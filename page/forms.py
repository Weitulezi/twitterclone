from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']