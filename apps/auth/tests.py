import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_user(api_client):
    """
    Test user registration
    :param api_client:
    :return:
    """
    url = reverse("signup")
    data = {
        "email": "test@example.com",
        "password": "testpassword",
        "password2": "testpassword",
        "first_name": "John",
        "last_name": "Doe",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    # assert User.objects.filter(email='testuser').exists()


@pytest.mark.django_db
def test_register_user_missing_fields(api_client):
    """
    Test user registration with missing fields
    :param api_client:
    :return:
    """
    url = reverse("signup")
    data = {
        "email": "test@example.com",
        "password": "testpassword",
        "password2": "testpassword",
        # Missing 'first_name' and 'last_name'
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "first_name" in response.data
    assert "last_name" in response.data


@pytest.mark.django_db
def test_register_user_invalid_format(api_client):
    """
    Test user registration with invalid email format
    :param api_client:
    :return:
    """
    url = reverse("signup")
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "test@@example.com",
        "password": "testpassword",
        "password2": "testpassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db
def test_login_user(api_client):
    """
    Test user login with correct and incorrect credentials
    :param api_client:
    :return:
    """
    # Create a user for testing
    User.objects.create_user(
        username="testuser",
        password="testpassword",
        email="test@example.com",
        first_name="John",
        last_name="Doe",
    )

    url = reverse("login")
    # Correct login credentials
    data = {"email": "test@example.com", "password": "testpassword"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "csrf_token" in response.data
    assert "session_id" in response.data

    # Incorrect password
    data_wrong_password = {"email": "test@example.com", "password": "wrongpassword"}
    response_wrong_password = api_client.post(url, data_wrong_password, format="json")
    assert response_wrong_password.status_code == status.HTTP_400_BAD_REQUEST
    assert "non_field_errors" in response_wrong_password.data


@pytest.mark.django_db
def test_password_validation(api_client):
    """
    Test password validation with common and short passwords
    :param api_client:
    :return:
    """
    url = reverse("signup")
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "test@example.com",
        "password": "password",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data
    assert response.data["password"][0] == "This password is too common."

    data["password"] = "1234"
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data
    assert (
        response.data["password"][0]
        == "This password is too short. It must contain at least 8 characters."
    )
    assert response.data["password"][1] == "This password is too common."


@pytest.mark.django_db
def test_logout_user(api_client):
    """
    Test user logout
    :param api_client:
    :return:
    """
    # Create a user for testing
    User.objects.create_user(
        "testuser",
        password="testpassword",
        email="test@example.com",
        first_name="John",
        last_name="Doe",
    )

    # Log in the user first
    login_url = reverse("login")
    login_data = {"email": "test@example.com", "password": "testpassword"}
    login_response = api_client.post(login_url, login_data, format="json")
    assert login_response.status_code == status.HTTP_200_OK

    # Extract CSRF token and session ID from login response
    csrf_token = login_response.data["csrf_token"]
    session_id = login_response.data["session_id"]

    # Set CSRF token in the client headers
    api_client.credentials(HTTP_X_CSRFTOKEN=csrf_token)

    # Logout the user
    logout_url = reverse("logout")
    logout_response = api_client.get(logout_url)
    assert logout_response.status_code == status.HTTP_200_OK
    assert "message" in logout_response.data
    assert logout_response.data["message"] == "Logout successful"
    assert not api_client.session.exists(session_id)
