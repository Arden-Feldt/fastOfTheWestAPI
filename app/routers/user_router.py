from fastapi import APIRouter, Depends
from fastapi import HTTPException
from app.db.database import get_db
from app.models import ResetPassword, User
from sqlalchemy.orm import Session


router = APIRouter()

# get users
@router.get("/", status_code=200)
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()



# make a user

# delete a user


# update password (inevitable tbh)
@router.put("/{user_id}", status_code=201)
def reset_password(user_id: int, data: ResetPassword, db: dict = Depends(get_db)):
    for user in db["users"]:
        if user.id == user_id:
            user.password = data.password
            return {
                f"user {user.name} with id: {user.id} has had their password updated"
            }
    raise HTTPException(404, detail=f"Could not find user with id: {user_id}")
