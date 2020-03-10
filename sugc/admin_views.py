import datetime

from django import views
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import render

from sugc.admin_tables import FlyingListDriversTable, FlyingListMembersTable
from sugc.forms import FlyingListCreationForm
from sugc.models import FlyingList

User = get_user_model()


class FlyingListView(views.generic.CreateView):
    model = FlyingList
    template_name = 'admin/sugc/flying.html'
    form_class = FlyingListCreationForm

    def get_context_data(self, **kwargs):
        context = super(FlyingListView, self).get_context_data(**kwargs)
        context['drivers_table'] = FlyingListDriversTable(User.objects.none())
        context['members_table'] = FlyingListMembersTable(User.objects.none())
        return context


# Use AJAX to load drivers on a given day
def load_available_drivers(request):
    date = datetime.datetime.strptime(request.GET.get('date'), '%d/%m/%Y')
    available = User.objects.filter(availability__date_available=date) \
        .annotate(unpaid_invoice_count=Count('invoices')) \
        .filter(unpaid_invoice_count__lte=3) \
        .order_by('availability__date_added')
    drivers = available.filter(is_driver=True)
    return render(request, 'admin/sugc/table_row.html', {'users': drivers, 'group': 'drivers', 'input_type': 'radio'})


def load_available_members(request):
    date = datetime.datetime.strptime(request.GET.get('date'), '%d/%m/%Y')
    available = User.objects.filter(availability__date_available=date) \
        .annotate(unpaid_invoice_count=Count('invoices')) \
        .filter(unpaid_invoice_count__lte=3) \
        .order_by('availability__date_added')
    return render(request, 'admin/sugc/table_row.html',
                  {'users': available, 'group': 'members', 'input_type': 'checkbox'})
