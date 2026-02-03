from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, status
from app.db.database import users, items, orders
from app.models import User, Item, Order


router = APIRouter()

# make a user

# delete a user