from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import Item


class ItemRepository:
    """项目数据访问层"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, item_id: int) -> Optional[Item]:
        """根据ID获取项目"""
        return self.db.query(Item).filter(Item.id == item_id).first()

    def get_multi_by_owner(
        self, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        """获取用户的项目列表"""
        return (
            self.db.query(Item)
            .filter(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, obj_in: dict, owner_id: int) -> Item:
        """创建项目"""
        db_obj = Item(**obj_in, owner_id=owner_id)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: Item, obj_in: dict) -> Item:
        """更新项目"""
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, item_id: int) -> bool:
        """删除项目"""
        obj = self.get_by_id(item_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
