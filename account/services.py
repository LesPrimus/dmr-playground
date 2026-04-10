from dataclasses import dataclass

from django.db import IntegrityError
from django.db.models import QuerySet

from account.models import User
from account.permissions import BasePermission
from account.serializers import UserCreateModel, UserModel


class UserUniqueConstraintError(Exception):
    """Fields ``email`` and ``username`` must be unique."""


@dataclass
class UserService:
    permission: BasePermission

    @staticmethod
    def get_users():
        return User.objects.all()

    def create_user(self, user_schema: UserCreateModel) -> UserModel:
        try:
            user = User.objects.create_user(
                email=user_schema.email,
                username=user_schema.username,
                password=user_schema.password,
            )
        except IntegrityError:
            # We don't raise `IntegrityError` here, because we prefer domain
            # exceptions over Django ones. It is much easier to manage.
            raise UserUniqueConstraintError from None
        return UserModel.model_validate(user)

    def list_users(self, user):
        self.check_permission(user)
        users: QuerySet[User] = self.get_users()
        return [UserModel.model_validate(u) for u in users]

    def check_permission(self, user: User):
        if not self.permission.has_permission(user):
            raise PermissionError("You are not admin")
