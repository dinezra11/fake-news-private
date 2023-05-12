from django.shortcuts import render
from registration.models import UserData
from articles.models import PredictionApproves, ArticleCache
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd


# Create your views here.
def graphPredictionapprovess(request):
    plt.clf()

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


def graphGeneral(request):
    """ Graph of general statistics about the model performance. """

    # Model's Predictions Graph
    plt.clf()

    legitCount = ArticleCache.objects.filter(isFake=False).count()
    fakeCount = ArticleCache.objects.filter(isFake=True).count()

    dfCount = pd.read_csv('OurArticlesModel/news data/validation set labels.csv')['label'].value_counts()

    legitCount += int(dfCount[1])
    fakeCount += int(dfCount[0])

    data = [legitCount, fakeCount]
    labels = ['Predicted as Legit', 'Predicted as Fake']
    colors = sns.color_palette('pastel')[0:2]

    plt.pie(data, labels=labels, colors=colors, autopct='%.0f%%')
    plt.title("Classification Model's Predictions Comparison")

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    modelGraph = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    # Type of Users Graph
    plt.clf()

    expertsCount = UserData.objects.filter(isexpert=True).count()
    adminCount = UserData.objects.filter(isAdmin=True).count()
    normalCount = UserData.objects.filter(isexpert=False, isAdmin=False).count()

    data = []
    labels = []

    if expertsCount > 0:
        data.append(expertsCount)
        labels.append('Experts')
    if adminCount > 0:
        data.append(adminCount)
        labels.append('Admins')
    if normalCount > 0:
        data.append(normalCount)
        labels.append('Users')

    colors = sns.color_palette('pastel')[0:3]

    plt.pie(data, labels=labels, colors=colors, autopct='%.0f%%')
    plt.title("Total Registered Users Type")

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    usersGraph = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    # Pass the plot to the template context
    context = {'modelGraph': modelGraph, 'usersGraph': usersGraph}
    return render(request, 'graphs_statistics/general_graphs.html', context)
