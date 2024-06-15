from django_filters import FilterSet, NumberFilter

from apps.receipts.models import Receipt


class ReceiptFilter(FilterSet):
    day = NumberFilter(field_name="dated__day", help_text="Filter by day")
    month = NumberFilter(
        field_name="dated__month", help_text="Filter by month, Use numbers 1-12"
    )
    year = NumberFilter(field_name="dated__year", help_text="Filter by year")

    class Meta:
        model = Receipt
        fields = ("day", "month", "year")
