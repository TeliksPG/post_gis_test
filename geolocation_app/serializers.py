from rest_framework import serializers
from .models import Place
from .tele_bot import bot_notification


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "user", "name", "description", "geom"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        user = self.context["request"].user
        name = validated_data.get("name")
        description = validated_data.get("description")
        geom = validated_data.get("geom")

        bot_notification(user, name, geom, description)

        place = Place(user=user, **validated_data)
        place.save()

        return place
