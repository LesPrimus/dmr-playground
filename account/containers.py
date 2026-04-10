from account.mappers import UserMapper
from account.permissions import IsAdmin
from account import services


from dependency_injector import containers, providers


class Services(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["account.views.user"])

    user = providers.Factory(
        services.UserService,
        mapper=providers.Object(UserMapper()),
        permission=providers.Object(IsAdmin()),
    )


class Application(containers.DeclarativeContainer):
    pass
