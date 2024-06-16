import json
import os

import requests

from apps.recommendations.models import Restaurant


class GooglePlacesAPI:
    """
    https://developers.google.com/maps/documentation/places/web-service/text-search

    Google Places API client to search for places using text queries.
    - Requires a Google Places API key to be set in the environment variables.
    - Provides a method to search for places using a text query.

    # Example usage 1:
    api = GooglePlacesAPI()
    query = "Recommended Restaurants with lunch available in Berlin, Germany with top rating"
    result = api.search_places(query)

    # Example usage 2:
    api = GooglePlacesAPI()
    query = "Spicy Vegetarian Food in Munich, Germany"
    api.bulk_create_or_update_restaurants(query)
    """

    BASE_URL = "https://places.googleapis.com/v1/places:searchText"
    GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

    def __init__(self):
        if not self.GOOGLE_PLACES_API_KEY:
            raise ValueError(
                "Google Places API key is not set in the environment variables."
            )

    def search_places(self, text_query):
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.GOOGLE_PLACES_API_KEY,
            "X-Goog-FieldMask": "*",
            # 'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel'
        }
        payload = {"textQuery": text_query}

        try:
            response = requests.post(self.BASE_URL, json=payload, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                return response.json()
            else:
                return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Google Places API: {e}")
            raise e
        except Exception as e:
            print(f"Some error occurred: {e}")
            raise e

    def map_to_restaurant(self, place_data):
        # Map Google Places API response
        return {
            "name": place_data.get("displayName", {}).get("text", ""),
            "google_place_name": place_data.get("name", ""),
            "google_place_id": place_data.get("id", ""),
            "types": place_data.get("types", []),
            "national_phone_number": place_data.get("nationalPhoneNumber", ""),
            "international_phone_number": place_data.get(
                "internationalPhoneNumber", ""
            ),
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
            "primary_type_display_name": place_data.get(
                "primaryTypeDisplayName", {}
            ).get("text", ""),
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

    def bulk_create_or_update_restaurants(self, query):
        response_data = self.search_places(query)
        places_ = response_data.get("places", [])
        for place_data in places_:
            print(f"Name: {place_data.get('displayName', {}).get('text')}")

            # Extract the Google Place ID
            google_place_id = place_data.get("placeId")

            # Prepare the defaults dictionary using your mapping function
            defaults = self.map_to_restaurant(place_data)

            # Check if restaurant with this Google Place ID already exists
            restaurant, created = Restaurant.objects.update_or_create(
                google_place_id=google_place_id,
                defaults=defaults,  # Ensure defaults is a dictionary
            )
