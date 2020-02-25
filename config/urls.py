from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
                  path("", TemplateView.as_view(template_name="index.html"), name="home"),
                  path("gallery/", TemplateView.as_view(template_name="gallery.html"), name="gallery"),
                  path("about/", include([
                      path("typical-day", TemplateView.as_view(template_name="about_pages/typical_day.html"),
                           name="typical_day"),
                      path("what-is-gliding", TemplateView.as_view(template_name="pages/what_is_gliding.html"),
                           name="what_is_gliding"),
                      path("join", TemplateView.as_view(template_name="about_pages/joining.html"), name='joining'),
                      path("expeditions", TemplateView.as_view(template_name="about_pages/expeditions.html"),
                           name="expeditions"),
                      path("faq", TemplateView.as_view(template_name="about_pages/faq.html"), name="faq"),
                      path("", TemplateView.as_view(template_name="about_pages/about.html"), name="about"),
                  ])),

                  # Django Admin, use {% url 'admin:index' %}
                  path('jet/', include('jet.urls', 'jet')),
                  path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
                  path(settings.ADMIN_URL, admin.site.urls),
                  # User management
                  path("users/", include("sugc.users.urls", namespace="users")),
                  path("accounts/", include("allauth.urls")),
                  path("avatar/", include('avatar.urls')),
                  # CMS
                  # Cannot specify these in blog app due to wagtail namespace restrictions
                  path("blog/", include('puput.urls')),
                  # path("blog/editors/", include(wagtailadmin_urls)),
                  # path("wagtail/", include(wagtail_urls)),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
