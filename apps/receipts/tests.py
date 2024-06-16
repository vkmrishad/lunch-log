import os
from decimal import Decimal

import boto3
import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from moto import mock_aws
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from apps.receipts.models import Receipt
from apps.receipts.views import ReceiptViewSet

User = get_user_model()
path = os.path.join(os.path.dirname(__file__))


# Fixtures for setting up test data
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def user1(create_user):
    return create_user(
        username="user1", email="user1@example.com", password="password1"
    )


@pytest.fixture
def user2(create_user):
    return create_user(
        username="user2", email="user2@example.com", password="password2"
    )


@pytest.fixture
def auth_client(api_client, user1):
    api_client.force_authenticate(user=user1)
    return api_client


@pytest.fixture
def receipt(user1):
    return Receipt.objects.create(
        user=user1,
        restaurant_name="Test Restaurant",
        dated=timezone.now(),
        price=Decimal("99.99"),
        image="path/to/image.jpg",
        street="123 Main St",
        city="Test City",
        state="Test State",
        country="Test Country",
        postal_code="12345",
    )


# Override AWS settings for tests
@pytest.fixture(scope="function", autouse=True)
def override_aws_settings(settings):
    settings.AWS_ACCESS_KEY_ID = "testing"
    settings.AWS_SECRET_ACCESS_KEY = "testing"
    settings.AWS_SECURITY_TOKEN = "testing"
    settings.AWS_SESSION_TOKEN = "testing"
    settings.AWS_BUCKET_REGION = "us-east-1"
    settings.AWS_BUCKET_NAME = "bucket"
    settings.AWS_S3_ENDPOINT_URL = "http://127.0.0.1:5000"


# Set up the mock S3 environment
@pytest.fixture
@mock_aws
def mock_s3_resource():
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="bucket")
    yield conn


# Test cases
@pytest.mark.django_db
def test_create_receipt_with_image(auth_client, user1, mock_s3_resource):
    url = reverse("receipts-list")
    image = SimpleUploadedFile(
        name="test_image.jpg",
        content=open(f"{path}/fixtures/img/receipt.jpeg", "rb").read(),
        content_type="image/jpeg",
    )
    data = {
        "restaurant_name": "New Restaurant",
        "dated": timezone.now().isoformat(),
        "price": "29.99",
        "image": image,
        "street": "456 Another St",
        "city": "Another City",
        "state": "Another State",
        "country": "Another Country",
        "postal_code": "67890",
    }

    factory = APIRequestFactory()
    request = factory.post(url, data, format="multipart")
    request.user = user1
    view = ReceiptViewSet.as_view({"post": "create"})
    response = view(request)
    # assert response.data == 1
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["restaurant_name"] == "New Restaurant"


@pytest.mark.django_db
def test_get_receipt_list(auth_client, receipt, mock_s3_resource):
    url = reverse("receipts-list")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.data.get("results")
    assert len(data) == 1
    assert data[0]["restaurant_name"] == "Test Restaurant"
    assert data[0]["price"] == "99.99"
    assert "image.jpg" in data[0]["image"]
    assert data[0]["street"] == "123 Main St"
    assert data[0]["city"] == "Test City"
    assert data[0]["state"] == "Test State"
    assert data[0]["country"] == "Test Country"
    assert data[0]["postal_code"] == "12345"


@pytest.mark.django_db
def test_get_receipt_detail(auth_client, receipt, mock_s3_resource):
    url = reverse("receipts-detail", args=[receipt.id])
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["restaurant_name"] == "Test Restaurant"


@pytest.mark.django_db
def test_update_receipt(auth_client, receipt, mock_s3_resource):
    url = reverse("receipts-detail", args=[receipt.id])
    data = {"restaurant_name": "Updated Restaurant", "price": "49.99"}
    response = auth_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["restaurant_name"] == "Updated Restaurant"
    assert response.data["price"] == "49.99"


@pytest.mark.django_db
def test_delete_receipt(auth_client, receipt, mock_s3_resource):
    url = reverse("receipts-detail", args=[receipt.id])
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Receipt.objects.filter(id=receipt.id).exists()


@pytest.mark.django_db
def test_unauthenticated_access(api_client, mock_s3_resource):
    url = reverse("receipts-list")
    response = api_client.get(url)
    assert response.data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_access_restrictions(
    api_client, create_user, user1, user2, receipt, mock_s3_resource
):
    api_client.force_authenticate(user=user2)
    url = reverse("receipts-detail", args=[receipt.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# Ensuring user1 can still access their own receipts after testing with user2
@pytest.mark.django_db
def test_owner_access_receipt_detail(auth_client, receipt, mock_s3_resource):
    url = reverse("receipts-detail", args=[receipt.id])
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["restaurant_name"] == "Test Restaurant"
