from django.shortcuts import render
from registration.models import UserData
from articles.models import PredictionApproves, ArticleCache
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64


# Create your views here.
def graphPredictionapprovess(request):
    Predictionapprovess = PredictionApproves.objects.filter(expertId=request.user.id)
    articles = ArticleCache.objects.all()
    name = request.user.username
    agree = 0
    disagree = 0
    for article in articles:
        if Predictionapprovess.filter(link=article.link).exists():
            if Predictionapprovess.get(link=article.link).approved:
                agree += 1
            else:
                disagree += 1
    ###############################################################
    x = ['agree', 'disagree']
    y = [agree, disagree]
    sns.barplot(x=x, y=y)
    plt.xlabel('agree or disagree')
    plt.ylabel('number of articles')
    plt.title('expert ' + name + ' agree or disagree with our Model')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    # Pass the plot to the template context
    context = {'image': image_base64}
    return render(request, 'graphs_statistics/graph.html', context)
