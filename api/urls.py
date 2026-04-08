from django.urls import include

# Our `path` is an optimized drop-in replacement of `django.urls.path`:
from dmr.routing import Router, path
from . import views

# Router is just a collection of regular Django urls:
router = Router(
    'api/',
    [
        path(
            'user/',
            views.UserController.as_view(),
            name='users',
        ),
    ],
)

# Just a regular `urlpatterns` definition, Django-style:
urlpatterns = [
    path(router.prefix, include((router.urls, 'rest_app'), namespace='api')),
]