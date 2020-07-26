import datetime

from bootstrap_datepicker_plus import DatePickerInput
from django import forms as dj_forms
from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from sugc.models import Availability

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_driver', 'phone_number', 'student_id']


class UserCreationForm(forms.UserCreationForm):
    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken."),
         "dob_in_future": _("Date of Birth cannot be in future")},
    )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = DatePickerInput(format='%d/%m/%Y',
                                                              attrs={'class': 'form-control'},
                                                              options={
                                                                  'locale': 'en-gb',
                                                              })

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'student_id', 'phone_number', 'date_of_birth']

    def clean_date_of_birth(self):
        dob = self.cleaned_data["date_of_birth"]
        if dob < datetime.date.today():
            return dob
        raise ValidationError(self.error_messages["dob_in_future"], code='dob_in_future')

    def save(self, commit=True):
        # saved in adapter
        pass


class UserAvailabilityForm(dj_forms.ModelForm):
    error_message = {
        "duplicate_availability": "Availability on this date has already been added",
        "past_availability": "Availability cannot be added in the past"
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserAvailabilityForm, self).__init__(*args, **kwargs)

        self.fields['date_available'].label = 'Availability'
        self.fields['date_available'].input_formats = ['%d/%m/%Y']
        self.fields['date_available'].widget = DatePickerInput(format='%d/%m/%Y',
                                                               attrs={'class': 'form-control'},
                                                               options={
                                                                   'daysOfWeekDisabled': [1, 2, 4, 5],
                                                                   'minDate': datetime.date.today().isoformat(),
                                                                   'maxDate': (datetime.date.today()
                                                                               + datetime.timedelta(
                                                                           weeks=2)).isoformat(),
                                                                   'locale': 'en-gb',
                                                               })

    def clean_date_available(self):
        date = self.cleaned_data['date_available']
        if date < datetime.date.today():
            raise ValidationError(self.error_message['past_availability'], code='past_availability')
        yesterday_date = datetime.date.today() - datetime.timedelta(days=1)
        user_availability = self.user.availability.filter(date_available__gte=yesterday_date)
        for availability in user_availability:
            if date == availability.date_available:
                raise ValidationError(self.error_message['duplicate_availability'], code='duplicate_availability')
        return date

    class Meta:
        model = Availability
        fields = ['date_available']
