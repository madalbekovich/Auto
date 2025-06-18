from rest_framework.test import APITestCase
from apps.users.serializers import RegisterSerializers
from apps.users.models import User
from rest_framework import status
from django.urls import reverse
import json
import random

class RegisterApiTestCase(APITestCase):
    def test_register(self):
        random_number = random.randint(111_000, 999_999)
        url = reverse('register')
        # url = "http://localhost:8000/users/register/"
        data = {
            'phone': f'+996997{random_number}',
            'first_name': 'Test',
            'password': 'adminadmin',
            'confirm_password': 'adminadmin',
        }
        response = self.client.post(url, data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        # self.assertEqual(User.objects.get(phone=f'+996997{random_number}'), f'+996997{random_number}')