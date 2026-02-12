from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.repositories.item_repo import ItemRepository
from app.schemas.user import ItemCreate, ItemUpdate
from app.core.exceptions import NotFoundException


class ItemService:
    """项目业务逻辑层"""

    def __init__(self, db: Session):
        self.repo = ItemRepository(db)

    def create_item(self, obj_in: ItemCreate, owner_id: int) -> Dict[str, Any]:
        """创建项目"""
        item = self.repo.create(obj_in.model_dump(), owner_id)
        return {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "owner_id": item.owner_id,
            "created_at": item.created_at,
        }

    def get_item(self, item_id: int, owner_id: int) -> Dict[str, Any]:
        """获取项目详情"""
        item = self.repo.get_by_id(item_id)
        if not item:
            raise NotFoundException("Item not found")
        if item.owner_id != owner_id:
            raise NotFoundException("Item not found")
        return {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "owner_id": item.owner_id,
            "created_at": item.created_at,
        }

    def get_user_items(
        self, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """获取用户的项目列表"""
        items = self.repo.get_multi_by_owner(owner_id, skip, limit)
        return [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "owner_id": item.owner_id,
                "created_at": item.created_at,
            }
            for item in items
        ]

    def update_item(
        self, item_id: int, obj_in: ItemUpdate, owner_id: int
    ) -> Dict[str, Any]:
        """更新项目"""
        item = self.repo.get_by_id(item_id)
        if not item:
            raise NotFoundException("Item not found")
        if item.owner_id != owner_id:
            raise NotFoundException("Item not found")

        update_data = obj_in.model_dump(exclude_unset=True)
        item = self.repo.update(item, update_data)
        return {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "owner_id": item.owner_id,
        }

    def delete_item(self, item_id: int, owner_id: int) -> bool:
        """删除项目"""
        item = self.repo.get_by_id(item_id)
        if not item or item.owner_id != owner_id:
            raise NotFoundException("Item not found")
        return self.repo.delete(item_id)
