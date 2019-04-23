from django.urls import path

from . import views

app_name = 'taskgen'
urlpatterns = [
	path('', views.index, name='index'),
	path('generate_list/', views.generate_list, name='generate_list'),
	path('db_list/', views.db_list, name='db_list'),
	path('load/', views.load_tasks, name='load'),
	path('change_task/', views.change_task, name='change_task')
]
