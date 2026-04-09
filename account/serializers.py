from typing import Annotated

import pydantic

type UserId = Annotated[int, pydantic.Field(gt=0)]


class BaseUserModel(pydantic.BaseModel):
    username: str
    email: str


class UserModel(BaseUserModel):
    id: UserId


class UserCreateModel(BaseUserModel):
    password: str
