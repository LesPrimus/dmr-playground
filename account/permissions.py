from dataclasses import dataclass
from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

User = get_user_model()


class BasePermission(ABC):
    @abstractmethod
    def has_permission(self) -> bool: ...


@dataclass
class IsAdmin(BasePermission):
    user: User

    def has_permission(self) -> bool:
        return self.user.is_staff
