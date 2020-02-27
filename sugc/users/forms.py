import datetime

from bootstrap_datepicker_plus import DatePickerInput
from django import forms as dj_forms
from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Availability

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")},
    )
    error_message = forms.UserCreationForm.error_messages.update(
        {"dob_in_future": _("Date of Birth cannot be in future!")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'student_id', 'date_of_birth']

    def clean_date_of_birth(self):
        dob = self.cleaned_data["date_of_birth"]
        if dob < datetime.date(datetime.today()):
            return dob
        return ValidationError(self.error_messages["dob_in_future"])

    def save(self, commit=True):
        # saved in adapter
        pass


class UserAvailabilityForm(dj_forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserAvailabilityForm, self).__init__(*args, **kwargs)

        self.fields['date_available'].label = 'Availability'
        self.fields['date_available'].input_formats = ['%d/%m/%Y']
        self.fields['date_available'].widget = DatePickerInput(format='%d/%m/%Y',
                                                               attrs={'class': 'form-control'},
                                                               options={
                                                                   'daysOfWeekDisabled': [1, 2, 4, 5],
                                                                   'minDate': datetime.date.today().isoformat(),
                                                                   'maxDate': datetime.date.today()
                                                                              + datetime.timedelta(weeks=2),
                                                                   'locale': 'en-gb',
                                                               })

    class Meta:
        model = Availability
        fields = ['date_available']
