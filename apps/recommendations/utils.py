import json
import logging
import os

import requests

logger = logging.getLogger(__name__)


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
    result = api.search_places(query)
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
            logger.error(f"Error fetching data from Google Places API: {e}")
            raise e
        except Exception as e:
            logger.error(f"Some error occurred: {e}")
            raise e
