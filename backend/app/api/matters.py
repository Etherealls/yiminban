"""办事事项查询"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models.entities import Matter
from app.schemas.schemas import MatterBrief, MatterDetail

router = APIRouter(prefix="/matters", tags=["matters"])


@router.get("", response_model=List[MatterBrief])
def list_matters(
    category_code: Optional[str] = Query(None, description="分类编码"),
    district_code: Optional[str] = Query(None, description="区县编码"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    high_frequency: Optional[bool] = Query(None, description="仅高频事项"),
    db: Session = Depends(get_db),
):
    """事项列表（支持分类/区县/关键词/高频筛选）"""
    query = db.query(Matter).filter(Matter.is_active.is_(True))

    if category_code:
        query = query.join(Matter.category).filter(
            Matter.category.has(code=category_code)
        )
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(
            Matter.name.like(like) | Matter.short_name.like(like) | Matter.summary.like(like)
        )
    if high_frequency is not None:
        query = query.filter(Matter.is_high_frequency.is_(high_frequency))

    items = query.order_by(Matter.sort_order, Matter.id).all()
    return items


@router.get("/{matter_id}", response_model=MatterDetail)
def get_matter(
    matter_id: int,
    district_code: Optional[str] = Query(None, description="区县编码，用于本地化材料清单"),
    db: Session = Depends(get_db),
):
    """事项详情（含本地化材料、避坑、窗口）"""
    matter = (
        db.query(Matter)
        .options(
            joinedload(Matter.category),
            joinedload(Matter.materials),
            joinedload(Matter.pitfalls),
            joinedload(Matter.windows),
        )
        .filter(Matter.id == matter_id, Matter.is_active.is_(True))
        .first()
    )
    if not matter:
        raise HTTPException(status_code=404, detail="事项不存在")

    # 按区县过滤材料与窗口（未指定区县时返回通用项）
    if district_code:
        from app.models.entities import District

        district = db.query(District).filter(District.code == district_code).first()
        if district:
            matter.materials = sorted(
                [m for m in matter.materials if m.district_id in (None, district.id)],
                key=lambda x: x.sort_order,
            )
            matter.windows = sorted(
                [w for w in matter.windows if w.district_id in (None, district.id)],
                key=lambda x: x.id,
            )
    return matter
