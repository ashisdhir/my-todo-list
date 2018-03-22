from django.db import models


# Create your models here.
class todo(models.Model):
    name = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField()
    created = models.DateTimeField()

    def __str__(self):
        return self.description