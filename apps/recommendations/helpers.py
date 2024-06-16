import logging
from datetime import timedelta

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from apps.receipts.models import Receipt
from apps.recommendations.models import Restaurant
from apps.recommendations.utils import GooglePlacesAPI

logger = logging.getLogger(__name__)


def get_matching_restaurants(validated_data: dict) -> Restaurant or None:
    """
    This function takes in validated data and returns a queryset of restaurants that match the validated data.
    Search for restaurants that match the validated data, which is location information.
    :param validated_data:
    :return:
    """
    # Prepare Q objects for each field
    q_objects = Q()

    # Add conditions for each field if it exists in validated_data
    if street := validated_data.get("street"):
        q_objects |= Q(street__icontains=street)

    if city := validated_data.get("city"):
        q_objects |= Q(city__icontains=city)

    if state := validated_data.get("state"):
        q_objects |= Q(administrative_area_level_1__icontains=state)

    if country := validated_data.get("country"):
        q_objects |= Q(country__icontains=country)

    if postal_code := validated_data.get("postal_code"):
        q_objects |= Q(postal_code__icontains=postal_code)

    # Filter Restaurant queryset based on the constructed Q objects
    matching_restaurants = Restaurant.objects.filter(q_objects)
    if matching_restaurants.exists():
        return matching_restaurants
    else:
        return None


def map_to_restaurant(place_data: dict) -> dict:
    """
    This function maps the Google Places API response to the Restaurant model fields.
    :param place_data:
    :return:
    """
    # Map Google Places API response
    return {
        "name": place_data.get("displayName", {}).get("text", ""),
        "google_place_name": place_data.get("name", ""),
        "google_place_id": place_data.get("id", ""),
        "types": place_data.get("types", []),
        "national_phone_number": place_data.get("nationalPhoneNumber", ""),
        "international_phone_number": place_data.get("internationalPhoneNumber", ""),
        "formatted_address": place_data.get("formattedAddress", ""),
        "street_number": next(
            (
                comp["shortText"]
                for comp in place_data.get("addressComponents", [])
                if "street_number" in comp.get("types", [])
            ),
            "",
        ),
        "street": next(
            (
                comp["shortText"]
                for comp in place_data.get("addressComponents", [])
                if "route" in comp.get("types", [])
            ),
            "",
        ),
        "sublocality_level_1": next(
            (
                comp["shortText"]
                for comp in place_data.get("addressComponents", [])
                if "sublocality_level_1" in comp.get("types", [])
            ),
            "",
        ),
        "city": next(
            (
                comp["shortText"]
                for comp in place_data.get("addressComponents", [])
                if "locality" in comp.get("types", [])
            ),
            "",
        ),
        "administrative_area_level_3": next(
            (
                comp["shortText"]
                for comp in place_data.get("addressComponents", [])
                if "administrative_area_level_3" in comp.get("types", [])
            ),
            "",
        ),
        "administrative_area_level_2": next(
            (
                comp["shortText"]
                for comp in place_data.get("addressComponents", [])
                if "administrative_area_level_2" in comp.get("types", [])
            ),
            "",
        ),
        "administrative_area_level_1": next(
            (
                comp["shortText"]
                for comp in place_data.get("addressComponents", [])
                if "administrative_area_level_1" in comp.get("types", [])
            ),
            "",
        ),
        "country": next(
            (
                comp["shortText"]
                for comp in place_data.get("addressComponents", [])
                if "country" in comp.get("types", [])
            ),
            "",
        ),
        "postal_code": next(
            (
                comp["shortText"]
                for comp in place_data.get("addressComponents", [])
                if "postal_code" in comp.get("types", [])
            ),
            "",
        ),
        "plus_code": place_data.get("plusCode", {}),
        "latitude": place_data.get("location", {}).get("latitude", 0.0),
        "longitude": place_data.get("location", {}).get("longitude", 0.0),
        "viewport": place_data.get("viewport", {}),
        "rating": place_data.get("rating", 0.0),
        "google_maps_url": place_data.get("googleMapsUri", ""),
        "website_url": place_data.get("websiteUri", ""),
        "utc_offset_minutes": place_data.get("utcOffsetMinutes", 0),
        "adr_formatted_address": place_data.get("adrFormatAddress", ""),
        "business_status": place_data.get("businessStatus", ""),
        "price_level": place_data.get("priceLevel", ""),
        "user_rating_count": place_data.get("userRatingCount", 0),
        "icon_mask_base_url": place_data.get("iconMaskBaseUri", ""),
        "icon_background_color": place_data.get("iconBackgroundColor", ""),
        "primary_type_display_name": place_data.get("primaryTypeDisplayName", {}).get(
            "text", ""
        ),
        "takeout": place_data.get("takeout", False),
        "delivery": place_data.get("delivery", False),
        "dine_in": place_data.get("dineIn", False),
        "curbside_pickup": place_data.get("curbsidePickup", False),
        "reservable": place_data.get("reservable", False),
        "serves_lunch": place_data.get("servesLunch", False),
        "serves_dinner": place_data.get("servesDinner", False),
        "serves_beer": place_data.get("servesBeer", False),
        "serves_wine": place_data.get("servesWine", False),
        "serves_vegetarian_food": place_data.get("servesVegetarianFood", False),
        "primary_type": place_data.get("primaryType", ""),
        "short_formatted_address": place_data.get("shortFormattedAddress", ""),
    }


def create_or_update_restaurants(query_):
    """
    This function creates or updates restaurants based on the Google Places API response.
    :param query_:
    :return:
    """
    google_places_api = GooglePlacesAPI()
    response_data = google_places_api.search_places(query_)

    # Extract the places from the response data
    places_ = response_data.get("places", [])

    try:
        with transaction.atomic():
            for place_data in places_:
                logger.info(f"Adding restaurant: {place_data.get('displayName')}")

                # Extract the Google Place ID
                google_place_id = place_data.get("placeId")

                # Prepare the defaults dictionary using your mapping function
                defaults = map_to_restaurant(place_data)

                # Check if restaurant with this Google Place ID already exists
                restaurant, created = Restaurant.objects.update_or_create(
                    google_place_id=google_place_id,
                    defaults=defaults,  # Ensure defaults is a dictionary
                )
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise e


def update_restaurant_data_from_google_places():
    """
    This function updates restaurant data from Google Places API.
    First, it fetches all receipts with google_places_last_updated older than 14 days
    or have never been updated.
    Then, it creates or updates restaurants based on the query.
    It updates the Google Places last updated field in the receipt.
    :return:
    """

    # Get all receipts with google_places_last_updated older than 14 days or have never been updated
    receipts = Receipt.objects.filter(
        Q(google_places_last_updated__isnull=True)
        | Q(google_places_last_updated__lte=timezone.now() - timedelta(days=14))
    )

    if not receipts.exists():
        logger.info("No data needs to be fetched from Google Places API.")

    try:
        with transaction.atomic():
            for receipt in receipts:
                location = f"{receipt.street}, {receipt.city}, {receipt.country}, {receipt.postal_code}"
                query = f"Top rated restaurant at {location} serving lunch"

                logger.info(f"Fetching data for: {query}")

                # Create or update restaurants based on the query
                create_or_update_restaurants(query)

                receipt.google_places_last_updated = timezone.now()
                receipt.save()
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise e
