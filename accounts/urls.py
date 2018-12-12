from django.urls import path
from . import views
from .views import Homeview

urlpatterns = [
    path('', Homeview.as_view(), name='home')
]