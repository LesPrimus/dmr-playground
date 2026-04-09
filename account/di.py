from dataclasses import dataclass, field

import punq

from account.mappers import UserMapper
from account.serializers import UserCreateModel
from account.services import UserListService


@dataclass(slots=True)
class UserContainerInjector:
    container: punq.Container = field(default_factory=punq.Container)

    def __post_init__(self):
        self.container.register(UserListService)
        self.container.register(UserCreateModel)
        self.container.register(UserMapper)

    def resolve(self, thing):
        return self.container.resolve(thing)
