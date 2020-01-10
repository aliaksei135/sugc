from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
                  path("", include(wagtail_urls)),
                  path("editors/", include(wagtailadmin_urls)),
                  path("docs/", include(wagtaildocs_urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
