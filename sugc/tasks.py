import datetime

from django.contrib.auth import get_user_model
from django.db.models import Count
from templated_email import send_templated_mail, InlineImage

from config import celery_app
from sugc.models import Flight, FlyingList, Aircraft

user_model = get_user_model()


@celery_app.task(name='Get Flights')
def get_flights(start_date: datetime.date, end_date: datetime.date):
    import requests
    from lxml import etree
    flog = requests.get(
        f'https://shalbournegliding.co.uk/members/Flightlogs/PilotLog.php?startdate={start_date.strftime("%Y-%m-%d")}&name=%&enddate={end_date.strftime("%Y-%m-%d")}')
    tree = etree.HTML(flog.text).find("body/table")
    rows = iter(tree)
    headers = [col.text for col in next(rows)]
    for row in rows:
        vals = [col.text for col in row]
        if vals[3].strip():
            crew_cap = 'P2'
            name = vals[3]
        else:
            crew_cap = 'P1'
            name = vals[2]

        is_tlf = 'train launch failure' in vals[7].lower()
        if not is_tlf:
            is_rlf = 'launch failure' in vals[7].lower()
        else:
            is_rlf = False

        first_name = name.strip().split(' ')[0]
        last_name = ' '.join(name.strip().split(' ')[1:])

        member_qs = user_model.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name)
        if not member_qs:
            # Probably not an SUGC member, skip
            continue

        member = member_qs.first()

        aircraft_qs = Aircraft.objects.filter(registration__icontains=vals[4].strip())
        if not aircraft_qs:
            # Cannot find aircraft, assume it is private third party
            continue
        aircraft = aircraft_qs.first()

        flight_date = datetime.datetime.strptime(vals[1].strip(), "%Y-%m-%d").date()

        duration_time = datetime.datetime.strptime(vals[6].strip(), "%H:%M:%S")
        duration_delta = datetime.timedelta(hours=duration_time.hour,
                                            minutes=duration_time.minute,
                                            seconds=duration_time.second)

        import_hash = hash(
            (
                vals[0],
                flight_date,
                member.pk,
                aircraft.pk,
                crew_cap,
                duration_delta,
                is_tlf,
                is_rlf
            )
        )

        similar_flights = Flight.objects.filter(import_hash=import_hash, date__exact=flight_date)

        if not similar_flights:
            flight_model = Flight.objects.create(date=flight_date,
                                                 member_id=member.pk,
                                                 aircraft_id=aircraft.pk,
                                                 capacity=crew_cap,
                                                 duration=duration_delta,
                                                 is_train_launch_failure=is_tlf,
                                                 is_real_launch_failure=is_rlf,
                                                 import_hash=import_hash)
            flight_model.save()


@celery_app.task(name="Daily Invoice Calculation")
def calculate_invoices():
    flight_dates = Flight.objects.filter(invoice__isnull=True).dates('date', 'day')
    if not flight_dates:
        return False

    for date in flight_dates:
        member_ids_on_date = Flight.objects.filter(date=date).values_list('member', flat=True).distinct()
        for member_id in member_ids_on_date:
            member = user_model.objects.get(id=member_id)
            Flight.objects.make_invoice_by_date(member, date)

    return True


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
        flying_list, success = FlyingList.objects.get_or_create(date=date, driver=driver)
        if success:
            flying_list.members.add(selected_applicants)
            send_flying_emails(flying_list)


@celery_app.task(name='Database Backup')
def db_backup():
    from django.core.management import call_command
    call_command('dbbackup')


def send_flying_emails(flying_list: FlyingList):
    prev = flying_list.date - datetime.timedelta(days=1)
    t = datetime.time(hour=12, minute=0)
    deadline = datetime.datetime.combine(prev, t).strftime('%H:%M %A %d %b')
    flying_date = flying_list.date.strftime('%A %d %b')

    dcontext = {
        'flying_date': flying_date,
        'driver': flying_list.driver,
        'deadline': deadline,
    }

    if flying_list.members.all():
        dcontext['members'] = flying_list.members.all()

        for member in flying_list.members.all():
            send_templated_mail(
                template_name='flying_list_member',
                from_email='flying@sugc.net',
                recipient_list=[member.email],
                context={
                    'flying_date': flying_date,
                    'driver': flying_list.driver,
                    'member': member,
                    'deadline': deadline,
                }
            )

    send_templated_mail(
        template_name='flying_list_driver',
        from_email='flying@sugc.net',
        recipient_list=[flying_list.driver.email],
        context=dcontext,
    )
