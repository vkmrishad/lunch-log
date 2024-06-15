from django.urls import include, path
from rest_framework import routers

from apps.receipts.views import ReceiptViewSet

router = routers.DefaultRouter()
router.register("", ReceiptViewSet)

urlpatterns = [
    path("", include(router.urls)),
]