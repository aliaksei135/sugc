from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from sugc.models import Flight, Aircraft
from sugc.users.forms import UserChangeForm, UserCreationForm, UserAvailabilityForm

User = get_user_model()

admin.site.register(Flight)
admin.site.register(Aircraft)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    availability_form = UserAvailabilityForm
    fieldsets = (("User", {"fields":
                               ("name", "has_susu_membership", "is_solo", "is_bronze", "is_xc")}),) \
                + auth_admin.UserAdmin.fieldsets
    list_display = ["name", "is_staff", "waiting_list_position", "has_susu_membership"]
    search_fields = ["name", "availability"]
