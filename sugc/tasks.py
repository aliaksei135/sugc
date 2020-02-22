from django.contrib.auth import get_user_model

from config import celery_app
from sugc.models import Flight, FeesInvoice

user_model = get_user_model()


@celery_app.task(name="Daily Invoice Calculation")
def calculate_invoices():
    flight_dates = Flight.objects.filter(invoiced_for=False).dates('date')
    for date in flight_dates:
        members_on_date = Flight.objects.filter(date=date).distinct('member').only('member')
        for member in members_on_date:
            fees = Flight.objects.get_fees_by_date(member, date)
            FeesInvoice.objects.create(date=date, member=member, balance=fees).save()
