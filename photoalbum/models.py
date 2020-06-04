from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser


class Photo(models.Model):
    votes = models.IntegerField(default=0)
    path = models.CharField(max_length=128, verbose_name='Podaj ścieżkę nowego zdjęcia: ')
    creation_date = models.DateTimeField(auto_now=True)
    photo = models.ForeignKey(User, on_delete=models.CASCADE)




class Comment(models.Model):
    comment = models.TextField()
    when = models.DateTimeField(auto_now=True)
    about = models.ForeignKey(Photo, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class Vote(models.Model):
    like = models.NullBooleanField(null=True)
    voting_photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    voting_user = models.ManyToManyField(User)