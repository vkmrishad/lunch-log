from django.contrib.auth import get_user_model, login, logout
from django.middleware.csrf import get_token
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

            # Get CSRF token
            csrf_token = get_token(request)

            # Get session ID
            session_id = request.session.session_key

            return Response(
                {
                    "message": "Login successful",
                    "csrf_token": csrf_token,
                    "session_id": session_id,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    User logout endpoint.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        # Logout the user from session (if using session authentication)
        logout(request)

        # Logout the user from token authentication (if using token authentication)
        try:
            request.user.auth_token.delete()
        except Exception:
            pass

        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
