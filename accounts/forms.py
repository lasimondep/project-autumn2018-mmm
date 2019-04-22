from django import forms
from accounts.models import Post
from django.forms.formsets import formset_factory


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
    SERVICES = (('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3'))
    service = forms.ChoiceField(choices=SERVICES, label="Sector")
#    def __init__(self, *args, **kargs):
#        super().__init__(args, kargs)
#        with open("DEBUG.html", "w") as _fdeb:
#            print(MyForm.service, file=_fdeb)

class tempform(forms.Form):
    title = forms.CharField(label="")

x = 5
tempformset = formset_factory(tempform, extra=x)

tempyformset = tempformset()
for form in tempyformset:
     print(tempformset)