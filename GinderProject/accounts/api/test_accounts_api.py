import GinderProject.settings as settings
import jwt
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class UserAPITestCase(APITestCase):
    """
    Tests of accounts app
    """

    def setUp(self) -> None:
        User.objects.create_user("TestUser", "TestUser@mail.ru", "TestUserPassword")

    def test_register_user_fail_on_password2_not_given(self):
        """
        field "password2" not given -> failed
        """
        url = reverse('accounts:register')
        data = {
            'username': 'TestUser',
            'email': 'TestUser@mail.ru',
            'password': 'TestUserPassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_success(self):
        """
        all fields given -> user registered, token given
        """
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

    def test_registration_when_user_is_authenticated_and_credentials_given(self):
        """
        if user has JWT header in request -> Forbidden
        """
        url_register = reverse('accounts:register')
        url_login = reverse('accounts:login')
        data = {
            'username': "TestUser",
            'password': "TestUserPassword"
        }
        login_response = self.client.post(url_login, data, format='json')
        token = login_response.data.get('token', '')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        register_data = {
            'username': 'TestUser2',
            'email': 'TestUser2@mail.ru',
            'password': 'TestUser2Password',
            'password2': 'TestUser2Password',
        }
        register_response = self.client.post(url_register, register_data, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login(self):
        """
        giving credentials to login endpoint -> getting token
        """
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

    def test_refresh_token(self):
        """
        give refresh token to refresh endpoint -> new token given
        """
        get_token_url = reverse('accounts:login')
        update_url = reverse('accounts:token_refresh')
        data = {
            'username': 'TestUser',
            'password': 'TestUserPassword',
        }
        response_on_get = self.client.post(get_token_url, data, format='json')
        refresh_get_on_login = response_on_get.data.get('refresh', False)
        token_get_on_login = response_on_get.data.get('token', False)
        data = {
            'refresh': refresh_get_on_login
        }
        response_on_refresh = self.client.post(update_url, data, format='json')
        # checks if status code is OK
        self.assertEqual(response_on_refresh.status_code, status.HTTP_200_OK)
        access = response_on_refresh.data.get('access', '')
        # checks token existence
        self.assertGreater(len(access), 0)
        decoded_on_login = jwt.decode(token_get_on_login, key=settings.SECRET_KEY,
                                      algorithms=settings.SIMPLE_JWT['ALGORITHM'])
        user_id_on_login = decoded_on_login['user_id']
        decoded_on_refresh = jwt.decode(access, key=settings.SECRET_KEY,
                                        algorithms=settings.SIMPLE_JWT['ALGORITHM'])
        user_id_on_refresh = decoded_on_login['user_id']
        # checks if user gets its own token on refresh
        self.assertEqual(user_id_on_login, user_id_on_refresh)
