from collections import UserList
from http import HTTPStatus
from typing import final, override

from django.http import HttpResponse
from dmr import Controller, Body, ResponseSpec
from dmr.endpoint import Endpoint, modify
from dmr.errors import ErrorType
from dmr.plugins.pydantic import PydanticSerializer

from .di import UserContainerInjector
from .serializers import UserCreateModel, UserModel
from .services import UserService, UserUniqueConstraintError, UserListService


@final
class UserController(
    UserContainerInjector,  # DI injects the services
    Controller[PydanticSerializer],
):
    def get(self) -> list[UserModel]:
        return self.resolve(UserListService)(UserService.get_users())

    @modify(
        extra_responses=[
            ResponseSpec(Controller.error_model, status_code=HTTPStatus.CONFLICT)
        ]
    )
    def post(self, parsed_body: Body[UserCreateModel]) -> UserModel:
        user = UserService.create_user(parsed_body)
        return UserModel(id=user.pk, username=user.username, email=user.email)

    # --- Controller Error handling --- #

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: "Controller[PydanticSerializer]",
        exc: Exception,
    ) -> HttpResponse:
        match exc:
            case UserUniqueConstraintError():
                return self.to_error(
                    self.format_error(
                        "User `email` and `username` must be unique",
                        error_type=ErrorType.value_error,
                    ),
                    status_code=HTTPStatus.CONFLICT,
                )
            case _:
                return super().handle_error(endpoint, controller, exc)
