from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_active_user
from app.schemas.user import ItemCreate, ItemOut, ItemUpdate
from app.services.item_service import ItemService
from app.core.exceptions import NotFoundException, ValidationException

router = APIRouter()


@router.post("/", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(
    item_in: ItemCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    """创建项目"""
    service = ItemService(db)
    return service.create_item(item_in, current_user["id"])


@router.get("/", response_model=List[ItemOut])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    """获取当前用户的项目列表"""
    service = ItemService(db)
    return service.get_user_items(current_user["id"], skip, limit)


@router.get("/{item_id}", response_model=ItemOut)
def read_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    """获取项目详情"""
    service = ItemService(db)
    try:
        return service.get_item(item_id, current_user["id"])
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.put("/{item_id}", response_model=ItemOut)
def update_item(
    item_id: int,
    item_in: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    """更新项目"""
    service = ItemService(db)
    try:
        return service.update_item(item_id, item_in, current_user["id"])
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    """删除项目"""
    service = ItemService(db)
    try:
        service.delete_item(item_id, current_user["id"])
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
