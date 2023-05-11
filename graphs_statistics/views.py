from django.shortcuts import render
from registration.models import UserData
from articles.models import PredictionApproves, ArticleCache
# Create your views here.
def graphPredictionapprovess(request):
    Predictionapprovess = PredictionApproves.objects.filter(expertId=request.user.id)
    articles = ArticleCache.objects.all()
    agree = 0
    notgree = 0
    for article in articles:
        if Predictionapprovess.filter(link=article.link).exists():
            if Predictionapprovess.get(link=article.link).approved:
                agree += 1
            else:
                notgree += 1

    print("agree:" +str(agree))
    print("notagree" +str(notgree))
