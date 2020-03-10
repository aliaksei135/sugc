import django_tables2 as tables
from django.utils.translation import ugettext_lazy as _


class FlyingListDriversTable(tables.Table):
    name = tables.Column(_("Name"))
    solo = tables.BooleanColumn(_("Solo"))
    last_flight_date = tables.DateColumn(_("Last Flight"))
    unpaid_invoices = tables.Column(_("# Unpaid invoices"))
    selected = tables.Column(_("Selected"))

    class Meta:
        attrs = {'id': 'driversTable'}


class FlyingListMembersTable(tables.Table):
    name = tables.Column(_("Name"))
    solo = tables.BooleanColumn(_("Solo"))
    last_flight_date = tables.DateColumn(_("Last Flight"))
    unpaid_invoices = tables.Column(_("# Unpaid invoices"))
    selected = tables.Column(_("Selected"))

    class Meta:
        attrs = {'id': 'membersTable'}
