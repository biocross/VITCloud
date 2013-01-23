from django.db import models


class File(models.Model):
    name = models.CharField(max_length=250)
    size = models.CharField(max_length=100)
    block = models.CharField(max_length=6)
    room = models.CharField(max_length=6)
    date = models.DateTimeField()


