from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from reviews.models import Review
from django.test import TestCase, Client
from django.urls import reverse
from .models import Review


class ReviewModelTest(TestCase):
    def test_create_review(self):
        review = Review.objects.create(
            name="John",
            email="din@example.com",
            title="Great product!",
            content="I"
        )
        self.assertEqual(review.name, "John")
        self.assertEqual(review.email, "din@example.com")
        self.assertEqual(review.title, "Great product!")
        self.assertEqual(review.content, "I")

    def setUp(self):
        self.client = Client()

    def test_view_form(self):
        response = self.client.post('/reviews/', {
                'name': 'John Doe',
                'email': 'johndoe@example.com',
                'title': 'A review',
                'description': 'This is a great product!'
            })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/submitted.html')
