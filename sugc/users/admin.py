import datetime

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field

from sugc.users import adapters
from sugc.users.forms import UserChangeForm, UserAvailabilityForm

User = get_user_model()


class UserResource(resources.ModelResource):
    id = Field(attribute='id', column_name='userID')
    first_name = Field(attribute='first_name', column_name='firstName')
    last_name = Field(attribute='last_name', column_name='lastName')
    mock_password = Field(column_name='password', readonly=True)
    email = Field(attribute='email', column_name='email')
    junior = Field(column_name='junior', readonly=True)
    is_driver = Field(attribute='is_driver', column_name='driver')
    is_staff = Field(attribute='is_staff', column_name='committee')
    date_joined = Field(attribute='date_joined', column_name='joined', default=datetime.datetime.today())

    def before_save_instance(self, instance, using_transactions, dry_run):
        instance.username = adapters.generate_random_username()
        instance.date_of_birth = datetime.date.today()
        instance.password = make_password(None)

    class Meta:
        model = User
        skip_unchanged = True
        report_skipped = True
        exclude = ['profile_img', 'date_of_birth', 'on_waiting_list', 'has_susu_membership', 'student_id', 'is_solo',
                   'is_bronze', 'password', 'is_xc', 'username', 'is_active', 'last_login', 'is_superuser', 'groups',
                   'user_permissions']


@admin.register(User)
class UserAdmin(ImportExportMixin, auth_admin.UserAdmin):
    form = UserChangeForm
    availability_form = UserAvailabilityForm
    resource_class = UserResource
    fieldsets = (("Gliding", {"fields":
                                  ("has_susu_membership", "is_driver", "is_solo", "on_waiting_list", "is_bronze",
                                   # noqa E127
                                   "is_xc", "date_of_birth")}),
                 ) + auth_admin.UserAdmin.fieldsets[1:]
    list_display = ["first_name", "last_name", "is_staff", "has_susu_membership", "on_waiting_list"]
    search_fields = ["first_name", "last_name", "email"]
    ordering = ['last_name']

    def has_add_permission(self, request):
        return False
