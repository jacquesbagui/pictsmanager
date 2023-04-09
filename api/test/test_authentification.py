from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.test import TestCase

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('token-auth')
        self.user = User.objects.create_user(username='testuser', password='testpassword123456789')

    #Register Test

    def test_registration(self):
        data = {'username': 'newuser', 'password': 'newpassword123456789'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)


    def test_if_username_already_exists_dont_signup(self):
        data = {'username': 'testuser', 'password': 'newpassword123456789'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0], 'This field must be unique.')

    def test_if_username_not_provided_then_cannot_signup(self):
        data = {'password': 'newpassword'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_if_password_not_provided_then_cannot_signup(self):
        data = {'username': 'newuser'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    #Login Test

    def test_login(self):
        data = {'username': 'testuser', 'password': 'testpassword123456789'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_if_password_incorrect_then_cannot_login(self):
        data = {'username': 'testuser', 'password': 'incorrectpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_if_username_does_not_exist_then_cannot_login(self):
        data = {'username': 'nonexistentuser', 'password': 'testpassword123456789'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_if_username_not_provided_then_cannot_login(self):
        data = {'password': 'testpassword123456789'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_if_password_not_provided_then_cannot_login(self):
        data = {'username': 'testuser'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
