from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from accounts.models import Post
import json
from http.client import HTTPConnection
from django.forms import modelformset_factory
from accounts.forms import MyForm
from accounts.forms import HomeForm


def request_mediator(host, head):
    connection = HTTPConnection(host)
    request = connection.request("GET", "/", headers=head)
    response = connection.getresponse()
    connection.close()
    rhead, rdata = response.getheaders(), response.read()
    return rhead, rdata

class GenReqID:
    _ID = 0
    def next(self):
        GenReqID._ID += 1
        return GenReqID._ID




class Homeview(TemplateView):
    template_name='accounts/login.html'













    """"
    #choicefield view
    def get(self, request):
        formy = MyForm()
        return render(request, self.template_name, {'formy': formy})

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['my_mathy_paragraph'] = my_mathy_paragraph
        return context

    def post(self, request):
        formy = MyForm(request.POST)
        if formy.is_valid():
            data = formy.cleaned_data
            text = data['service']
        args = {'formy': formy, 'text': text}


        return render(request, self.template_name, args)
    """



    """"
    #formfield view
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
            # here we are getting tasks
            text = text.split(' ')

            form = HomeForm()
            #return redirect('/account')
        args = {'form': form, 'text': text}

        return render(request, self.template_name, args)
"""
