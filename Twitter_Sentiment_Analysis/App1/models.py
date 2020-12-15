from django.db import models
from django.conf import settings

# Create your models here.

class Search1 (models.Model):
    username= models.CharField(max_length=256)
    search = models.CharField(max_length=256)

    def __str__(self):
        return "{}".format(self.search)
