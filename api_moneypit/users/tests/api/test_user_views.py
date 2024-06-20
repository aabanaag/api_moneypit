import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api_moneypit.users.tests.factories import UserFactory


@pytest.mark.django_db()
class UserViewTestCase(APITestCase):
    def setUp(self):
        super().setUp()

        self.user = UserFactory.create()

        self.client.force_login(self.user)

    def test_should_return_user_details(self):
        url = reverse("api:user-me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
