from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from sugc.users.forms import UserChangeForm, UserCreationForm, UserAvailabilityForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    availability_form = UserAvailabilityForm
    fieldsets = (("User", {"fields":
                               (
                               "has_susu_membership", "is_driver", "is_solo", "is_bronze", "is_xc", "date_of_birth")}),) \
                + auth_admin.UserAdmin.fieldsets
    list_display = ["first_name", "last_name", "is_staff", "has_susu_membership"]
    search_fields = ["first_name", "last_name", "email"]
    ordering = ['last_name']



