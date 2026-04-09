from typing import final

from dmr import Controller, Body
from dmr.plugins.pydantic import PydanticSerializer

from .serializers import UserCreateModel, UserModel
from .services import UserService


@final
class UserController(Controller[PydanticSerializer]):
    def get(self) -> list[UserModel]:
        return [
            UserModel(id=u.pk, username=u.username, email=u.email)
            for u in UserService.get_users()
        ]

    def post(self, parsed_body: Body[UserCreateModel]) -> UserModel:
        user = UserService.create_user(parsed_body)
        return UserModel(id=user.pk, username=user.username, email=user.email)
