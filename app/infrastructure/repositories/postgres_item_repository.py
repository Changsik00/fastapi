from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domain.models.item import Item, ItemCreate
from app.domain.repository_interfaces.item_repository import ItemRepository

class PostgresItemRepository(ItemRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, item: ItemCreate) -> Item:
        db_item = Item.model_validate(item)
        self.session.add(db_item)
        await self.session.commit()
        await self.session.refresh(db_item)
        return db_item

    async def get_by_id(self, item_id: int) -> Optional[Item]:
        result = await self.session.execute(select(Item).where(Item.id == item_id))
        return result.scalars().first()

    async def get_all(self) -> List[Item]:
        result = await self.session.execute(select(Item))
        return list(result.scalars().all())

    async def update(self, item_id: int, item_update: ItemCreate) -> Optional[Item]:
        db_item = await self.get_by_id(item_id)
        if not db_item:
            return None
        
        item_data = item_update.model_dump(exclude_unset=True)
        for key, value in item_data.items():
            setattr(db_item, key, value)
            
        self.session.add(db_item)
        await self.session.commit()
        await self.session.refresh(db_item)
        return db_item

    async def delete(self, item_id: int) -> Optional[Item]:
        db_item = await self.get_by_id(item_id)
        if not db_item:
            return None
            
        await self.session.delete(db_item)
        await self.session.commit()
        return db_item
