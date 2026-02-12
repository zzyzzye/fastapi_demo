from typing import Optional, Dict, Any
from datetime import timedelta
from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.exceptions import NotFoundException, ValidationException
from app.config import settings


class UserService:
    """用户业务逻辑层"""

    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def authenticate(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """用户认证"""
        user = self.repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return {"id": user.id, "email": user.email, "is_active": user.is_active}

    def create_access_token(self, user_id: int) -> str:
        """创建访问令牌"""
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            data={"sub": str(user_id)}, expires_delta=access_token_expires
        )

    def create_user(self, obj_in: UserCreate) -> Dict[str, Any]:
        """创建用户"""
        # 检查邮箱是否已存在
        if self.repo.get_by_email(obj_in.email):
            raise ValidationException("Email already registered")

        # 创建用户数据
        obj_data = obj_in.model_dump()
        obj_data["hashed_password"] = get_password_hash(obj_data.pop("password"))

        user = self.repo.create(obj_data)
        return {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at,
        }

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """获取用户信息"""
        user = self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at,
        }

    def update_user(self, user_id: int, obj_in: UserUpdate) -> Dict[str, Any]:
        """更新用户"""
        user = self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        update_data = obj_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        user = self.repo.update(user, update_data)
        return {"id": user.id, "email": user.email, "is_active": user.is_active}

    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        return self.repo.delete(user_id)
