from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.core.database import get_session
from app.domain.models.user import User, UserRole
from app.domain.repository_interfaces.item_repository import ItemRepository
from app.domain.repository_interfaces.user_repository import UserRepository
from app.infrastructure.repositories.postgres_item_repository import PostgresItemRepository
from app.infrastructure.repositories.postgres_user_repository import PostgresUserRepository
from app.services.auth_service import AuthService
from app.services.item_service import ItemService

async def get_item_repository(
    session: AsyncSession = Depends(get_session),
) -> ItemRepository:
    return PostgresItemRepository(session)

async def get_item_service(
    repo: ItemRepository = Depends(get_item_repository),
) -> ItemService:
    return ItemService(repo)

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

async def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return PostgresUserRepository(session)

async def get_auth_service() -> AuthService:
    return AuthService()

async def get_current_user(
    token: Annotated[str, Depends(reusable_oauth2)],
    user_repo: UserRepository = Depends(get_user_repo)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = payload.get("sub")
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    user = await user_repo.get_by_email(email=str(token_data))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
