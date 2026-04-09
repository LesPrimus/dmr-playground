from account.models import User


class UserUniqueConstraintError(Exception):
    """Fields ``email`` and ``username`` must be unique."""


class UserService:
    @classmethod
    def get_users(cls):
        return User.objects.all()
