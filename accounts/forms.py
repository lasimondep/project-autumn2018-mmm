from django import forms
from accounts.models import Post


class HomeForm(forms.ModelForm):
    post = forms.CharField()
    class Meta:
        model = Post
        fields = {'post',}


my_choice_field = (
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
)

class NewArticleForm(forms.Form):
    c =[("1", "Option 1"), ("2", "Option 2")]
    choices = forms.ChoiceField(choices=c, label="Choices")


class MyForm(forms.Form):
    SERVICES = (
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
)
    SUBJECTS = (
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
)

    service = forms.ChoiceField(choices=SERVICES, widget=forms.Select(attrs={'id':'radioregion'}), label="Sector")
