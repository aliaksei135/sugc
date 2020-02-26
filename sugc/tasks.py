import datetime

from django.contrib.auth import get_user_model
from django.db.models import Count

from config import celery_app
from sugc.models import Flight, FeesInvoice, FlyingList

user_model = get_user_model()


@celery_app.task(name="Daily Invoice Calculation")
def calculate_invoices():
    flight_dates = Flight.objects.filter(invoiced_for=False).dates('date')
    for date in flight_dates:
        members_on_date = Flight.objects.filter(date=date).distinct('member').only('member')
        for member in members_on_date:
            fees = Flight.objects.get_fees_by_date(member, date)
            FeesInvoice.objects.create(date=date, member=member, balance=fees).save()


@celery_app.task(name="Make flying list")
def make_flying_list(weekday=(5, 6), spaces=(5, 5)):
    today = datetime.date.today().weekday()
    weekday_dates = [datetime.date.today() + datetime.timedelta(days=w - today, weeks=1) for w in weekday]
    for date, day_spaces in zip(weekday_dates, spaces):
        applicants = user_model.objects.filter(availability__date_available=date) \
            .annotate(unpaid_invoice_count=Count('invoices')) \
            .filter(unpaid_invoice_count__lte=3) \
            .order_by('availability__date_added')
        driver = applicants.filter(is_driver=True).first()
        selected_applicants = applicants[:day_spaces - 2]
        send_flying_emails(driver, selected_applicants)
        list, success = FlyingList.objects.get_or_create(date=date, driver=driver)
        if success:
            list.members.add(selected_applicants)


def send_flying_emails(driver, passengers):
    pass
