from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Place
from .serializers import PlaceSerializer
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import fromstr
from rest_framework.pagination import PageNumberPagination


class PlacePagination(PageNumberPagination):
    page_size = 5
    max_page_size = 20


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    pagination_class = PlacePagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the place with name"""
        name = self.request.query_params.get("name")
        users = self.request.query_params.get("user")

        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        if users:
            users_ids = self._params_to_ints(users)
            queryset = queryset.filter(user__id__in=users_ids)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type={"type": "string"},
                description="Filter by name (ex. ?name=shop)",
            ),
            OpenApiParameter(
                "users",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by user (ex. ?user=1,4)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# for documentation
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="lat",
            type=OpenApiTypes.NUMBER,
            description="The latitude coordinate for finding the nearest place.",
            required=True,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="lon",
            type=OpenApiTypes.NUMBER,
            description="The longitude coordinate for finding the nearest place.",
            required=True,
            location=OpenApiParameter.QUERY,
        ),
    ],
)
class NearestPlaceView(generics.RetrieveAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_object(self):
        lat = self.request.query_params.get("lat", None)
        lon = self.request.query_params.get("lon", None)
        if lat is not None and lon is not None:
            pnt = fromstr(f"POINT({lat} {lon})", srid=4326)
            return (
                self.get_queryset()
                .annotate(distance=Distance("geom", pnt))
                .order_by("distance")
                .first()
            )
        else:
            return None
