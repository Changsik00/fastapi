from typing import List, Optional
from app.domain.models.item import Item, ItemCreate
from app.domain.repository_interfaces.item_repository import ItemRepository

class ItemService:
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    async def create_item(self, item: ItemCreate) -> Item:
        return await self.item_repository.create(item)

    async def get_items(self) -> List[Item]:
        return await self.item_repository.get_all()

    async def get_item(self, item_id: int) -> Optional[Item]:
        return await self.item_repository.get_by_id(item_id)

    async def update_item(self, item_id: int, item: ItemCreate) -> Optional[Item]:
        return await self.item_repository.update(item_id, item)

    async def delete_item(self, item_id: int) -> Optional[Item]:
        return await self.item_repository.delete(item_id)
