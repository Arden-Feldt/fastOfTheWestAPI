from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from app.models import User, Order, Item
from app.routers import user_router, item_router, order_router
from app.db.database import _test_db as database


@asynccontextmanager
async def lifespan(app: FastAPI):
    frodo = User(id=0, name="Frodo", password="password")
    galadriel = User(id=1, name="Galadriel", password="password")

    ring = Item(id=0, name="ring", cost=10)
    sting = Item(id=1, name="sting", cost=15)
    palantir = Item(id=2, name="palantir", cost=25)

    database["users"].extend([frodo, galadriel])
    database["items"].extend([ring, sting, palantir])
    database["orders"].extend(
        [
            Order(id=0, user_id=0, item_id=0),
            Order(id=1, user_id=0, item_id=1),
            Order(id=2, user_id=1, item_id=2),
        ]
    )

    yield

    database["users"].clear()
    database["items"].clear()
    database["orders"].clear()


app = FastAPI(lifespan=lifespan)  # remove lifespan when db is added

app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(item_router.router, prefix="/items", tags=["items"])
app.include_router(order_router.router, prefix="/orders", tags={"orders"})


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {
        '"This task was appointed to you. And if you do not find a way, no one will." — Galadriel, The Fellowship of the Ring'
    }
