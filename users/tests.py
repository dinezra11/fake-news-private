from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from registration.models import UserData
from .views import users, delete_user, approve

class UsersViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')

    def test_users_get_request(self):
        request = self.factory.get('/users/')
        request.user = self.admin
        response = users(request)
        self.assertEqual(response.status_code, 200)  # Test if the response is successful

    def test_users_post_request(self):
        request = self.factory.post('/users/', {'radio': 'expert'})
        request.user = self.admin
        response = users(request)
        self.assertEqual(response.status_code, 200)  # Test if the response is successful

    def test_delete_user(self):
        user = User.objects.create_user(username='testuser2', password='testpass2')
        request = self.factory.get('/delete-user/')
        request.user = self.admin
        response = delete_user(request, user.id)
        self.assertEqual(response.status_code, 302)  # Test if the response is a redirect

        # Cleanup
        self.assertFalse(User.objects.filter(id=user.id).exists())

    def test_approve(self):
        user = User.objects.create_user(username='testuser3', password='testpass3')
        UserData.objects.create(user_id=user.id)
        request = self.factory.get('/approve/')
        request.user = self.admin
        response = approve(request, user.id)
        self.assertEqual(response.status_code, 302)  # Test if the response is a redirect

        # Cleanup
        self.assertTrue(UserData.objects.filter(user_id=user.id, Pending=False).exists())

