from fastapi import APIRouter
from pydantic import BaseModel
from jose import jwt

from services.user_service import load_users, save_users

router = APIRouter()

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

class User(BaseModel):
    username: str
    password: str


@router.post("/signup")
def signup(user: User):
    users = load_users()

    for u in users:
        if u["username"] == user.username:
            return {"message": "exists"}

    users.append(user.dict())
    save_users(users)

    return {"message": "created"}


@router.post("/login")
def login(user: User):
    users = load_users()

    for u in users:
        if u["username"] == user.username and u["password"] == user.password:

            token = jwt.encode(
                {"username": user.username},
                SECRET_KEY,
                algorithm=ALGORITHM
            )

            return {
                "access_token": token,
                "token_type": "bearer"
            }

    return {"message": "invalid"}