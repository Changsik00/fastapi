from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.item import Item, ItemCreate

class ItemRepository(ABC):

    @abstractmethod
    def create(self, item: ItemCreate) -> Item:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[Item]:
        pass

    @abstractmethod
    def get_all(self) -> List[Item]:
        pass

    @abstractmethod
    def update(self, item_id: int, item: ItemCreate) -> Optional[Item]:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> Optional[Item]:
        pass
