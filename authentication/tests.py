from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import User


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username="testuser",
            nom="Doe",
            prenom="John",
            date_de_naissance="1990-01-01",
            adr_email="john@example.com",
            password="mypassword",
            localisation="New York",
            numero_de_tel="1234567890",
            description="Lorem ipsum",
            photo_de_profile=None
        )

    def test_user_signup(self):
        signup_url = reverse('signup')
        data = {
            'username': 'newuser',
            'nom': 'Doe',
            'prenom': 'John',
            'date_de_naissance': '1990-01-01',
            'adr_email': 'john@example.com',
            'password': 'mypassword',
            'localisation': 'New York',
            'numero_de_tel': '1234567890',
            'description': 'Lorem ipsum',
            'photo_de_profile': None
        }
        response = self.client.post(signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_signup_invalid_data(self):
        signup_url = reverse('signup')
        data = {
            'username': 'newuser',
            'nom': 'Doe',
            'prenom': 'John',
            'date_de_naissance': '1990-01-01',
            'adr_email': 'john@example.com',
            'password': '',  # Invalid data, empty password
            'localisation': 'New York',
            'numero_de_tel': '1234567890',
            'description': 'Lorem ipsum',
            'photo_de_profile': None
        }
        response = self.client.post(signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
