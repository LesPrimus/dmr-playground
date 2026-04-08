import pydantic

from dmr import Controller, Headers, Body
from dmr.plugins.pydantic import PydanticSerializer


class UserModel(pydantic.BaseModel):
    email: str
    name: str


class UserCreateModel(UserModel):
    pass


class HeaderModel(pydantic.BaseModel):
    consumer: str = pydantic.Field(alias="X-FOO")


class UserController(Controller[PydanticSerializer]):
    def get(self, parsed_headers: Headers[HeaderModel]) -> UserModel:
        return UserModel(email="foo@email.com", name=parsed_headers.consumer)

    def post(self, parsed_body: Body[UserCreateModel]) -> UserModel:
        return UserModel(email=parsed_body.email, name=parsed_body.name)
