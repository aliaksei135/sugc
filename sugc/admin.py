from django.contrib import admin
from django.urls import path
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from import_export.fields import Field

from sugc.admin_views import load_available_members, FlyingListView, load_available_drivers
from sugc.models import FeesInvoice, Flight, FlyingList, Aircraft, GlidingFeePeriod


# django-import-export ModelResources
# ----------------------------------------------------------------------------------------

class FlightResource(resources.ModelResource):
    id = Field(attribute='id', column_name='ID', saves_null_values=False)
    date = Field(attribute='date', column_name='Date')
    day_id = Field(column_name='dayID', readonly=True)
    first_name = Field(column_name='firstName', readonly=True)
    last_name = Field(column_name='surname', readonly=True)
    user_id = Field(attribute='member__id', column_name='userID', saves_null_values=False)
    aircraft = Field(attribute='aircraft__registration', column_name='a/c', saves_null_values=False)
    duration = Field(attribute='Duration', column_name='Duration')
    capacity = Field(attribute='capacity', column_name='Crew')
    friend_or_trial = Field(column_name='FriendOrTrial', readonly=True)
    trial = Field(column_name='Trial', readonly=True)
    tlf = Field(attribute='is_train_launch_failure', column_name='TLF')
    rlf = Field(attribute='is_real_launch_failure', column_name='RLF')
    badge_flight = Field(column_name='Badge flight', readonly=True)
    instructing = Field(column_name='Instructing')
    xc_flight = Field(column_name='XC flight', readonly=True)
    xc_distance = Field(column_name='XC Distance', readonly=True)
    xc_comments = Field(column_name='Comments', readonly=True)

    class Meta:
        model = Flight
        skip_unchanged = True
        report_skipped = True


class GlidingFeePeriodResource(resources.ModelResource):
    id = Field(attribute='id', column_name='feesLsistID')
    start_date = Field(attribute='date_effective_from', column_name='startDate')
    end_date = Field(column_name='endDate', readonly=True)

    cost_mins = Field(attribute='junior_minute_cost', column_name='costMins')
    cost_subs_mins = Field(attribute='junior_subs_minute_cost', column_name='costSubsidisedMins')
    cost_launch = Field(attribute='junior_launch_cost', column_name='costLaunch')
    cost_subs_launch = Field(attribute='junior_subs_launch_cost', column_name='costSubsidisedLaunch')
    cost_tlf = Field(attribute='junior_tlf_cost', column_name='costTLF')
    cost_subs_tlf = Field(attribute='junior_subs_tlf_cost', column_name='costSubsidisedTLF')

    std_cost_mins = Field(attribute='std_minute_cost', column_name='oldMins')
    std_cost_subs_mins = Field(attribute='std_subs_minute_cost', column_name='oldSubsidisedMins')
    std_cost_launch = Field(attribute='std_launch_cost', column_name='oldLaunch')
    std_cost_subs_launch = Field(attribute='std_subs_launch_cost', column_name='oldSubsidisedLaunch')
    std_cost_tlf = Field(attribute='std_tlf_cost', column_name='oldTLF')
    std_cost_subs_tlf = Field(attribute='std_subs_tlf_cost', column_name='oldSubsidisedTLF')

    class Meta:
        model = GlidingFeePeriod
        skip_unchanged = True
        report_skipped = True


# Model Admins
# ------------------------------------------------------------------------------------------


admin.site.register(Aircraft)


@admin.register(GlidingFeePeriod)
class GlidingFeePeriodAdmin(ImportExportActionModelAdmin):
    resource_class = GlidingFeePeriodResource


@admin.register(Flight)
class FlightAdmin(ImportExportActionModelAdmin):
    resource_class = FlightResource
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
            path('flying_list/ajax/drivers', self.admin_site.admin_view(load_available_drivers),
                 name='ajax_available_drivers'),
            path('flying_list/ajax/members', self.admin_site.admin_view(load_available_members),
                 name='ajax_available_members'),
            path('flying-list/', self.admin_site.admin_view(FlyingListView.as_view()), name='flying_list'),
        ]
        return my_urls + super().get_urls()

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        default_response = super(FlyingListAdmin, self).render_change_form(request, context, add=add,
                                                                           change=change, form_url=form_url, obj=obj)
        if not add:
            return default_response
        else:
            return FlyingListView.as_view()(default_response._request)
