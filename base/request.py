from django.http import HttpRequest
from account.models import User


class AuthenticatedHttpRequest(HttpRequest):
    user: User
