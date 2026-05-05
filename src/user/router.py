from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from src.user import controller
from src.user.dtos import UserSchema as User, UserResponseSchema as UserResponse, UserLoginSchema as UserLogin
from src.utils.db import get_db

user_routes = APIRouter(prefix="/users")

@user_routes.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(body: User, db: Session = Depends(get_db)):
    return controller.register_user(body, db)

@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login_user(body: UserLogin, db: Session = Depends(get_db)):
    return controller.login_user(body, db)

@user_routes.get("/is_authenticated", response_model=UserResponse, status_code=status.HTTP_200_OK)
def is_authenticated(request: Request, db: Session = Depends(get_db)):
    return controller.is_authenticated(request, db)
