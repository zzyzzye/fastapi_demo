from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_active_user
from app.schemas.user import UserCreate, UserOut, Token
from app.services.user_service import UserService
from app.core.exceptions import ValidationException

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    service = UserService(db)
    try:
        return service.create_user(user_in)
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """用户登录"""
    service = UserService(db)
    user = service.authenticate(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = service.create_access_token(user["id"])
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: dict = Depends(get_current_active_user)):
    """获取当前用户信息"""
    return current_user
