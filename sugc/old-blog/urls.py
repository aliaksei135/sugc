from django.urls import path, include

from wagtail.admin import urls as wt_admin_urls
from wagtail.core import urls as wt_urls

app_name = "blog"
urlpatterns = [
    path("editors/", include(wt_admin_urls), name="blog_editors"),
    path("", include(wt_urls), name="blog_index"),
]
