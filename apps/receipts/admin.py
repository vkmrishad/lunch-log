from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.receipts.models import Receipt


class ReceiptAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "restaurant_name",
        "dated",
        "price",
        "city",
        "created_at",
        "updated_at",
    )
    list_filter = ("dated", "city", "postal_code", "country")
    search_fields = ("restaurant_name", "city", "postal_code", "country")


admin.site.register(Receipt, ReceiptAdmin)
