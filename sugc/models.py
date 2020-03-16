from decimal import Decimal, ROUND_UP

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from sugc.validators import not_in_past_validator

user_model = get_user_model()


class FlightModelManager(models.Manager):

    def get_flights_by_date(self, user, date):
        return self.filter(member=user, date=date)

    def get_fees_by_date(self, user, date):
        flights = self.get_flights_by_date(user, date)
        fee_model = GlidingFeePeriod.objects.get_fee_model_for_date(date)
        days_fee = 0.0
        for f in flights:

            if f.is_real_launch_failure:
                continue

            if user.age < fee_model.std_age:
                # Is a junior
                if f.is_train_launch_failure:
                    days_fee += fee_model.junior_subs_tlf_cost
                else:
                    if f.duration <= fee_model.junior_subs_mins:
                        subsidised_minutes = f.duration
                        unsubsidised_minutes = 0
                    else:
                        subsidised_minutes = fee_model.junior_subs_mins
                        unsubsidised_minutes = f.duration - fee_model.junior_subs_mins
                    days_fee += (
                        fee_model.junior_subs_launch_cost + subsidised_minutes * fee_model.junior_subs_minute_cost
                        + unsubsidised_minutes * fee_model.junior_minute_cost)
            else:
                # Not a junior
                if f.is_train_launch_failure:
                    days_fee += fee_model.std_subs_tlf_cost
                else:
                    if f.duration <= fee_model.std_subs_mins:
                        subsidised_minutes = f.duration
                        unsubsidised_minutes = 0
                    else:
                        subsidised_minutes = fee_model.std_subs_mins
                        unsubsidised_minutes = f.duration - fee_model.std_subs_mins
                    days_fee += (
                        fee_model.std_subs_launch_cost + subsidised_minutes * fee_model.std_subs_minute_cost
                        + unsubsidised_minutes * fee_model.std_minute_cost)

            f.invoiced_for = True
            f.save()

        return Decimal(days_fee).quantize(Decimal('.01'), rounding=ROUND_UP)


class FeesModelManager(models.Manager):

    def get_fee_model_for_date(self, date):
        # Most recent fee model that is before the given date
        # model objects are sorted into descending date_effective_from order
        return self.filter(date_effective_from__lte=date).last()


class FeesInvoice(models.Model):
    date = models.DateField(_("Flying Date"), blank=False, null=False)
    balance = models.FloatField(_("Flying Fees Due"), blank=False, null=False, default=0.0)
    paid = models.BooleanField(_("Paid"), null=False, default=False)

    member = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name='invoices')

    def __str__(self):
        return self.date.strftime('%d/%m/%Y') + ' ' + self.member.name

    class Meta:
        ordering = ['-date']


class GlidingFeePeriod(models.Model):
    objects = FeesModelManager()

    date_effective_from = models.DateField(_("Date Fees effective from"), blank=False, null=False)

    junior_launch_cost = models.FloatField(_("Juniors' Actual Launch Cost"), blank=False, null=False)
    junior_tlf_cost = models.FloatField(_("Juniors' Actual TLF Cost"), blank=False, null=False)
    junior_minute_cost = models.FloatField(_("Juniors' Actual Minute Cost"), null=False, blank=False)
    junior_subs_mins = models.IntegerField(_("Juniors' Subsidised Amount of Minutes"), null=False, blank=False)
    junior_subs_launch_cost = models.FloatField(_("Juniors' Subsidised Launch Cost"), blank=False, null=False)
    junior_subs_tlf_cost = models.FloatField(_("Juniors' Subsidised TLF Cost"), blank=False, null=False)
    junior_subs_minute_cost = models.FloatField(_("Juniors' Subsidised Minute Cost"), null=False, blank=False)

    std_launch_cost = models.FloatField(_("Standard Actual Launch Cost"), blank=False, null=False)
    std_tlf_cost = models.FloatField(_("Standard Actual TLF Cost"), blank=False, null=False)
    std_minute_cost = models.FloatField(_("Standard Actual Minute Cost"), null=False, blank=False)
    std_subs_mins = models.IntegerField(_("Standard Subsidised Amount of Minutes"), null=False, blank=False)
    std_subs_launch_cost = models.FloatField(_("Standard Subsidised Launch Cost"), blank=False, null=False)
    std_subs_tlf_cost = models.FloatField(_("Standard Subsidised TLF Cost"), blank=False, null=False)
    std_subs_minute_cost = models.FloatField(_("Standard Subsidised Minute Cost"), null=False, blank=False)

    std_age = models.IntegerField(_("Age from which to charge standard fees"), blank=False, null=False, default=26)

    def __str__(self):
        return "Fees from " + self.date_effective_from.strftime('%d/%m/%Y')

    class Meta:
        ordering = ['-date_effective_from']


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
    objects = FlightModelManager()

    date = models.DateField(_("Flight Date"), null=False, blank=False)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)

    member = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name='flights')

    capacity = models.CharField(_("Pilot Capacity"), choices=PILOT_CAPACITY_CHOICES, default='P2', max_length=32)
    duration = models.IntegerField(_("Flight Duration [mins]"), null=False, blank=False)
    is_train_launch_failure = models.BooleanField(_("TLF?"), default=False)
    is_real_launch_failure = models.BooleanField(_("RLF?"), default=False)

    invoiced_for = models.BooleanField(_("Invoiced For"), editable=False, null=False, default=False)

    def __str__(self):
        return str(self.aircraft.registration) + ' ' + str(self.member.name) + ' ' + str(self.date)

    class Meta:
        ordering = ['date']


class FlyingList(models.Model):
    date = models.DateField(_("Flying List Date"), blank=False, null=False, unique=True)
    driver = models.ForeignKey(user_model, on_delete=models.CASCADE)
    members = models.ManyToManyField(user_model, related_name='flyinglists')

    def __str__(self):
        return str(self.date) + ' List'

    class Meta:
        ordering = ['date']


class Availability(models.Model):
    date_added = models.DateTimeField(_("Time Added"), auto_now_add=True)
    date_available = models.DateField(_("Available"), blank=False, null=False, validators=[not_in_past_validator])

    member = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name='availability')

    class Meta:
        verbose_name = _("Available Day")
        verbose_name_plural = _("Availability")
