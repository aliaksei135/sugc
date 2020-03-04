import django_tables2 as tables

from sugc.models import Flight


class FlightTable(tables.Table):
    class Meta:
        model = Flight
        template_name = "django_tables2/bootstrap4.html"
        fields = ['date', 'aircraft', 'duration', 'capacity', 'is_train_launch_failure', 'is_real_launch_failure']
