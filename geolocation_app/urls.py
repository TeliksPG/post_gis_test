from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet, NearestPlaceView

router = DefaultRouter()
router.register("places", PlaceViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("nearest_place/", NearestPlaceView.as_view(), name="nearest_place"),
]

app_name = "geolocation_app"
