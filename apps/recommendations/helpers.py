from django.db.models import Q

from apps.recommendations.models import Restaurant


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
    if validated_data.get("street"):
        q_objects |= Q(street_number=validated_data["street"])

    if validated_data.get("city"):
        q_objects |= Q(city=validated_data["city"])

    if validated_data.get("state"):
        q_objects |= Q(administrative_area_level_1=validated_data["state"])

    if validated_data.get("country"):
        q_objects |= Q(country=validated_data["country"])

    if validated_data.get("postal_code"):
        q_objects |= Q(postal_code=validated_data["postal_code"])

    # Filter Restaurant queryset based on the constructed Q objects
    matching_restaurants = Restaurant.objects.filter(q_objects)
    if matching_restaurants.exists():
        return matching_restaurants
    else:
        return None
