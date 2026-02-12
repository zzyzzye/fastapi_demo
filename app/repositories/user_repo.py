from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    """用户数据访问层"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.db.query(User).filter(User.email == email).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[User]:
        """获取多个用户"""
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> User:
        """创建用户"""
        db_obj = User(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: User, obj_in: dict) -> User:
        """更新用户"""
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, user_id: int) -> bool:
        """删除用户"""
        obj = self.get_by_id(user_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
