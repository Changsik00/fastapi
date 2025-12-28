from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.domain.models.item import Item, ItemCreate
from src.domain.repositories.item import ItemRepository
from src.infrastructure.repositories.in_memory_item_repository import InMemoryItemRepository

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

# ...
# In a real app, this might be a module-level variable
# or managed by a more sophisticated dependency injection container.
_in_memory_item_repository = InMemoryItemRepository()

def get_item_repository() -> ItemRepository:
    return _in_memory_item_repository

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, item_repository: ItemRepository = Depends(get_item_repository)):
    return item_repository.create(item)

@router.get("/", response_model=List[Item])
def read_items(item_repository: ItemRepository = Depends(get_item_repository)):
    return item_repository.get_all()

@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int, item_repository: ItemRepository = Depends(get_item_repository)):
    item = item_repository.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate, item_repository: ItemRepository = Depends(get_item_repository)):
    updated_item = item_repository.update(item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(item_id: int, item_repository: ItemRepository = Depends(get_item_repository)):
    deleted_item = item_repository.delete(item_id)
    if deleted_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"message": "Item deleted successfully"} # OpenAPI contract says string message

