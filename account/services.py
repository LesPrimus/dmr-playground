import uuid
from dataclasses import dataclass
import datetime as dt

from django.conf import settings
from django.core import signing
from django.db import IntegrityError
from django.db.models import QuerySet
from dmr.security.jwt import JWToken

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


@dataclass
class OauthService:
    @staticmethod
    def make_jwt(user: User, token_type: str, expiration: dt.timedelta) -> str:
        now = dt.datetime.now(dt.UTC)
        return JWToken(
            sub=str(user.pk),
            exp=now + expiration,
            jti=uuid.uuid4().hex,
            extras={"type": token_type},
        ).encode(secret=settings.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def encode_state(data: dict) -> str:
        return signing.dumps(data, salt="oauth_state")

    @staticmethod
    def decode_state(raw: str, max_age: int = 300) -> dict:
        return signing.loads(raw, salt="oauth_state", max_age=max_age)
