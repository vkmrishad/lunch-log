from rest_framework.serializers import ModelSerializer

from apps.receipts.models import Receipt
from apps.users.serializers import UserSerializer


class ReceiptSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested UserSerializer

    class Meta:
        model = Receipt
        fields = (
            "id",
            "user",
            "restaurant_name",
            "dated",
            "price",
            "image",
            "street",
            "city",
            "state",
            "country",
            "postal_code",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "created_at", "updated_at")

    def create(self, validated_data):
        # Ensure user field is not passed in the validated_data
        # Set the user as the logged-in user from the request context
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
