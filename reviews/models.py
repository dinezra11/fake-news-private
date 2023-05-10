from django.db import models


# Create your models here.
class Review(models.Model):
    name = models.CharField(max_length=100, default="unknown")
    email = models.CharField(max_length=40, default="unknown")
    title = models.CharField(max_length=40, default="")
    content = models.CharField(max_length=250, default="")
