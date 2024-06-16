from django.db.models import (
    BooleanField,
    CharField,
    FloatField,
    IntegerField,
    JSONField,
    URLField,
)
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Restaurant(BaseModel):
    name = CharField(_("name"), max_length=255)
    google_place_name = CharField(_("Google place name"), max_length=255)
    google_place_id = CharField(_("Google place ID"), max_length=50)
    types = JSONField(_("types"))
    national_phone_number = CharField(_("national phone number"), max_length=20)
    international_phone_number = CharField(
        _("international phone number"), max_length=20
    )
    formatted_address = CharField(_("formatted address"), max_length=255)
    street_number = CharField(_("street number"), max_length=10)
    street = CharField(_("street"), max_length=255)
    sublocality_level_1 = CharField(_("sublocality level 1"), max_length=255)
    city = CharField(_("city"), max_length=255)
    administrative_area_level_3 = CharField(
        _("administrative area level 3"), max_length=255
    )
    administrative_area_level_2 = CharField(
        _("administrative area level 2"), max_length=255
    )
    administrative_area_level_1 = CharField(
        _("administrative area level 1"), max_length=255
    )
    country = CharField(_("country"), max_length=255)
    postal_code = CharField(_("postal code"), max_length=20)
    plus_code = JSONField(_("plus code"))
    latitude = FloatField(_("latitude"))
    longitude = FloatField(_("longitude"))
    viewport = JSONField(_("viewport"))
    rating = FloatField(_("rating"))
    google_maps_url = URLField(_("Google maps URL"))
    website_url = URLField(_("website URL"))
    utc_offset_minutes = IntegerField(_("UTC offset minutes"))
    adr_formatted_address = CharField(_("ADR formatted address"), max_length=255)
    business_status = CharField(_("business status"), max_length=50)
    price_level = CharField(_("price level"), max_length=50)
    user_rating_count = IntegerField(_("user rating count"))
    icon_mask_base_url = URLField(_("icon mask base URL"))
    icon_background_color = CharField(_("icon background color"), max_length=7)
    primary_type_display_name = CharField(
        _("primary type display name"), max_length=255
    )
    takeout = BooleanField(_("takeout"))
    delivery = BooleanField(_("delivery"))
    dine_in = BooleanField(_("dine-in"))
    curbside_pickup = BooleanField(_("curbside pickup"))
    reservable = BooleanField(_("reservable"))
    serves_lunch = BooleanField(_("serves lunch"))
    serves_dinner = BooleanField(_("serves dinner"))
    serves_beer = BooleanField(_("serves beer"))
    serves_wine = BooleanField(_("serves wine"))
    serves_vegetarian_food = BooleanField(_("serves vegetarian food"))
    primary_type = CharField(_("primary type"), max_length=255)
    short_formatted_address = CharField(_("short formatted address"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
        verbose_name = _("restaurant")
        verbose_name_plural = _("restaurants")
