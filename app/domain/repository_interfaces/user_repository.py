from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.models.user import User, UserRole

class UserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_multi(self, skip: int = 0, limit: int = 100, role: Optional[UserRole] = None) -> List[User]:
        pass
