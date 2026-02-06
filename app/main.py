from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from app.models import User, Order, Item
from app.routers import user_router, item_router, order_router
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)  # remove lifespan when db is added

app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(item_router.router, prefix="/items", tags=["items"])
app.include_router(order_router.router, prefix="/orders", tags={"orders"})


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {
        '"This task was appointed to you. And if you do not find a way, no one will." — Galadriel, The Fellowship of the Ring'
    }
