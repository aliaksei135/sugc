from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .validators import not_in_past_validator


class Availability(models.Model):
    date_added = models.DateTimeField(_("Time Added"), auto_now_add=True)
    date_available = models.DateField(_("Available"), blank=False, null=False, validators=[not_in_past_validator], )

    class Meta:
        verbose_name = _("Available Day")
        verbose_name_plural = _("Availability")


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    profile_img = models.FileField(upload_to='user_media', default='images/profile_default.jpg')

    is_solo = models.BooleanField(_("Solo?"), default=False)
    is_bronze = models.BooleanField(_("Bronze?"), default=False)
    is_xc = models.BooleanField(_("XC?"), default=False)

    availability = models.ManyToManyField(Availability, )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    class Meta:
        # permissions = [
        #     ('can_change_badges', 'Can change pilot badges')
        # ]
        pass
