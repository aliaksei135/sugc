import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django_tables2 import SingleTableMixin

from .forms import UserAvailabilityForm
from .tables import FlightTable
from ..models import Availability

User = get_user_model()


class UserDetailView(LoginRequiredMixin, ModelFormMixin, SingleTableMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    form_class = UserAvailabilityForm

    table_class = FlightTable
    table_pagination = {
        'per_page': 10
    }

    def get_table_data(self):
        return self.object.flights.all()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UserAvailabilityForm(request.POST, user=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['avail_list'] = self.object.availability.filter(date_available__gte=datetime.date.today(),
                                                                date_available__lte=(datetime.date.today()
                                                                                     + datetime.timedelta(weeks=2)
                                                                                     )
                                                                )
        # flights_table = FlightTable(self.object.flights.all())
        # flights_table.paginate(page=self.request.GET.get('flights_page', 1), per_page=10)
        # context['table'] = flights_table
        return context

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def form_valid(self, form):
        avail = Availability(date_available=form.cleaned_data['date_available'], member=self.request.user)
        avail.save()
        messages.add_message(
            self.request, messages.SUCCESS, _("Availability updated")
        )
        return HttpResponseRedirect(self.get_success_url())


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'student_id', 'is_driver']

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, _("Details successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def user_delete_avail_view(request, *args, **kwargs):
    pk = request.POST.get('avail_pk')
    avail = Availability.objects.filter(pk=pk, member=request.user)
    avail.delete()
    messages.add_message(
        request, messages.SUCCESS, _("Availability deleted")
    )
    return HttpResponseRedirect(reverse("users:detail", kwargs={'username': request.user.username}))
