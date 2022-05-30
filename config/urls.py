from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Social Post API",
        default_version="v1",
        description="You will need this!",
        terms_of_service="",
        contact=openapi.Contact(email="elfateh.dev@gmail.com"),
        license=openapi.License(name="Proprietary"),
    ),
    permission_classes=(permissions.AllowAny,),
    public=True,
)


api_urlpatterns = [
    path("users/", include("app.users.urls")),
    path("posts/", include("app.posts.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
    re_path(r"^api/(?P<version>v(1))/", include(api_urlpatterns)),
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
