from smtplib import SMTPException

from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import resolve_url
from django.urls import path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from import_export import resources, widgets
from import_export.admin import ImportExportActionModelAdmin
from import_export.fields import Field

from sugc.admin_views import load_available_members, FlyingListView, load_available_drivers
from sugc.models import FeesInvoice, Flight, FlyingList, Aircraft, GlidingFeePeriod, GlidingFeeGroup

user_model = get_user_model()


# django-import-export ModelResources
# ----------------------------------------------------------------------------------------

class FlightResource(resources.ModelResource):
    id = Field(attribute='id', column_name='ID', saves_null_values=False)
    date = Field(attribute='date', column_name='Date', widget=widgets.DateWidget())
    day_id = Field(column_name='dayID', readonly=True)
    first_name = Field(column_name='firstName', readonly=True)
    last_name = Field(column_name='surname', readonly=True)
    user_id = Field(attribute='member', column_name='userID', saves_null_values=False,
                    widget=widgets.ForeignKeyWidget(user_model, 'id'))
    aircraft = Field(attribute='aircraft', column_name='a/c', saves_null_values=False,
                     widget=widgets.ForeignKeyWidget(Aircraft, 'registration'))
    duration = Field(attribute='duration', column_name='Duration')
    capacity = Field(attribute='capacity', column_name='Crew')
    friend_or_trial = Field(column_name='FriendOrTrial', readonly=True)
    trial = Field(column_name='Trial', readonly=True)
    tlf = Field(attribute='is_train_launch_failure', column_name='TLF')
    rlf = Field(attribute='is_real_launch_failure', column_name='RLF')
    badge_flight = Field(column_name='Badge flight', readonly=True)
    instructing = Field(column_name='Instructing')
    xc_flight = Field(column_name='XC flight', readonly=True, default='NO')
    xc_distance = Field(column_name='XC Distance', readonly=True, default='')
    xc_comments = Field(column_name='Comments', readonly=True, default='')

    class Meta:
        model = Flight
        skip_unchanged = True
        report_skipped = True


class GlidingFeePeriodResource(resources.ModelResource):
    id = Field(attribute='id', column_name='feesListID')
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


@admin.register(GlidingFeeGroup)
class GlidingFeeGroupAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Flight)
class FlightAdmin(ImportExportActionModelAdmin):
    resource_class = FlightResource
    list_display = ['date', 'member', 'aircraft', 'capacity']
    readonly_fields = ('inv',)
    exclude = ('invoice',)
    ordering = ['-date']
    search_fields = ['aircraft', 'date']

    def inv(self, obj):
        invoice = obj.invoice
        if invoice is not FeesInvoice.objects.none:
            url = resolve_url(admin_urlname(FeesInvoice._meta, 'change'), invoice.pk)
            name = invoice.__str__()
            return mark_safe('<a href="{url}">{name}</a>'.format(url=url, name=name))
        else:
            return 'Not invoiced'

    inv.short_description = 'Invoice'

    def memb(self, obj):
        member = obj.member
        url = resolve_url(admin_urlname(user_model._meta, 'change'), member.pk)
        name = member.__str__()
        return mark_safe('<a href="{url}">{name}</a>'.format(url=url, name=name))

    memb.short_description = 'Member'


def mark_paid(modeladmin, request, queryset):
    queryset.update(paid=True)


@admin.register(FeesInvoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['paid', 'date', 'member', 'balance']
    list_filter = ['paid']
    readonly_fields = ('member', 'flights',)
    ordering = ['-date', 'member']
    search_fields = ['member']
    actions = [mark_paid]

    def flights(self, obj):
        flights = obj.flights.all()
        html_list = '<ul>'
        for flight in flights:
            url = resolve_url(admin_urlname(Flight._meta, 'change'), flight.pk)
            name = flight.__str__()
            html_list += format_html('<li><a href="{url}">{name}</a></li>'.format(url=url, name=name))
        html_list += '</ul>'
        return mark_safe(html_list)


def email_flying_list(_, request, queryset):
    for flying_list in queryset:
        if isinstance(flying_list, FlyingList):
            try:
                date_str = flying_list.date.strftime('%d/%m/%Y')
                flying_list.driver.email_user('Flying {}'.format(date_str),
                                              "You've been selected to drive for flying on {}".format(date_str),
                                              )
                send_mail('Flying {}'.format(date_str),
                          "You've been selected for flying on {}".format(date_str),
                          None,
                          list(flying_list.members.all())
                          )

                messages.success(request, "Emails sent")
            except (SMTPException, BadHeaderError) as e:
                messages.error(request, e)


@admin.register(FlyingList)
class FlyingListAdmin(admin.ModelAdmin):
    actions = [email_flying_list]

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
