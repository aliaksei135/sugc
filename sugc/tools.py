import object_tools
from django.contrib import messages
from django.contrib.admin.sites import site

from sugc.models import FeesInvoice
from sugc.tasks import calculate_invoices


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


object_tools.tools.register(Invoice, model_class=FeesInvoice)
