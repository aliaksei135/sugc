from admin_views.admin import AdminViews
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
class FlyingListAdmin(AdminViews):
    admin_views = (
        ('Make new Flying List', 'flying_list')
    )

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

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        default_response = super(FlyingListAdmin, self).render_change_form(request, context, add=add,
                                                                           change=change, form_url=form_url, obj=obj)
        if not add:
            return default_response
        else:
            return FlyingListView.as_view()(default_response._request)
