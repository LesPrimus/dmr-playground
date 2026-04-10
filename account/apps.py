from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = "account"

    def ready(self):
        from account.containers import Services

        Services()
