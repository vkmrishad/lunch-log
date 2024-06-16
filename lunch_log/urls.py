"""
URL configuration for lunch_log project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

api_v1 = "api/v1"

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path(f"{api_v1}/auth/", include("apps.auth.urls")),
        path(f"{api_v1}/receipts/", include("apps.receipts.urls")),
        path(f"{api_v1}/recommendations/", include("apps.recommendations.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

# Swagger
if settings.DEBUG:
    urlpatterns += [
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/swagger/",
            SpectacularSwaggerView.as_view(
                url="/schema/?format=json", url_name="schema"
            ),
            name="swagger-ui",
        ),
        path(
            "api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
        ),
    ]
