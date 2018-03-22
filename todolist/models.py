from django.db import models
from django.utils import timezone


# Create your models here.
class todo(models.Model):
    name = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description