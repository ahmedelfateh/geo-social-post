from test_plus.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from app.utils.test_helper import get_tokens
from app.users.tests.factories import UserFactory


class TestRegisterUser(TestCase):
    def setUp(self):
        self.url = "/api/v1/users/register/"
        self.client = APIClient()
        self.data = {
            "email": "elfateh91@gmail.com",
            "password": "1234qwer@",
            "password2": "1234qwer@",
            "first_name": "ahmed test",
        }

    def test_register_user_pass(self):
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_fail_duplicated_email(self):
        UserFactory(email="elfateh91@gmail.com")
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_fail_invalid_email(self):
        self.data = {
            "email": "elfateh91.try.fail@gmail.com",
            "password": "1234qwer",
            "password2": "1234qwer",
            "first_name": "ahmed test",
        }
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_fail_unqualified_pass(self):
        self.data = {
            "email": "elfateh91@gmail.com",
            "password": "1234qwer",
            "password2": "1234qwer",
            "first_name": "ahmed test",
        }
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_fail_wrong_pass(self):
        self.data = {
            "email": "elfateh91@gmail.com",
            "password": "1234qwer@",
            "password2": "1234qwer",
            "first_name": "ahmed test",
        }
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestLoginUser(TestCase):
    def setUp(self):
        self.url = "/api/v1/users/login/"
        self.client = APIClient()
        self.user = UserFactory(email="elfateh91@gmail.com")
        self.data = {"email": "elfateh91@gmail.com", "password": "password"}

    def test_register_user_login_pass(self):
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user_login_fail(self):
        self.data = {"email": "elfateh91@gmail.com", "password": "password1"}
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestGetMeAPI(TestCase):
    def setUp(self):
        self.url = "/api/v1/users/me/"
        self.client = APIClient()
        self.user = UserFactory()
        token = get_tokens(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_retrieve_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        self.data = {"first_name": "ahmed test"}
        response = self.client.patch(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
