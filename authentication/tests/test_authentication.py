import logging
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

client = APIClient()


@pytest.mark.django_db
def test_user_login():
    user = User.objects.create_user(username="testuser", password="password123")
    response = client.post(
        "/api/auth/login/", {"username": "testuser", "password": "password123"}
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_user_logout():
    # Create a user and generate tokens
    user = User.objects.create_user(username="testuser", password="password123")
    refresh = RefreshToken.for_user(user)

    # Use credentials for authorization
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    # Log refresh token and access token
    logging.info(f"Access Token: {refresh.access_token}")
    logging.info(f"Refresh Token: {str(refresh)}")

    # Log headers for troubleshooting
    logging.info(f"Headers: {client._credentials}")

    # Make the logout request
    response = client.post(
        "/api/auth/logout/",
        data={"refresh": str(refresh)},
        format="json"
    )

    # Log detailed response on failure
    if response.status_code == 400:
        logging.error(f"Status Code: {response.status_code}")
        logging.error(f"Response Headers: {response.headers}")
        logging.error(f"Response Data: {response.data}")

    # Assert the status code is 200 or 205
    assert response.status_code in [200, 205]