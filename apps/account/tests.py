from json import loads as json_load

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

UserModel = get_user_model()


class LogoutAPIViewTestCase(APITestCase):
    """
    LogoutAPIView test case.

    supported methods:
    - POST
        cases:
        - logout without data
        - logout without 'refresh' parameter in data
        - logout with invalid refresh token
        - logout not authenticated with valid refresh token
        - logout with valid refresh token
    """

    logout_url = reverse('logout_api')

    def setUp(self):
        """
        Initial setup that will be performed before each test
        """

        # Create a new user
        username = 'anon'
        password = 'Change_me_123!'
        UserModel.objects.create_user(username=username, password=password)

        # Make the request for login with user and retrieve JWT tokens
        login_url = reverse('token_obtain_pair')
        payload = {'username': username, 'password': password}
        response = self.client.post(login_url, data=payload, format='json')
        response_data = json_load(response.content)

        # Save JWT tokens for authentication during test
        self.access_token = response_data['access']
        self.refresh_token = response_data['refresh']

    def test_logout_successful(self):
        # Make the request for logout as authenticated user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        payload = {'refresh': self.refresh_token}
        response = self.client.post(self.logout_url, data=payload, format='json')

        # Assertion for a successful logout
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_no_data(self):
        # Make the request for logout as authenticated user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(self.logout_url, format='json')
        response_data = json_load(response.content)

        # Assertion for a failing logout cause invalid refresh token
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['error'], 'Refresh token not provided')

    def test_logout_no_refresh(self):
        # Make the request for logout as authenticated user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        payload = {'token': self.refresh_token}
        response = self.client.post(self.logout_url, data=payload, format='json')
        response_data = json_load(response.content)

        # Assertion for a failing logout cause invalid refresh token
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['error'], 'Refresh token not provided')

    def test_logout_invalid_refresh(self):
        # Make the request for logout as authenticated user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        payload = {'refresh': 'invalid_refresh_token'}
        response = self.client.post(self.logout_url, data=payload, format='json')
        response_data = json_load(response.content)

        # Assertion for a failing logout cause invalid refresh token
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['error'], 'Token is invalid or expired')

    def test_logout_not_authenticated_valid_refresh(self):
        # Make the request for logout as unauthenticated user
        payload = {'refresh': self.refresh_token}
        response = self.client.post(self.logout_url, data=payload, format='json')

        # Assertion for an unauthorized logout
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
