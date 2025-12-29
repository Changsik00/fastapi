from typing import List, Optional, Dict
from src.domain.models.item import Item, ItemCreate
from src.domain.repositories.item import ItemRepository

class InMemoryItemRepository(ItemRepository):
    def __init__(self):
        self._items: Dict[int, Item] = {}
        self._next_id = 1

    def create(self, item: ItemCreate) -> Item:
        new_item = Item(id=self._next_id, **item.model_dump())
        self._items[self._next_id] = new_item
        self._next_id += 1
        return new_item

    def get_by_id(self, item_id: int) -> Optional[Item]:
        return self._items.get(item_id)

    def get_all(self) -> List[Item]:
        return list(self._items.values())

    def update(self, item_id: int, item_update: ItemCreate) -> Optional[Item]:
        if item_id in self._items:
            item = self._items[item_id]
            item.name = item_update.name
            item.description = item_update.description
            self._items[item_id] = item
            return item
        return None

    def delete(self, item_id: int) -> Optional[Item]:
        return self._items.pop(item_id, None)
