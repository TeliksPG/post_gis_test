from django.contrib.gis.db import models


class Place(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    geom = models.PointField(unique=True)

    def __str__(self):
        return self.name
