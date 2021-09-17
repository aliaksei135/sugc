from django.urls import path

from sugc.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    user_delete_avail_view,
    user_onboarding_submit
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("~delete/", view=user_delete_avail_view, name="delete_avail"),
    path("~ajax/onboarding", view=user_onboarding_submit, name="onboarding_submit"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
