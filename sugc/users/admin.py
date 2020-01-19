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
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name", "availability"]
