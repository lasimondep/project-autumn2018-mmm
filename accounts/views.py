from django.shortcuts import render, HttpResponse, redirect
from accounts.forms import HomeForm
from django.views.generic import TemplateView
from  django.contrib.auth.models import User
from accounts.models import Post
import json

class Homeview(TemplateView):
    template_name='accounts/login.html'

    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['my_mathy_paragraph'] = my_mathy_paragraph
        return context

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
            new = '''
            {
                "GlossSeeAlso": "1"
            }
            '''
            data = json.loads(new)
            data['GlossSeeAlso'] = text
            text= str(data['GlossSeeAlso'])
            form = HomeForm()
            #return redirect('/account')
        args = {'form': form, 'text': text}

        return render(request, self.template_name, args)
