from django.urls import path

from . import views

app_name = 'taskgen'
urlpatterns = [
	path('', views.index, name='index'),
	path('list/gen/', views.generate_list, name='generate_list'),
	path('list/db/', views.db_list, name='db_list'),
	path('login/', views.my_view, name='my_view'),
	path('register/', views.my_view_reg, name='my_view_reg'),
	path('statements/', views.statements, name='statements'),
	path('statements/download', views.download, name='download')
]
