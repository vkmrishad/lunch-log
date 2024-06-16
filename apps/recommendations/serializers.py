from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.recommendations.models import Restaurant


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class RecommendationInputSerializer(Serializer):
    street = CharField(
        max_length=100,
        required=False,
        allow_null=True,
        help_text=_("Street address (e.g., 123 Main St)"),
    )
    city = CharField(
        max_length=100,
        help_text=_("City name"),
    )
    state = CharField(
        max_length=100,
        required=False,
        allow_null=True,
        help_text=_("State or province name (if applicable)"),
    )
    country = CharField(
        max_length=100,
        required=False,
        allow_null=True,
        help_text=_("Country name"),
    )
    postal_code = CharField(
        max_length=20,
        required=False,
        allow_null=True,
        help_text=_("Postal code or ZIP code"),
    )
