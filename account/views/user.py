from http import HTTPStatus
from typing import final, override

from django.http import HttpResponse
from dmr import Controller, Body, ResponseSpec
from dmr.endpoint import Endpoint, modify
from dmr.errors import ErrorType
from dmr.plugins.pydantic import PydanticSerializer
from dmr.security.jwt import JWTSyncAuth
from dependency_injector.wiring import Provide, inject

from account.containers import Services
from account.serializers import UserCreateModel, UserModel
from account.services import UserService

from account.services import (
    UserUniqueConstraintError,
)
from base.request import AuthenticatedHttpRequest


@final
class UserController(
    Controller[PydanticSerializer],
):
    request = AuthenticatedHttpRequest
    auth = (JWTSyncAuth(),)

    @modify(
        extra_responses=[
            ResponseSpec(Controller.error_model, status_code=HTTPStatus.FORBIDDEN),
        ]
    )
    @inject
    def get(
        self, user_service: UserService = Provide[Services.user]
    ) -> list[UserModel]:
        return user_service.list_users(user=self.request.user)

    @modify(
        extra_responses=[
            ResponseSpec(Controller.error_model, status_code=HTTPStatus.CONFLICT)
        ]
    )
    @inject
    def post(
        self,
        parsed_body: Body[UserCreateModel],
        user_service: UserService = Provide[Services.user],
    ) -> UserModel:
        return user_service.create_user(parsed_body)

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
            case PermissionError():
                return self.to_error(
                    self.format_error(
                        "You don't have permission to perform this action",
                        error_type=ErrorType.value_error,
                    ),
                    status_code=HTTPStatus.FORBIDDEN,
                )
            case _:
                return super().handle_error(endpoint, controller, exc)
