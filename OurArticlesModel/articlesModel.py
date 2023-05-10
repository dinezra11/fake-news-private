from GoogleNews import GoogleNews as g
import newspaper
from django.db.models import Count
from articles.models import ArticleCache, PredictionApproves

import re
import numpy as np
import pandas as pd
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def initializeEngine(query: str = None, language: str = "en"):
    """ Given a query, initialize the engine for the article retrieval.

    :param query:           Search query.
    :param language:        The language of the articles.
    :return:                GoogleNews engine object.
    """

    # Find Articles
    gn = g(lang=language, period='1d')
    gn.search(query)

    return gn


def getPage(engine: g, page: int = 1):
    """ Given a query, find and return the relevant articles from Google News.

    :param engine:          A GoogleNews engine object, pre-initialized.
                            Call the function 'initializeEngine' before calling this function.
    :param page:            The page index.
    :return:                A dataframe of the articles, with the columns:
                            ['title', 'content', 'media', 'link', 'img', 'datetime']
    """

    def getContent(link):
        """ Given a link to a specific article, return the content of it (text) and the img path.
        Check if the article already cached before using the api.

        :param link:        The link for the article.
        :return:            Article's content and img path, as a list of strings.
        """
        articleObject = ArticleCache.objects.filter(link=link)
        if articleObject.exists():
            articleObject = articleObject.first()

            return [getattr(articleObject, 'content'), getattr(articleObject, 'img')]
        else:
            article = newspaper.Article(link)
            article.download()
            article.parse()

            ArticleCache.objects.create(
                link = link,
                content = article.text,
                img = article.top_img
            )

            return [article.text, article.top_img]

    # Find Articles
    df = pd.DataFrame(engine.page_at(page)).iloc[:6]

    # Check which articles are already cached in the database
    df[['content', 'img']] = df['link'].apply(lambda l: getContent(l)).to_list()

    # Get statistical data
    df['approvesCount'] = df['link'].apply(lambda l: PredictionApproves.objects.filter(link=l, approved=True).aggregate(Count('expertId'))['expertId__count'])
    df['denialsCount'] = df['link'].apply(lambda l: PredictionApproves.objects.filter(link=l, approved=False).aggregate(Count('expertId'))['expertId__count'])
    df['approvals'] = df['link'].apply(lambda l: PredictionApproves.objects.filter(link=l, approved=True))
    df['denials'] = df['link'].apply(lambda l: PredictionApproves.objects.filter(link=l, approved=False))

    # Get predictions from classifier
    df['predict'] = getPrediction(df)

    return df[['title', 'content', 'media', 'link', 'img', 'date', 'approvesCount', 'denialsCount', 'predict', 'approvals', 'denials']]


def getPrediction(data):
    """ Given a data, use the classifier to predict whether the article is FAKE or LEGIT.
    Return the preprocessed data.
    """
    def preprocessing(rawData):
        """ Preprocess the data. """

        def stemming(content):
            stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
            stemmed_content = stemmed_content.lower()
            stemmed_content = stemmed_content.split()
            stemmed_content = [ps.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
            stemmed_content = ' '.join(stemmed_content)
            return stemmed_content

        nltk.download('stopwords')
        ps = PorterStemmer()
        newData = rawData['media'] + ' ' + rawData['title']

        # Tokenization and stop words
        newData = newData.apply(stemming)

        # TF-IDF Vectorization
        file = open('OurArticlesModel/tfidf vectorizer', 'rb')
        vectorizer = pickle.load(file)
        newData = vectorizer.transform(newData)
        file.close()

        return newData

    processedData = preprocessing(data)

    file = open('OurArticlesModel/Fake News Classifier - LR', 'rb')
    model = pickle.load(file)
    prediction = model.predict(processedData).astype(bool)
    prediction = pd.Series(prediction).apply(lambda x: "Legit" if x else "FAKE!")
    file.close()

    return prediction
