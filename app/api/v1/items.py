from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_item_service
from app.domain.models.item import Item, ItemCreate
from app.services.item_service import ItemService

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, service: ItemService = Depends(get_item_service)):
    return await service.create_item(item)

@router.get("/", response_model=List[Item])
async def read_items(service: ItemService = Depends(get_item_service)):
    return await service.get_items()

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int, service: ItemService = Depends(get_item_service)):
    item = await service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate, service: ItemService = Depends(get_item_service)):
    updated_item = await service.update_item(item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_item(item_id: int, service: ItemService = Depends(get_item_service)):
    deleted_item = await service.delete_item(item_id)
    if deleted_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"message": "Item deleted successfully"}
