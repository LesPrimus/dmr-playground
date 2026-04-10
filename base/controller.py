from dmr import Controller
from dmr.plugins.pydantic import PydanticSerializer
from dmr.serializer import BaseSerializer


class BaseController[T: BaseSerializer](Controller[T]):
    pass


class PydanticController(BaseController[PydanticSerializer]):
    pass
