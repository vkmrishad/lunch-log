from django.urls import include, path
from rest_framework import routers

from apps.receipts.views import ReceiptViewSet

router = routers.DefaultRouter()
router.register("", ReceiptViewSet, basename="receipts")

urlpatterns = [
    path("", include(router.urls)),
]
