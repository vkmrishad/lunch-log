from django.urls import path

from apps.recommendations.views import RecommendationView

urlpatterns = [
    path(r"", RecommendationView.as_view(), name="recommendations"),
]
