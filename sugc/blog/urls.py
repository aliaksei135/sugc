from django.urls import include, path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

app_name = 'blog'
urlpatterns = [
    path("", include(wagtail_urls), name='main'),
    path("editors/", include(wagtailadmin_urls), name='editors'),
    path("docs/", include(wagtaildocs_urls), name='docs'),
]
