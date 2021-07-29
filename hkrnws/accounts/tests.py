from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status


class TestUserRegistration(TestCase):
    url = '/users/register'

    def test_user_create(self):
        client = APIClient()
        payload = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }
        response = client.post(self.url, payload, format='json')

        self.assertEqual(User.objects.count(), 1)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data['username'], payload['username'])
        self.assertEqual(response.data['email'], payload['email'])
        self.assertFalse('password' in response.data)
