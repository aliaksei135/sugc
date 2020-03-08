from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.contrib.auth import get_user_model

from sugc.models import FlyingList

User = get_user_model()


class FlyingListCreationForm(forms.ModelForm):
    class Meta:
        model = FlyingList
        fields = ['date', 'driver', 'members']

    def __init__(self, *args, **kwargs):
        super(FlyingListCreationForm, self).__init__(*args, **kwargs)
        self.fields['driver'].queryset = User.objects.none()
        self.fields['members'].queryset = User.objects.none()
        self.fields['date'].input_formats = ['%d/%m/%Y']
        self.fields['date'].widget = DatePickerInput(format='%d/%m/%Y')
