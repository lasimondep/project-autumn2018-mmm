from django.db import models
from django.contrib.auth.models import User

class Example(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)

class Post(models.Model):
    post = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

