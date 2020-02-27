from django import views
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import render

from sugc.forms import FlyingListCreationForm
from sugc.models import FlyingList

User = get_user_model()


class FlyingListView(views.generic.CreateView):
    model = FlyingList
    template_name = 'admin/sugc/flying.html'
    form_class = FlyingListCreationForm


# Has to be a prettier way of doing this

# Use AJAX to load drivers on a given day
def load_available_drivers(request):
    date = request.GET.get('date')
    available = User.objects.filter(availability__date_available=date) \
        .annotate(unpaid_invoice_count=Count('invoices')) \
        .filter(unpaid_invoice_count__lte=3) \
        .order_by('availability__date_added')
    drivers = available.filter(is_driver=True)
    return render(request, 'admin/sugc/driver_dropdown_list.html', {'drivers': drivers})


# Use AJAX to load members on a given day
def load_available_members(request):
    date = request.GET.get('date')
    available = User.objects.filter(availability__date_available=date) \
        .annotate(unpaid_invoice_count=Count('invoices')) \
        .filter(unpaid_invoice_count__lte=3) \
        .order_by('availability__date_added')
    members = available.filter(is_driver=False)
    return render(request, 'admin/sugc/member_dropdown_list.html', {'members': members})
