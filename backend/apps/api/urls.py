from apps.users import views as users_views
from django.urls import include, path

app_name = "api"
urlpatterns = [
    path("", include("apps.users.urls")),
    path("", include("apps.chat.urls")),
    path("csrf/", users_views.get_csrf, name="api-csrf"),
    path(
        "token/connection/",
        users_views.get_connection_token,
        name="api-connection-token",
    ),
    path(
        "token/subscription/",
        users_views.get_subscription_token,
        name="api-subscription-token",
    ),
    path("login/", users_views.login_view, name="api-login"),
    path("logout/", users_views.logout_view, name="api-logout"),
]
