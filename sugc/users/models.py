import datetime
from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .validators import not_in_past_validator


class Availability(models.Model):
    date_added = models.DateTimeField(_("Time Added"), auto_now_add=True)
    date_available = models.DateField(_("Available"), blank=False, null=False, validators=[not_in_past_validator],
                                      unique=True)

    class Meta:
        verbose_name = _("Available Day")
        verbose_name_plural = _("Availability")


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    profile_img = models.ImageField(upload_to='user_media/', default='images/profile_default.jpg')
    date_of_birth = models.DateField(_("Date of Birth"), null=False, blank=False, default=datetime.date.today)

    on_waiting_list = models.BooleanField(_("On Waiting List?"), default=True)
    has_susu_membership = models.BooleanField(_("Has SUSU Membership?"), default=False)

    is_solo = models.BooleanField(_("Solo?"), default=False)
    is_bronze = models.BooleanField(_("Bronze?"), default=False)
    is_xc = models.BooleanField(_("XC?"), default=False)

    availability = models.ManyToManyField(Availability, )

    # balance = models.FloatField(_("Account Balance"), null=False, blank=False, default=0.0, editable=False)

    @property
    def balance(self):
        unpaid_invoices = self.unpaid_invoices()
        balance = 0.0
        for i in unpaid_invoices:
            balance += i.invoice_balance
        return balance

    @property
    def waiting_list_position(self):
        '''Returns waiting list position on first-come-first-serve basis'''
        return 0

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - \
               ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def unpaid_invoices(self):
        return self.invoices.filter(paid=False)
