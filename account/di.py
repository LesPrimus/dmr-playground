import punq

from account.mappers import UserMapper
from account.services import UserListService, UserDetailService, UserCreateService

_container = punq.Container()
_container.register(UserListService)
_container.register(UserCreateService)
_container.register(UserDetailService)
_container.register(UserMapper)


class UserContainerInjector:
    def resolve(self, thing):
        return _container.resolve(thing)
