from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
                  path("", TemplateView.as_view(template_name="pages/index.html"), name="home"),

                  path("about/", include([
                      path("typical-day", TemplateView.as_view(template_name="pages/typical_day.html"),
                           name="typical_day"),
                      path("what-is-gliding", TemplateView.as_view(template_name="pages/what_is_gliding.html"),
                           name="what_is_gliding"),
                      path("join", TemplateView.as_view(template_name="pages/joining.html"), name='joining'),
                      path("expeditions", TemplateView.as_view(template_name="pages/expeditions.html"),
                           name="expeditions"),
                      path("faq", TemplateView.as_view(template_name="about_pages/faq.html"), name="faq"),
                      path("", TemplateView.as_view(template_name="pages/about.html"), name="about"),
                  ])),

                  # Django Admin, use {% url 'admin:index' %}
                  path(settings.ADMIN_URL, admin.site.urls),
                  # User management
                  path("users/", include("sugc.users.urls", namespace="users")),
                  path("accounts/", include("allauth.urls")),
                  # CMS
                  path("blog/", include("sugc.blog.urls", namespace='blog')),

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
