from django.contrib.auth import get_user_model, login
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.serializers import UserLoginSerializer, UserRegistrationSerializer

User = get_user_model()


class RegisterView(CreateAPIView):
    """
    User registration endpoint.
    """

    model = User
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    authentication_classes = []


class LoginView(APIView):
    """
    User login endpoint.
    - Used session based authentication.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        request=UserLoginSerializer,
        responses={200: "Login successful", 400: "Invalid credentials"},
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
