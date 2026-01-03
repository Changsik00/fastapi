from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain.repository_interfaces.item import ItemRepository
from app.infrastructure.repositories.postgres_item_repository import PostgresItemRepository
from app.services.item_service import ItemService

async def get_item_repository(
    session: AsyncSession = Depends(get_session),
) -> ItemRepository:
    return PostgresItemRepository(session)

async def get_item_service(
    repo: ItemRepository = Depends(get_item_repository),
) -> ItemService:
    return ItemService(repo)
