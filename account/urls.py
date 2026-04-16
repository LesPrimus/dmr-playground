from django.urls import include, path as django_path

# Our `path` is an optimized drop-in replacement of `django.urls.path`:
from dmr.routing import Router, path

from account import views

app_name = "account"

# Router is just a collection of regular Django urls:
router = Router(
    "account/",
    [
        path("auth/", views.ObtainAccessAndRefreshJwtController.as_view(), name="auth"),
        path(
            "user/",
            views.UserController.as_view(),
            name="users",
        ),
    ],
)

# Just a regular `urlpatterns` definition, Django-style:
urlpatterns = [
    path(router.prefix, include((router.urls, "account"), namespace="account")),
    # Plain Django views — outside the dmr Router so they're excluded from OpenAPI schema:
    django_path(
        "account/auth/google/", views.GoogleLoginView.as_view(), name="google_login"
    ),
    django_path(
        "account/auth/google/callback/",
        views.GoogleCallbackView.as_view(),
        name="google_callback",
    ),
]
