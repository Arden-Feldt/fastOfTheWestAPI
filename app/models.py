from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    password: str

class Item(BaseModel):
    id: int
    name: str
    cost: float 

class Order(BaseModel):
    id: int
    user: User
    item: Item
    # date perhaps?
