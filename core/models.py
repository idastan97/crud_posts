from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    text = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
