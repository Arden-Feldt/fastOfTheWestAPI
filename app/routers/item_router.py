from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, status
from app.db.database import items
from app.models import User, Item, Order

router = APIRouter()

# Add an item to inventory
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    if item.id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items.append(item)
    return item

# Delete and item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(item_id: int):
    if item_id not in [i.id for i in items]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No item with id {item_id}")
    for item in items:
        if item.id == item_id:
            items.remove(item)