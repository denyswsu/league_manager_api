from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Taxi(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
