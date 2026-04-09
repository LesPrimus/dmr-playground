import pydantic


class UserModel(pydantic.BaseModel):
    username: str
    email: str


class UserCreateModel(UserModel):
    password: str
