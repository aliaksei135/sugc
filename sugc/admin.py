from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path

from sugc.admin_views import load_available_members, FlyingListView
from sugc.models import FeesInvoice, Flight, FlyingList, Aircraft, GlidingFeePeriod

admin.site.register(Aircraft)
admin.site.register(GlidingFeePeriod)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['date', 'member', 'aircraft', 'capacity']
    ordering = ['-date']
    search_fields = ['aircraft', 'date']


@admin.register(FeesInvoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['date', 'member', 'balance', 'paid']
    list_filter = ['paid']
    ordering = ['-date']
    search_fields = ['member']


@admin.register(FlyingList)
class FlyingListAdmin(admin.ModelAdmin):
    def get_urls(self):
        my_urls = [
            path('flying_list/ajax/drivers', self.admin_site.admin_view(load_available_members),
                 name='ajax_available_drivers'),
            path('flying_list/ajax/members', self.admin_site.admin_view(load_available_members),
                 name='ajax_available_members'),
            path('flying-list/', self.admin_site.admin_view(FlyingListView.as_view()), name='flying_list'),
        ]
        return my_urls + super().get_urls()

    def flying_list_view(self, request):
        context = dict(
            self.admin_site.each_context(request),

        )
        return TemplateResponse(request, "admin/sugc/flying.html", context)
