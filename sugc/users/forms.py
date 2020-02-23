from datetime import datetime

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

    # date_of_birth = dj_forms.DateField(
    #     label=_("Date of Birth"),
    #     widget=dj_forms.DateInput,
    #     hint=_("Enter your Date of Birth"),
    # )
    #
    # student_id = dj_forms.IntegerField(
    #     label=_("Student ID Number"),
    #
    # )

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'student_id', 'date_of_birth']

    # def clean_username(self):
    #     username = self.cleaned_data["username"]
    #
    #     try:
    #         User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         return username
    #
    #     raise ValidationError(self.error_messages["duplicate_username"])

    def clean_date_of_birth(self):
        dob = self.cleaned_data["date_of_birth"]
        if dob < datetime.date(datetime.today()):
            return dob
        return ValidationError(self.error_messages["dob_in_future"])


class UserAvailabilityForm(dj_forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserAvailabilityForm, self).__init__(*args, **kwargs)

        self.fields['date_available'].label = 'Availability'
        self.fields['date_available'].input_formats = ['%d/%m/%Y']
        self.fields['date_available'].widget = DatePickerInput(format='%d/%m/%Y',
                                                               attrs={'class': 'form-control'},
                                                               options={
                                                                   'daysOfWeekDisabled': [1, 2, 4, 5],
                                                                   'minDate': datetime.now().date().isoformat(),
                                                                   'locale': 'en-gb',
                                                               })

    class Meta:
        model = Availability
        fields = ['date_available']
