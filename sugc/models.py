from django.db import models


class Aircraft(models.Model):
    registration = models.CharField("Registration", max_length=5, unique=True, blank=False, null=False)
    type = models.CharField("Aircraft Type", max_length=255, )
    is_club_aircraft = models.BooleanField("Our Aircraft?", blank=False, null=False)

    class Meta:
        ordering = ["registration"]


class Flight(models.Model):
    date = models.DateField("Flight Date", null=False, blank=False)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
