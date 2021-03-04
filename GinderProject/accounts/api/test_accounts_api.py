import jwt
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import GinderProject.settings as settings

class UserAPITestCase(APITestCase):
    """
    Tests of accounts app
    """

    def setUp(self) -> None:
        User.objects.create_user("TestUser", "TestUser@mail.ru", "TestUserPassword")

    def test_register_user_fail_on_password2_not_given(self):
        url = reverse('accounts:register')
        data = {
            'username': 'TestUser',
            'email': 'TestUser@mail.ru',
            'password': 'TestUserPassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_success(self):
        url = reverse('accounts:register')
        data = {
            'username': 'TestUser2',
            'email': 'TestUser2@mail.ru',
            'password': 'TestUser2Password',
            'password2': 'TestUser2Password',
        }
        response = self.client.post(url, data, format='json')
        # checks that comes response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # checks that response contains token
        self.assertGreater(len(response.data.get("token", 0)), 0)
        # checks that user is created
        self.assertEqual(User.objects.filter(username='TestUser2').count(), 1)

    def test_user_login(self):
        url = reverse('accounts:login')
        data = {
            'username': 'TestUser',
            'password': 'TestUserPassword',
        }
        response = self.client.post(url, data, format='json')
        # checks if response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token', False)
        # checks if token send back
        self.assertGreater(len(token), 0)
        decoded = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT['ALGORITHM'])
        user_id = decoded['user_id']
        # checks that token is own by requested user
        self.assertEqual(User.objects.get(pk=user_id).username,
                         response.data.get('user'))
