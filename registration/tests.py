from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserData
from .forms import UserRegisterForm


class UserRegistrationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_user(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'firstname': 'Test',
            'lastname': 'User',
            'isexpert': True,
            'pic': '',
            'Certificate': '',
            'isAdmin': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(UserData.objects.filter(user__username='testuser').exists())


class UserLoginTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.register_url = reverse('register')

        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_valid_form(self):
        form_data = {
            'username': 'testuser2',
            'email': 'testuserexample.com',
            'password1': 'password123',
            'password2': 'password123',
            'firstname': 'John',
            'lastname': 'Doe',
        }

        form = UserRegisterForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123',
            'firstname': 'John',
            'lastname': '',  # missing required field
        }

        form = UserRegisterForm(data=form_data)

        self.assertFalse(form.is_valid())

        self.assertIn('lastname', form.errors)
