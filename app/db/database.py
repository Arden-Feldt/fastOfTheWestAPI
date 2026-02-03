from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Item, Order, User

items: list[Item] = []
orders: list[Order] = []
users: list[User] = []  