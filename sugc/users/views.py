from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.edit import ModelFormMixin

from .forms import UserAvailabilityForm
from ..models import Availability

User = get_user_model()


class UserDetailView(LoginRequiredMixin, ModelFormMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    form_class = UserAvailabilityForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UserAvailabilityForm(request.POST, user=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def form_valid(self, form):
        avail = Availability(date_available=form.cleaned_data['date_available'], member=self.request.user)
        avail.save()
        messages.add_message(
            self.request, messages.INFO, _("Availability updated")
        )
        return super().form_valid(form)


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
