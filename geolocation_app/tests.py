from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from geolocation_app.models import Place
from geolocation_app.serializers import PlaceSerializer

import random
import uuid

PLACE_URL = reverse("geolocation_app:place-list")


def sample_place(**params):
    nums = random.randint(-99, 99)

    defaults = {
        "user": get_user_model().objects.create_user(
            f"{uuid.uuid4().hex[:10]}@gmail.com",
            "t1e2s3t4",
        ),
        "name": "Test",
        "description": "Test description",
        "geom": f"POINT({nums} {nums})"
    }
    defaults.update(params)
    return Place.objects.create(**defaults)


class UnauthenticatedPlaceApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required_create_location(self):
        res = self.client.post(PLACE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlaceApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "t1e2s3t4",
        )
        self.client.force_authenticate(self.user)

    def test_list_places(self):
        Place.objects.all().delete()

        sample_place()
        sample_place()

        res = self.client.get(PLACE_URL)

        places = Place.objects.all().order_by('-id')[:2]
        serializer = PlaceSerializer(places, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

        sorted_results = sorted(res.data['results'], key=lambda x: x['id'])
        sorted_serialized = sorted(serializer.data, key=lambda x: x['id'])

        self.assertEqual(sorted_results, sorted_serialized)

    def test_create_place(self):
        payload = {
            "name": "Test",
            "description": "Test description",
            "geom": "POINT (1 1)"
        }

        res = self.client.post(PLACE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        place = Place.objects.get(id=res.data['id'])
        for key in payload.keys():
            if key == "geom":
                expected = payload[key]
                actual = str(getattr(place, key)).split(';')[1].strip()
                self.assertEqual(expected, actual)
            else:
                self.assertEqual(payload[key], getattr(place, key))

    def test_place_filtered_by_name(self):

        place1 = sample_place(name="Test")
        place2 = sample_place(name="Test2")
        place3 = sample_place(name="Shop")

        res = self.client.get(PLACE_URL, {"name": "Test"})

        serializer1 = PlaceSerializer(place1)
        serializer2 = PlaceSerializer(place2)
        serializer3 = PlaceSerializer(place3)

        self.assertIn(serializer1.data, res.data['results'])
        self.assertIn(serializer2.data, res.data['results'])
        self.assertNotIn(serializer3.data, res.data['results'])

    def test_place_detail(self):
        place = sample_place()

        url = reverse("geolocation_app:place-detail", args=[place.id])
        res = self.client.get(url)

        serializer = PlaceSerializer(place)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
