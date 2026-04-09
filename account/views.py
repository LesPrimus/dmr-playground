from typing import final

from dmr import Controller, Body
from dmr.plugins.pydantic import PydanticSerializer

from .serializers import UserCreateModel, UserModel
from .services import UserService


@final
class UserController(Controller[PydanticSerializer]):
    def get(self) -> list[UserModel]:
        return [
            UserModel(username=u.username, email=u.email)
            for u in UserService.get_users()
        ]

    def post(self, parsed_body: Body[UserCreateModel]) -> UserModel:
        return UserModel(username=parsed_body.username, email=parsed_body.email)
