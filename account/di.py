import punq

from account.mappers import UserMapper
from account.permissions import IsAdmin
from account.services import UserListService, UserDetailService, UserCreateService

_container = punq.Container()

_container.register(UserListService)
_container.register(UserCreateService)
_container.register(UserDetailService)
_container.register(UserMapper)
_container.register(IsAdmin)


class UserContainerInjector:
    def resolve(self, thing, **kwargs):
        return _container.resolve(thing, **kwargs)
