from django.db import IntegrityError

from account.models import User
from account.serializers import UserCreateModel


class UserUniqueConstraintError(Exception):
    """Fields ``email`` and ``username`` must be unique."""


class UserService:
    @classmethod
    def get_users(cls):
        return User.objects.all()

    @classmethod
    def create_user(cls, user_schema: UserCreateModel) -> User:
        try:
            return User.objects.create(
                email=user_schema.email,
                username=user_schema.username,
                password=user_schema.password,
            )
        except IntegrityError:
            # We don't raise `IntegrityError` here, because we prefer domain
            # exceptions over Django ones. It is much easier to manage.
            raise UserUniqueConstraintError from None
