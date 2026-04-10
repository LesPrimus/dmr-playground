from typing import Annotated, final

import pydantic

type UserId = Annotated[int, pydantic.Field(gt=0)]


class BaseUserModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    username: str
    email: str


@final
class UserModel(BaseUserModel):
    id: UserId


@final
class UserCreateModel(BaseUserModel):
    password: str
