from django.test import TestCase
from hkrnws.accounts.models import User

from rest_framework.test import APIClient
from rest_framework import serializers, status
from hkrnws.accounts.serializers import UserRegistrationSerializer


class TestUserRegistration(TestCase):
    url = '/api/users/register/'

    @classmethod
    def setUpTestData(cls):
        test_user = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'somepassword',
            'password2': 'somepassword'
        }
        serializer = UserRegistrationSerializer(data=test_user)
        if serializer.is_valid():
            cls.testuser = serializer.save()

    def test_user_create(self):
        client = APIClient()
        payload = {
            'email': 'foobar@example.com',
            'username': 'foobar',
            'password': 'somepassword',
            'password2': 'somepassword'
        }
        response = client.post(self.url, payload, format='json')

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], payload['username'])
        self.assertEqual(response.data['email'], payload['email'])
        self.assertFalse('password' in response.data)

    def test_duplicate_email_user_not_created(self):
        client = APIClient()
        payload = {
            'email': 'testuser@example.com',
            'username': 'foobar',
            'password': 'somepassword',
            'password2': 'somepassword'
        }
        response = client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, "user with this email already exists.", status_code=status.HTTP_400_BAD_REQUEST)

    def test_duplicate_username_user_not_created(self):
        client = APIClient()
        payload = {
            'email': 'test2@example.com',
            'username': 'testuser',
            'password': 'somepassword',
            'password2': 'somepassword'
        }
        response = client.post(self.url, payload, format='json')

        self.assertContains(response, "A user with that username already exists.", status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_different_password_user_not_created(self):
        client = APIClient()
        payload = {
            'email': 'test2@example.com',
            'username': 'sadsa',
            'password': 'somepassword',
            'password2': 'dasdsaf'
        }
        response = client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserLogin(TestCase):
    url = '/users/login/'
