from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, status
from app.db.database import users, orders
from app.models import User, Item, Order

router = APIRouter()

# Make an order
@router.post("/", status_code = status.HTTP_201_CREATED)
def make_order(order: Order):
    orders.append(order)
    return order

# Get all orders for any or all users
@router.get("/", status_code = status.HTTP_200_OK)
def get_users_orders(user_id: int | None = None):
    if user_id is None:
        return orders
    if user_id not in [u.id for u in users]:
        raise HTTPException(status_code=404, detail="User not found")
    user_orders = []
    for order in orders:
        if order.user.id == user_id:
            user_orders.append(order)
    return user_orders

# Delete an order
@router.delete("/order/{order_id}", status_code = status.HTTP_204_NO_CONTENT)
def remove_order(order_id: int):
    if order_id not in [o.id for o in orders]:
        raise HTTPException(status_code=404, detail="Order not found")
    for order in orders:
        if order.id == order_id:
            orders.remove(order)
