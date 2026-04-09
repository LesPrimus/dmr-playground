from django.urls import include

# Our `path` is an optimized drop-in replacement of `django.urls.path`:
from dmr.routing import Router, path

from account.views import UserController

app_name = "account"

# Router is just a collection of regular Django urls:
router = Router(
    "account/",
    [
        path(
            "user/",
            UserController.as_view(),
            name="users",
        ),
    ],
)

# Just a regular `urlpatterns` definition, Django-style:
urlpatterns = [
    path(router.prefix, include((router.urls, "account"), namespace="account")),
]
