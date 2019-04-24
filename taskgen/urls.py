from django.urls import path

from . import views

app_name = 'taskgen'
urlpatterns = [
	path('', views.index, name='index'),
	path('list/gen/', views.generate_list, name='generate_list'),
	path('list/db/', views.db_list, name='db_list'),
	path('statements/', views.statements, name='statements'),
	path('change_task/', views.change_task, name='change_task')
]
