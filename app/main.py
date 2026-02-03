from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from pydantic import BaseModel
from app.models import User, Order, Item


items: list[Item] = []

orders: list[Order] = []

users: list[User] = []  

@asynccontextmanager
async def lifespan(app: FastAPI):
    frodo = User(id=0, name="Frodo", password="password")
    galadriel = User(id=1, name="Galadriel", password="password")

    users.extend([frodo, galadriel])

    ring = Item(id=0, name="ring", cost=10)
    sting = Item(id=1, name="sting", cost=15)
    palantir = Item(id=2, name="palantir", cost=25)

    items.extend([ring, sting, palantir])

    orders.extend([
        Order(id=0, user=frodo, item=ring),
        Order(id=1, user=frodo, item=sting),
        Order(id=2, user=galadriel, item=palantir),
    ])

    yield

    # shut it down
    users.clear()
    items.clear()

app = FastAPI(lifespan=lifespan) # remove lifespan when db is added

### user

### order 

# Make an order
@app.post("/order", status_code = status.HTTP_201_CREATED)
def make_order(order: Order):
    orders.append(order)
    return order

# Delete an order
@app.delete("/order/{order_id}", status_code = status.HTTP_204_NO_CONTENT)
def remove_order(order_id: int):
    if order_id not in [o.id for o in orders]:
        raise HTTPException(status_code=404, detail="Order not found")
    for order in orders:
        if order.id == order_id:
            orders.remove(order)

# Get all orders for any or all users
@app.get("/orders", status_code = status.HTTP_200_OK)
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

### item

# Add an item to inventory
@app.post("/item", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    if item.id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items.append(item)
    return item

# Delete and item
@app.delete("/item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(item_id: int):
    if item_id not in [i.id for i in items]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No item with id {item_id}")
    for item in items:
        if item.id == item_id:
            items.remove(item)