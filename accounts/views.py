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
from django import template
#from django.template.defaultfilters import stringfilter
from common import AMQP_client
import time
register = template.Library()


def request_mediator(host, head):
	connection = HTTPConnection(host)
	request = connection.request("GET", "/", headers=head)
	response = connection.getresponse()
	connection.close()
	rhead, rdata = response.getheaders(), response.read()
	return rhead, rdata

class InterfaceClient(AMQP_client):
	_REQUEST_TIMEOUT, _QUEUE_TIMEOUT = 1, 10

	class TimeOutExcept(Exception):
		pass

	class GenReqID:
		_ID = 0

		def next():
			InterfaceClient.GenReqID._ID += 1
			return InterfaceClient.GenReqID._ID

	def __init__(self, Host, e_name, e_type="fanout"):
		super(InterfaceClient, self).__init__(Host, e_name, e_type)
		self.ans_queue = list()

	def send_request(self, to_name, Type, Data=None, to_type="fanout"):
		Id = InterfaceClient.GenReqID.next()
		self.send(to_name, Id, Type, Data, to_type)
		time.sleep(InterfaceClient._REQUEST_TIMEOUT)
		if Id not in map(lambda x: x["Id"], self.ans_queue):
			raise TimeoutError()
		else:
			with open("DEBUG.txt", "a") as fdebout:
				print(self.ans_queue, file=fdebout)
			res = list(filter(lambda x: x["Id"] == Id, self.ans_queue))[0]
			return res["Type"], res["Data"]

	def parse(self, Id, Type, Data):
		self.ans_queue = list(filter(lambda x: time.time() - x["time"] < InterfaceClient._QUEUE_TIMEOUT, self.ans_queue))
		self.ans_queue.append({"time": time.time(), "Id": Id, "Type": Type, "Data": Data})
		with open("DEBUG.txt", "a") as fdebout:
			print(self.ans_queue, file=fdebout)


Client = InterfaceClient("localhost", "interface")
Client.start_consume()

class Homeview(TemplateView):
	template_name='accounts/login.html'

	@register.filter
	def index(List, i):
		return List[int(i)]

	def get(self, request):
		try:
			Type, Data = Client.send_request("facade", "get_taskList")
		except InterfaceClient.TimeOutExcept:
			print("TImeOutError")
		else:
			fortry = HomeForm()
			print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa", Data, "\n\n\n")
			return render(request, self.template_name, {"fortry": fortry,"Data": Data})

	def post(self, request):
		if request.method == 'POST' and "choizy" in request.POST:
			fortry = HomeForm(request.POST)
			if fortry.is_valid():
				texty = fortry.cleaned_data["post"]
				try:
					Type, Data = Client.send_request("facade", "get_task", {"task_id": texty,"args": ""})
					print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBlllllllla", Data, "\n\n\n")
				except InterfaceClient.TimeOutExcept:
					print("TImeOutError")
				else:
					formMy = formset_factory(tempform, extra=5)
					fortry= MyForm()
					check1 = "1"
					return render(request, self.template_name, {'texty': texty, 'fortry': fortry, "formMy": formMy,"check1": check1,"Data1": Data})


		elif request.method == 'POST' and "manyfields1" in request.POST:
			formMyy = formset_factory(tempform, extra=5)
			formMysec = formMyy(request.POST)
			if formMysec.is_valid():
				data = formMysec.cleaned_data
				formMysec = formset_factory(tempform, extra=5)
				check2 = "1"
				Prime = ['string1', 'string2', 'string3', 'string3', 'string3']
				return render(request, self.template_name, {"formMysec":formMysec,"data":data, "check2":check2,"Prime":Prime})
		elif request.method == 'POST' and "manyfields2" in request.POST:
			formMyy = formset_factory(tempform, extra=9)
			formMythi = formMyy(request.POST)
			if formMythi.is_valid():
				mata = formMythi.cleaned_data
				formMythi = formset_factory(tempform, extra=9)
				check3 = "1"
				return render(request, self.template_name, {"formMythi":formMythi,"check3": check3})
		elif request.method == 'POST' and "manyfields3" in request.POST:
			formMyy = formset_factory(tempform, extra=9)
			formMythi = formMyy(request.POST)
			if formMythi.is_valid():
				mata = formMythi.cleaned_data
				formMythi = formset_factory(tempform, extra=9)
				check4 = "1"

				return render(request, self.template_name, {"formMythi":formMythi,"mata":mata,"check4":check4})

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