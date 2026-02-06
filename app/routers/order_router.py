from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from app.db.database import get_db
from app.models import Item, Order, Order_Create, User
from sqlalchemy.orm import Session

router = APIRouter()

# Make an order
@router.post("/", status_code=status.HTTP_201_CREATED)
def make_order(order: Order_Create, db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(order.user_id == User.id).first()
    if not user_exist:
        raise HTTPException(status_code=404, detail=f"User {order.user_id} not found")
    
    item_exist = db.query(Item).filter(Item.id == order.item_id).first()
    if not item_exist:
        raise HTTPException(status_code=404, detail=f"Item {order.item_id} not found")

    new_order = Order(user_id = order.user_id, item_id = order.item_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# Get all orders for any or all users
@router.get("/", status_code=status.HTTP_200_OK)
def get_users_orders(user_id: int | None = None, db: Session = Depends(get_db)):
    if user_id is None:
        return db.query(Order).all()
    user_exist = db.query(User).filter(user_id == User.id).first()
    if not user_exist:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return db.query(Order).filter(user_id == Order.user_id).all()


# Delete an order
@router.delete("/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_order(order_id: int, db: Session = Depends(get_db)):
    removed_order = db.query(Order).filter(order_id == Order.id).first()
    if not removed_order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")    
    db.delete(removed_order)
    db.commit()
