from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

User = get_user_model()


class UserRegistrationSerializer(ModelSerializer):
    password = CharField(write_only=True)
    first_name = CharField(required=True)
    last_name = CharField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")

    @atomic
    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data["email"].lower(),
                email=validated_data["email"].lower(),
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                password=validated_data["password"],
            )
            validate_password(validated_data["password"], user=user)
            return user
        except Exception as e:
            error_message = {"error": "Something went wrong!"}
            status_code = HTTP_500_INTERNAL_SERVER_ERROR

            # If password validation error
            if e.args:
                error_message = {
                    "password": [str(error) for arg in e.args[0] for error in arg]
                }
                status_code = HTTP_400_BAD_REQUEST

            raise ValidationError(error_message, status_code)


class UserLoginSerializer(Serializer):
    email = CharField()
    password = CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            data["user"] = user
        else:
            raise ValidationError("Invalid credentials")
        return data
