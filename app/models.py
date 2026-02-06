from pydantic import BaseModel
from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from .db.database import Base
from sqlalchemy.orm import relationship


# class User(BaseModel):
#     id: int
#     name: str
#     password: str

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)

class User_Create(BaseModel):
    name: str
    password: str

class User_Response(BaseModel):
    id: int
    password: str

# class Item(BaseModel):
#     id: int
#     name: str
#     cost: float

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cost = Column(Integer)

class Item_Create(BaseModel):
    name: str
    cost: int

class Item_Return(BaseModel):
    id: int
    name: str
    cost: int
    class Config:
        from_attributes = True

# class Order(BaseModel):
#     id: int
#     user_id: int
#     item_id: int

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, Sequence("order_id_sequence", start=0, increment=1), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))

    buyer = relationship("User")
    product = relationship("Item")

class Order_Create(BaseModel):
    user_id: int
    item_id: int

class Order_Return(BaseModel):
    id: int
    user_id: int
    item_id: int
    class Config:
        from_attributes = True

###

class ResetPassword(BaseModel):
    password: str
