import object_tools
from django.contrib import messages
from django.contrib.admin.sites import site
import datetime

from django.shortcuts import render
from django.urls import reverse

from sugc.models import FeesInvoice, Flight
from sugc.tasks import calculate_invoices, get_flights


class Invoice(object_tools.ObjectTool):
    name = 'invoice'
    label = 'Run Invoices'

    def view(self, request, extra_content=None):
        modeladmin = site._registry.get(self.model)
        result = calculate_invoices()
        if result:
            messages.success(request, "Invoices updated")
        else:
            messages.info(request, "No new invoices")
        return modeladmin.changelist_view(request)


class GetFlights(object_tools.ObjectTool):
    name = 'get_flights'
    label = "Import Shalbourne Logs"

    def view(self, request, extra_context=None):
        modeladmin = site._registry.get(self.model)

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            get_flights(start_date, end_date)
        else:
            today = datetime.date.today()
            past_month_end_date = today.replace(day=1) - datetime.timedelta(days=1)
            past_month_start_date = past_month_end_date.replace(day=1)
            get_flights(past_month_start_date, past_month_end_date)
        messages.success(request, "Shalbourne Flights Imported")

        return modeladmin.changelist_view(request)


object_tools.tools.register(Invoice, model_class=FeesInvoice)
object_tools.tools.register(GetFlights, model_class=Flight)
