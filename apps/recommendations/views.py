from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.recommendations.helpers import get_matching_restaurants
from apps.recommendations.serializers import (
    RecommendationInputSerializer,
    RestaurantSerializer,
)


class RecommendationView(APIView):
    @extend_schema(
        request=RecommendationInputSerializer,
        responses={
            200: RestaurantSerializer(many=True),
            404: "Sorry, we don't have any recommendations for you right now.",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = RecommendationInputSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            matching_restaurants = get_matching_restaurants(validated_data)

            if matching_restaurants is not None:
                serializer = RestaurantSerializer(matching_restaurants, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "error": "Sorry, we don't have any recommendations for you right now."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
