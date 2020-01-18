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
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class UserAvailabilityForm(dj_forms.ModelForm):
    # date_available = dj_forms.DateField(label="Availability",
    #                                     required=True,
    #                                     input_formats='%d/%m/%Y',
    #                                     widget=DatePickerInput(format='%d/%m/%Y',
    #                                                            attrs={'class': 'form-control'},
    #                                                            options={
    #                                                                'daysOfWeekDisabled': [1,2,4,5],
    #                                                                'minDate': datetime.now().date().isoformat(),
    #                                                                'locale': 'en-gb',
    #                                                            })
    #                                     )

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
