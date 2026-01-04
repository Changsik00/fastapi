from typing import Optional, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.domain.models.user import User, UserRole
from app.domain.repository_interfaces.user_repository import UserRepository

class PostgresUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement)
        return result.first()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_multi(self, skip: int = 0, limit: int = 100, role: Optional[UserRole] = None) -> List[User]:
        query = select(User).offset(skip).limit(limit)
        if role:
            query = query.where(User.role == role)
        result = await self.session.exec(query)
        return result.all()
