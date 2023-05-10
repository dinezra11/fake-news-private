from django.db import models
from registration.models import UserData


# Create your models here.
class ArticleCache(models.Model):
    link = models.CharField(max_length=200, default="unknown", primary_key=True)
    content = models.CharField(max_length=300, default="")
    img = models.CharField(max_length=200, default="")
    isFake = models.BooleanField(default=False)


class PredictionApproves(models.Model):
    title = models.CharField(max_length=200, default="unknown")
    link = models.CharField(max_length=200, default="unknown")
    expertId = models.IntegerField()
    expertName = models.CharField(max_length=50, default="unknown")
    approved = models.BooleanField(default=True) # True for like, False for dislike

    def __str__(self):
        return self.link
