from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from accounts.models import Post
from django.forms.formsets import formset_factory
from accounts.forms import tempform
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


    #def get(self,request):

    def get(self, request):

        fortry = MyForm()
        formMy = formset_factory(tempform, extra=5)
        return render(request, self.template_name, {"fortry": fortry,})

    def post(self, request):
        if request.method == 'POST' and "choizy" in request.POST:
            fortry = MyForm(request.POST)
            if fortry.is_valid():
                texty = fortry.cleaned_data
                formMy = formset_factory(tempform, extra=5)
                fortry= MyForm()
                return render(request, self.template_name, {'texty': texty, 'fortry': fortry, "formMy": formMy})


        elif request.method == 'POST' and "manyfields1" in request.POST:
            formMyy = formset_factory(tempform, extra=5)
            formMysec = formMyy(request.POST)
            if formMysec.is_valid():
                data = formMysec.cleaned_data
                formMysec = formset_factory(tempform, extra=5)
                return render(request, self.template_name, {"formMysec":formMysec,"data":data})
        elif request.method == 'POST' and "manyfields2" in request.POST:
            formMyy = formset_factory(tempform, extra=9)
            formMythi = formMyy(request.POST)
            if formMythi.is_valid():
                mata = formMythi.cleaned_data
                formMythi = formset_factory(tempform, extra=9)
                return render(request, self.template_name, {"formMythi":formMythi})
        elif request.method == 'POST' and "manyfields3" in request.POST:
            formMyy = formset_factory(tempform, extra=9)
            formMyfou = formMyy(request.POST)
            if formMyfou.is_valid():
                mata = formMyfou.cleaned_data
                formMyfou = formset_factory(tempform, extra=9)
                return render(request, self.template_name, {"formMyfou":formMyfou,"mata":mata})

        else:
            fortry= MyForm()

        return render(request, self.template_name, {'texty': texty, 'fortry':fortry, "formMy":formMy})








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
