from django.urls import path

from apps.auth.views import LoginView, RegisterView

urlpatterns = [
    path(r"signup/", RegisterView.as_view(), name="signup"),
    path(r"login/", LoginView.as_view(), name="login"),
]
