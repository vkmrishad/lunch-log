from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.receipts.filters import ReceiptFilter
from apps.receipts.models import Receipt
from apps.receipts.permissions import IsOwnerOnly
from apps.receipts.serializers import ReceiptSerializer


class ReceiptViewSet(ModelViewSet):
    """
    API endpoint that allows receipts to be created, viewed, updated, and deleted.
    """

    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated, IsOwnerOnly]
    allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReceiptFilter

    def get_queryset(self):
        # Return only the receipts of the logged-in user and user specific receipts
        return self.queryset.filter(user=self.request.user)
