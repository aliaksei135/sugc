import datetime

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import CreateView

import sugc.admin
from sugc.admin_forms import FlyingListCreationForm
from sugc.admin_tables import FlyingListDriversTable, FlyingListMembersTable
from sugc.models import FlyingList

User = get_user_model()


class FlyingListView(CreateView):
    model = FlyingList
    template_name = 'admin/sugc/flying.html'
    form_class = FlyingListCreationForm
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super(FlyingListView, self).get_context_data(**kwargs)
        context['drivers_table'] = FlyingListDriversTable(User.objects.none())
        context['members_table'] = FlyingListMembersTable(User.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        response = super(FlyingListView, self).post(request, *args, **kwargs)
        if '_saveandemail' in request.POST:
            sugc.admin.email_flying_list(None, request, [self.object])
        return response


# Use AJAX to load drivers on a given day
def load_available_drivers(request):
    date = datetime.datetime.strptime(request.GET.get('date'), '%d/%m/%Y')
    available = User.objects.filter(availability__date_available=date) \
        .annotate(unpaid_invoice_count=Count('invoices')) \
        .order_by('availability__date_added')
    drivers = available.filter(is_driver=True)
    return render(request, 'admin/sugc/table_row.html', {'users': drivers, 'group': 'driver', 'input_type': 'radio'})


def load_available_members(request):
    date = datetime.datetime.strptime(request.GET.get('date'), '%d/%m/%Y')
    available = User.objects.filter(availability__date_available=date) \
        .annotate(unpaid_invoice_count=Count('invoices')) \
        .order_by('availability__date_added')
    return render(request, 'admin/sugc/table_row.html',
                  {'users': available, 'group': 'members', 'input_type': 'checkbox'})
