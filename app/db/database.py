from app.models import Item, Order, User
from typing import Generator

items: list[Item] = []
orders: list[Order] = []
users: list[User] = []

_test_db = {"users": [], "items": [], "orders": []}


def get_db() -> Generator:
    db = _test_db
    try:
        # pass db
        yield db
    finally:
        # close db
        pass
