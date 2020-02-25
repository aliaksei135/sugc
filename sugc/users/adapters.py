from random import choice
from string import ascii_letters, digits
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest

User = get_user_model()


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user.email = data.get('email')
        user.username = self.generate_random_username()
        user.date_of_birth = data.get('date_of_birth')
        user.student_id = data.get('student_id_number')
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user

    # Complies with GDPR as well
    # https://gist.github.com/jcinis/2866253
    def generate_random_username(self, length=16, chars=ascii_letters + digits, split=4, delimiter=''):
        username = ''.join([choice(chars) for i in range(length)])
        if split:
            username = delimiter.join([username[start:start + split] for start in range(0, len(username), split)])

        try:
            User.objects.get(username=username)
            return self.generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
        except User.DoesNotExist:
            return username


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
