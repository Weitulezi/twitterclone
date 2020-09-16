from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Tweet

class TweetForm(forms.ModelForm):
    content = forms.CharField(max_length=1000, widget=CKEditorWidget(config_name='awesome_ckeditor'))
    class Meta:
        model = Tweet
        fields = ["content"]


class RetweetForm(forms.ModelForm):
    content = forms.CharField(max_length=1000, widget=CKEditorWidget(config_name='awesome_ckeditor'))
    class Meta:
        model = Tweet
        fields = ["content"]