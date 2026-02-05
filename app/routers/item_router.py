from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from app.models import Item
from app.db.database import get_db

router = APIRouter()


# Get available items
@router.get("/", status_code=status.HTTP_200_OK)
def get_items(db: dict = Depends(get_db)):
    return db["items"]


# Get an item
@router.get("/{item_id}", status_code=status.HTTP_200_OK)
def get_item(item_id: int, db: dict = Depends(get_db)):
    for item in db["items"]:
        if item.id == item_id:
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"item with id {item_id} not found",
    )


# Add an item to inventory
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item, db: dict = Depends(get_db)):
    if any(i.id == item.id for i in db["items"]):
        raise HTTPException(status_code=400, detail="Item already exists")
    db["items"].append(item)
    return item


# Delete and item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(item_id: int, db: dict = Depends(get_db)):
    for item in db["items"]:
        if item.id == item_id:
            db["items"].remove(item)
            return None
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"No item with id {item_id}"
    )


# update price
@router.put("/{item_id}", status_code=status.HTTP_200_OK)
def update_price(item_id: int, price: int, db: dict = Depends(get_db)):
    for item in db["items"]:
        if item.id == item_id:
            item.cost = price
            return item
    raise HTTPException(
        status_code=404, detail=f"Could not find item with id: {item_id}"
    )
