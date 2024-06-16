import json
import os
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

# Import the APIClient from Django REST framework
from rest_framework.test import APIClient

from apps.receipts.models import Receipt
from apps.recommendations.helpers import update_restaurant_data_from_google_places

# Import other necessary modules and fixtures
from apps.recommendations.models import Restaurant

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user1():
    return User.objects.create_user(
        first_name="Test",
        last_name="User1",
        email="testuser1@example.com",
        username="testuser1@example.com",
        password="testpassword1",
    )


@pytest.fixture
def authenticated_client(api_client, user1):
    api_client.force_authenticate(user=user1)
    return api_client


# Fixture to mock the Google Places API response
@pytest.fixture
def mock_google_places_response():
    path = os.path.join(os.path.dirname(__file__), "fixtures/google_places_data.json")
    with open(path) as f:
        return json.load(f)


@pytest.mark.django_db
def test_update_restaurant_data_from_google_places(mock_google_places_response):
    """
    Test updating restaurant data from Google Places API
    """
    # Create a Receipt object
    Receipt.objects.create(
        user=User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="John",
            last_name="Doe",
        ),
        restaurant_name="Test Restaurant",
        dated="2024-06-15T12:00:00Z",
        price=100.00,
        image="receipts/test_image.jpg",
        street="123 Main St",
        city="Springfield",
        state="IL",
        country="US",
        postal_code="62701",
    )

    # Mock the Google Places API response
    with patch(
        "apps.recommendations.utils.GooglePlacesAPI.search_places"
    ) as mock_get_places:
        mock_get_places.return_value = mock_google_places_response

        update_restaurant_data_from_google_places()

    # Assert that Restaurant objects were created or updated as expected
    restaurants = Restaurant.objects.all().order_by("id")
    restaurant_count = restaurants.count()

    places_ = mock_google_places_response.get("places")

    # Assert first Restaurant object
    assert restaurant_count == len(places_)
    assert restaurants[0].name == places_[0].get("displayName", {}).get("text", "")
    assert restaurants[0].google_place_name == places_[0].get("name", "")
    assert restaurants[0].google_place_id == places_[0].get("id", "")
    assert restaurants[0].types == places_[0].get("types", [])
    assert restaurants[0].national_phone_number == places_[0].get(
        "nationalPhoneNumber", ""
    )
    assert restaurants[0].international_phone_number == places_[0].get(
        "internationalPhoneNumber", ""
    )
    assert restaurants[0].formatted_address == places_[0].get("formattedAddress", "")
    assert restaurants[0].street_number == next(
        (
            comp["shortText"]
            for comp in places_[0].get("addressComponents", [])
            if "street_number" in comp.get("types", [])
        ),
        "",
    )
    assert restaurants[0].street == next(
        (
            comp["shortText"]
            for comp in places_[0].get("addressComponents", [])
            if "route" in comp.get("types", [])
        ),
        "",
    )
    assert restaurants[0].sublocality_level_1 == next(
        (
            comp["shortText"]
            for comp in places_[0].get("addressComponents", [])
            if "sublocality_level_1" in comp.get("types", [])
        ),
        "",
    )
    assert restaurants[0].city == next(
        (
            comp["shortText"]
            for comp in places_[0].get("addressComponents", [])
            if "locality" in comp.get("types", [])
        ),
        "",
    )
    assert restaurants[0].administrative_area_level_3 == next(
        (
            comp["shortText"]
            for comp in places_[0].get("addressComponents", [])
            if "administrative_area_level_3" in comp.get("types", [])
        ),
        "",
    )
    assert restaurants[0].administrative_area_level_2 == next(
        (
            comp["shortText"]
            for comp in places_[0].get("addressComponents", [])
            if "administrative_area_level_2" in comp.get("types", [])
        ),
        "",
    )
    assert restaurants[0].administrative_area_level_1 == next(
        (
            comp["shortText"]
            for comp in places_[0].get("addressComponents", [])
            if "administrative_area_level_1" in comp.get("types", [])
        ),
        "",
    )
    assert restaurants[0].country == next(
        (
            comp["shortText"]
            for comp in places_[0].get("addressComponents", [])
            if "country" in comp.get("types", [])
        ),
        "",
    )
    assert restaurants[0].postal_code == next(
        (
            comp["shortText"]
            for comp in places_[0].get("addressComponents", [])
            if "postal_code" in comp.get("types", [])
        ),
        "",
    )
    assert restaurants[0].plus_code == places_[0].get("plusCode", {})
    assert restaurants[0].latitude == places_[0].get("location", {}).get(
        "latitude", 0.0
    )
    assert restaurants[0].longitude == places_[0].get("location", {}).get(
        "longitude", 0.0
    )
    assert restaurants[0].viewport == places_[0].get("viewport", {})
    assert restaurants[0].rating == places_[0].get("rating", 0.0)
    assert restaurants[0].google_maps_url == places_[0].get("googleMapsUri", "")
    assert restaurants[0].website_url == places_[0].get("websiteUri", "")
    assert restaurants[0].utc_offset_minutes == places_[0].get("utcOffsetMinutes", 0)
    assert restaurants[0].adr_formatted_address == places_[0].get(
        "adrFormatAddress", ""
    )
    assert restaurants[0].business_status == places_[0].get("businessStatus", "")
    assert restaurants[0].price_level == places_[0].get("priceLevel", "")
    assert restaurants[0].user_rating_count == places_[0].get("userRatingCount", 0)
    assert restaurants[0].icon_mask_base_url == places_[0].get("iconMaskBaseUri", "")
    assert restaurants[0].icon_background_color == places_[0].get(
        "iconBackgroundColor", ""
    )
    assert restaurants[0].primary_type_display_name == places_[0].get(
        "primaryTypeDisplayName", {}
    ).get("text", "")
    assert restaurants[0].takeout == places_[0].get("takeout", False)
    assert restaurants[0].delivery == places_[0].get("delivery", False)
    assert restaurants[0].dine_in == places_[0].get("dineIn", False)
    assert restaurants[0].curbside_pickup == places_[0].get("curbsidePickup", False)
    assert restaurants[0].reservable == places_[0].get("reservable", False)
    assert restaurants[0].serves_lunch == places_[0].get("servesLunch", False)
    assert restaurants[0].serves_dinner == places_[0].get("servesDinner", False)
    assert restaurants[0].serves_beer == places_[0].get("servesBeer", False)
    assert restaurants[0].serves_wine == places_[0].get("servesWine", False)
    assert restaurants[0].serves_vegetarian_food == places_[0].get(
        "servesVegetarianFood", False
    )
    assert restaurants[0].primary_type == places_[0].get("primaryType", "")
    assert restaurants[0].short_formatted_address == places_[0].get(
        "shortFormattedAddress", ""
    )


@pytest.mark.django_db
def test_recommendations_endpoint(
    api_client, authenticated_client, mock_google_places_response
):
    """
    Test recommendations endpoint
    """
    # Create a Receipt object
    Receipt.objects.create(
        user=User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="John",
            last_name="Doe",
        ),
        restaurant_name="Test Restaurant",
        dated="2024-06-15T12:00:00Z",
        price=100.00,
        image="receipts/test_image.jpg",
        street="123 Main St",
        city="Springfield",
        state="IL",
        country="US",
        postal_code="62701",
    )

    # Mock the Google Places API response
    with patch(
        "apps.recommendations.utils.GooglePlacesAPI.search_places"
    ) as mock_get_places:
        mock_get_places.return_value = mock_google_places_response
        update_restaurant_data_from_google_places()

    url = reverse("recommendations")
    data = {
        "city": "Hürth",
    }

    # Test authenticated user
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK

    # Restaurant objects at city 'Hürth' should be returned
    restaurants = Restaurant.objects.filter(city__icontains="Hürth").order_by("-id")[
        :10
    ]

    results = response.data.get("results")

    # Assert that the response data matches the Restaurant objects
    assert len(results) == restaurants.count()
    assert results[2].get("name") == restaurants[2].name
    assert results[2].get("google_place_name") == restaurants[2].google_place_name
    assert results[2].get("google_place_id") == restaurants[2].google_place_id
    assert results[2].get("types") == restaurants[2].types
    assert (
        results[2].get("national_phone_number") == restaurants[2].national_phone_number
    )
    assert (
        results[2].get("international_phone_number")
        == restaurants[2].international_phone_number
    )
    assert results[2].get("formatted_address") == restaurants[2].formatted_address
    assert results[2].get("street_number") == restaurants[2].street_number
    assert results[2].get("street") == restaurants[2].street
    assert results[2].get("sublocality_level_1") == restaurants[2].sublocality_level_1
    assert results[2].get("city") == restaurants[2].city
    assert (
        results[2].get("administrative_area_level_3")
        == restaurants[2].administrative_area_level_3
    )
    assert (
        results[2].get("administrative_area_level_2")
        == restaurants[2].administrative_area_level_2
    )
    assert (
        results[2].get("administrative_area_level_1")
        == restaurants[2].administrative_area_level_1
    )
    assert results[2].get("country") == restaurants[2].country
    assert results[2].get("postal_code") == restaurants[2].postal_code
    assert results[2].get("plus_code") == restaurants[2].plus_code
    assert results[2].get("latitude") == restaurants[2].latitude
    assert results[2].get("longitude") == restaurants[2].longitude
    assert results[2].get("viewport") == restaurants[2].viewport
    assert results[2].get("rating") == restaurants[2].rating
    assert results[2].get("google_maps_url") == restaurants[2].google_maps_url
    assert results[2].get("website_url") == restaurants[2].website_url
    assert results[2].get("utc_offset_minutes") == restaurants[2].utc_offset_minutes
    assert (
        results[2].get("adr_formatted_address") == restaurants[2].adr_formatted_address
    )
    assert results[2].get("business_status") == restaurants[2].business_status
    assert results[2].get("price_level") == restaurants[2].price_level
    assert results[2].get("user_rating_count") == restaurants[2].user_rating_count
    assert results[2].get("icon_mask_base_url") == restaurants[2].icon_mask_base_url
    assert (
        results[2].get("icon_background_color") == restaurants[2].icon_background_color
    )
    assert (
        results[2].get("primary_type_display_name")
        == restaurants[2].primary_type_display_name
    )
    assert results[2].get("takeout") == restaurants[2].takeout
    assert results[2].get("delivery") == restaurants[2].delivery
    assert results[2].get("dine_in") == restaurants[2].dine_in
    assert results[2].get("curbside_pickup") == restaurants[2].curbside_pickup
    assert results[2].get("reservable") == restaurants[2].reservable
    assert results[2].get("serves_lunch") == restaurants[2].serves_lunch
    assert results[2].get("serves_dinner") == restaurants[2].serves_dinner
    assert results[2].get("serves_beer") == restaurants[2].serves_beer
    assert results[2].get("serves_wine") == restaurants[2].serves_wine
    assert (
        results[2].get("serves_vegetarian_food")
        == restaurants[2].serves_vegetarian_food
    )
    assert results[2].get("primary_type") == restaurants[2].primary_type
    assert (
        results[2].get("short_formatted_address")
        == restaurants[2].short_formatted_address
    )

    # Test city with no recommendations
    data = {
        "city": "Munich",
    }
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        response.data.get("error")
        == "Sorry, we don't have any recommendations for you right now."
    )
