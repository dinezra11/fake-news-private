from django.test import TestCase
from django.test import Client
from django.urls import reverse

# Create your tests here.
from django.test import TestCase
from .models import ArticleCache, PredictionApproves


class ArticleCacheModelTest(TestCase):
    def test_default_values(self):
        article = ArticleCache.objects.create(link="example.com")
        self.assertEqual(article.content, "")  # Test default value for content field
        self.assertEqual(article.img, "")  # Test default value for img field
        self.assertFalse(article.isFake)  # Test default value for isFake field

    def test_str_representation(self):
        article = ArticleCache.objects.create(link="example.com")
        self.assertEqual(str(article.link), "example.com")  # Test __str__ method


class PredictionApprovesModelTest(TestCase):
    def test_default_values(self):
        prediction = PredictionApproves.objects.create(title="example", link="example.com", expertId=1,
                                                       expertName="example")
        self.assertTrue(prediction.approved)  # Test default value for approved field

    def test_str_representation(self):
        prediction = PredictionApproves.objects.create(title="example", link="example.com", expertId=1,
                                                       expertName="example")
        self.assertEqual(str(prediction.link), "example.com")  # Test __str__ method

    def test_expertId(self):
        prediction = PredictionApproves.objects.create(title="example", link="example.com", expertId=1,
                                                       expertName="example")
        self.assertEqual(prediction.expertId, 1)


from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import PredictionApproves
from .views import catalog, addApprove

class CatalogViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_catalog_get_request(self):
        request = self.factory.get('/catalog/')
        request.user = self.user
        response = catalog(request)
        self.assertEqual(response.status_code, 200)  # Test if the response is successful


        # Cleanup
        self.user.delete()

