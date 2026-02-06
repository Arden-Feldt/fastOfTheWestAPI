from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from app.models import Item, Item_Create
from app.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


# Get available items
@router.get("/", status_code=status.HTTP_200_OK)
def get_items(db: dict = Depends(get_db)):
    return db.query(Item).all()


# Get an item
@router.get("/{item_id}", status_code=status.HTTP_200_OK)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item


# Add an item to inventory
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item_Create, db: Session = Depends(get_db)):
    exists = db.query(Item).filter(Item.id == item.id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Item already exists")
    
    new_item = Item(name=item.name, cost=item.cost)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# Delete and item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")    
    db.delete(item)
    db.commit()
    return None


# update price
@router.put("/{item_id}", status_code=status.HTTP_200_OK)
def update_price(item_id: int, price: int, db: dict = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    
    item.cost = price
    db.commit()
    db.refresh(item)
    return item
