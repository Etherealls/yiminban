"""分类与区县查询"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.entities import Category, District
from app.schemas.schemas import CategoryOut, DistrictOut

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/categories", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    """获取办事分类列表"""
    return db.query(Category).order_by(Category.sort_order).all()


@router.get("/districts", response_model=List[DistrictOut])
def list_districts(db: Session = Depends(get_db)):
    """获取区县列表（用于本地化材料清单）"""
    return db.query(District).order_by(District.sort_order).all()
