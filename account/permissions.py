from dataclasses import dataclass
from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model

User = get_user_model()


class BasePermission(ABC):
    @abstractmethod
    def has_permission(self, user: User) -> bool: ...


@dataclass
class IsAdmin(BasePermission):
    def has_permission(self, user: User) -> bool:
        return user.is_staff
