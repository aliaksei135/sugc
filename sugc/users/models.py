import datetime
from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    profile_img = models.ImageField(upload_to='user_media/', default='images/profile_default.jpg')
    date_of_birth = models.DateField(_("Date of Birth"), null=False, blank=False, default=datetime.date.today)
    is_driver = models.BooleanField(_("Is driver?"), default=False)

    on_waiting_list = models.BooleanField(_("On Waiting List?"), default=True)
    has_susu_membership = models.BooleanField(_("Has SUSU Membership?"), default=False)
    student_id = models.IntegerField(_("Student ID Number"), null=True, blank=True)
    phone_number = models.IntegerField(_("Phone Number"), null=True, blank=False)

    is_alumni = models.BooleanField(_("Alumni?"), default=False, null=False, blank=False)
    is_third_party = models.BooleanField(_("Third Party?"), default=False, null=False, blank=False)

    is_solo = models.BooleanField(_("Solo?"), default=False)
    is_bronze = models.BooleanField(_("Bronze?"), default=False)
    is_xc = models.BooleanField(_("XC?"), default=False)

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def balance(self):
        unpaid_invoices = self.unpaid_invoices()
        balance = 0.0
        for i in unpaid_invoices:
            balance += i.invoice_balance
        return balance

    @property
    def waiting_list_position(self):
        if self.on_waiting_list:
            waited_users = list(User.objects.filter(on_waiting_list=True).order_by('date_joined'))
            num_waited = len(waited_users)
            pos = waited_users.index(self) + 1
            return [pos, num_waited, num_waited - pos + 1]
        else:
            return 0

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - \
               ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))  # noqa E127

    @property
    def last_flight_date(self):
        return self.flights.latest('date').date

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def unpaid_invoices(self):
        return self.invoices.filter(paid=False)

    def __str__(self):
        return self.name
