from django.urls import path

from . import views

app_name = 'taskgen'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/gen/', views.generate_list, name='generate_list'),
    path('list/db/', views.db_list, name='db_list'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('statements/', views.statements, name='statements'),
    path('statements/download', views.download, name='download'),
    path('debug', views.debug_statements, name='debug')
]
