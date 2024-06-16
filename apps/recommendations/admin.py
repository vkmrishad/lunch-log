from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.recommendations.models import Restaurant


class RestaurantAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "rating",
        "street",
        "city",
        "postal_code",
        "created_at",
        "updated_at",
    )


admin.site.register(Restaurant, RestaurantAdmin)
