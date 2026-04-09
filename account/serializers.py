from typing import Annotated, final

import pydantic

type UserId = Annotated[int, pydantic.Field(gt=0)]


class BaseUserModel(pydantic.BaseModel):
    username: str
    email: str


@final
class UserModel(BaseUserModel):
    id: UserId


@final
class UserCreateModel(BaseUserModel):
    password: str
