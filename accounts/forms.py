from django import forms
from accounts.models import Post

class HomeForm(forms.ModelForm):
    post = forms.CharField()
    class Meta:
        model = Post
        fields = {'post',}