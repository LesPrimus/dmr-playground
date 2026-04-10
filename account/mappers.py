from dataclasses import dataclass

from django.db.models import QuerySet

from account.models import User
from account.serializers import UserModel


@dataclass
class UserMapper:
    def single(self, user: User) -> UserModel:
        return UserModel(id=user.pk, username=user.username, email=user.email)

    def multiple(self, users: QuerySet[User]) -> list[UserModel]:
        return [self.single(user) for user in users]
