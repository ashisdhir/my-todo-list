from django.db import models
from django.utils import timezone


# Create your models here.
class TodoTitle(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class TodoDetail(models.Model):
    todotitle = models.ForeignKey(TodoTitle, on_delete=models.CASCADE)
    description = models.TextField()
    completed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.description


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
