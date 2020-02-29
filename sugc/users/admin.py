from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from import_export import resources
from import_export.fields import Field

from sugc.users.forms import UserChangeForm, UserCreationForm, UserAvailabilityForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    availability_form = UserAvailabilityForm
    fieldsets = (("Gliding", {"fields":
        (
            "has_susu_membership", "is_driver", "is_solo", "is_bronze", "is_xc", "date_of_birth")}),) \
                + auth_admin.UserAdmin.fieldsets[1:]
    list_display = ["first_name", "last_name", "is_staff", "has_susu_membership"]
    search_fields = ["first_name", "last_name", "email"]
    ordering = ['last_name']


class UserResource(resources.ModelResource):
    id = Field(attribute='id', column_name='userID')
    first_name = Field(attribute='first_name', column_name='firstName')
    last_name = Field(attribute='last_name', column_name='surname')
    mock_password = Field(column_name='password', readonly=True)
    email = Field(attribute='email', column_name='email')
    junior = Field(column_name='junior', readonly=True)
    driver = Field(attribute='is_driver', column_name='driver')
    committee = Field(attribute='is_staff', column_name='committee')
    joined = Field(attribute='date_joined', column_name='joined')

    class Meta:
        model = User
        skip_unchanged = True
        report_skipped = True
