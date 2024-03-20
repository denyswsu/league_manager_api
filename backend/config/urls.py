from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="League Manager API",
        default_version="v1",
        description="It is a Multi-tenant RESTful API that provides "
        "ability to create websites for football leagues and manage them.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="marzique@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path("api/", include("apps.api.urls", namespace="api")),
    path("api/channels_chat/", include("apps.websockets.urls")),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("django/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    # enable media on localhost
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
