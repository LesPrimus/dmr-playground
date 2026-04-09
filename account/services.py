from dataclasses import dataclass

from django.db import IntegrityError
from django.db.models import QuerySet

from account.mappers import UserMapper
from account.models import User
from account.serializers import UserCreateModel, UserModel


class UserUniqueConstraintError(Exception):
    """Fields ``email`` and ``username`` must be unique."""


class UserService:
    @classmethod
    def get_users(cls):
        return User.objects.all()

    @classmethod
    def create_user(cls, user_schema: UserCreateModel) -> User:
        try:
            return User.objects.create_user(
                email=user_schema.email,
                username=user_schema.username,
                password=user_schema.password,
            )
        except IntegrityError:
            # We don't raise `IntegrityError` here, because we prefer domain
            # exceptions over Django ones. It is much easier to manage.
            raise UserUniqueConstraintError from None


@dataclass
class UserListService:
    mapper: UserMapper

    def __call__(self) -> list[UserModel]:
        users: QuerySet[User] = UserService.get_users()
        return self.mapper.multiple(users)


@dataclass
class UserDetailService:
    mapper: UserMapper

    def __call__(self, user: User) -> UserModel:
        return self.mapper.single(user)


@dataclass
class UserCreateService:
    mapper: UserMapper

    def __call__(self, user_schema: UserCreateModel) -> UserModel:
        return self.mapper.single(UserService.create_user(user_schema))
