from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser


class Photo(models.Model):
    path = models.CharField(max_length=128)
    creation_date = models.DateTimeField(auto_now=True)
    photo = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    when = models.DateTimeField(auto_now=True)
    about = models.ForeignKey(Photo, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
