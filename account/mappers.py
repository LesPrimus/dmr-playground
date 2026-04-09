from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from account.serializers import UserModel

User = get_user_model()


@dataclass
class UserMapper:
    def single(self, user: User) -> UserModel:
        return UserModel(id=user.pk, username=user.username, email=user.email)

    def multiple(self, users: QuerySet[User]) -> list[UserModel]:
        return [self.single(user) for user in users]
