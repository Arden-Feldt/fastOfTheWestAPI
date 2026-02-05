from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from app.db.database import get_db
from app.models import Order

router = APIRouter()


# Make an order
@router.post("/", status_code=status.HTTP_201_CREATED)
def make_order(order: Order, db: dict = Depends(get_db)):
    # trusting user to submit a valid order :shrug:
    db["orders"].append(order)
    return order


# Get all orders for any or all users
@router.get("/", status_code=status.HTTP_200_OK)
def get_users_orders(user_id: int | None = None, db: dict = Depends(get_db)):
    if user_id is None:
        return db["orders"]
    if user_id not in [u.id for u in db["users"]]:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    user_orders = []
    for order in db["orders"]:
        if order.user_id == user_id:
            user_orders.append(order)
    return user_orders


# Delete an order
@router.delete("/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_order(order_id: int, db: dict = Depends(get_db)):
    removed_order = None
    for order in db["orders"]:
        if order.id == order_id:
            removed_order = order
            db["orders"].remove(removed_order)
    if not removed_order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return None
