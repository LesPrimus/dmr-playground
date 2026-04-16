from account.permissions import IsAdmin
from account import services


from dependency_injector import containers, providers


class Services(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["account.views.user", "account.views.oauth"]
    )

    user = providers.Factory(
        services.UserService,
        permission=providers.Object(IsAdmin()),
    )

    oauth = providers.Factory(
        services.OauthService,
    )
