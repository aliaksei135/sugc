from django.db import models
from django.utils.translation import ugettext_lazy as _

from sugc.users.models import User


class Aircraft(models.Model):
    registration = models.CharField(_("Registration"), max_length=5, unique=True, blank=False, null=False)
    type = models.CharField(_("Aircraft Type"), max_length=255, )
    is_club_aircraft = models.BooleanField(_("Our Aircraft?"), blank=False, null=False)

    def __str__(self):
        return self.registration

    class Meta:
        ordering = ["registration"]


class Flight(models.Model):
    PILOT_CAPACITY_CHOICES = [('P1', _('P1')), ('P2', _('P2')), ('EX', _('Examiner')), ('INS', _('Instructor'))]

    date = models.DateField(_("Flight Date"), null=False, blank=False)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)

    member = models.ForeignKey(User, on_delete=models.CASCADE)

    capacity = models.CharField(_("Pilot Capacity"), choices=PILOT_CAPACITY_CHOICES, default='P2', max_length=32)
    duration = models.IntegerField(_("Flight Duration"), null=False, blank=False)
    is_launch_failure = models.BooleanField(_("Is Launch Fail?"), default=False)

    def __str__(self):
        return str(self.aircraft.registration) + ' ' + str(self.member.name) + ' ' + str(self.date)

    class Meta:
        ordering = ['date']
