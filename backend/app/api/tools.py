"""模板、反馈、提醒、进度聚合"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.entities import Feedback, ProgressItem, Reminder, Template
from app.schemas.schemas import (
    FeedbackIn, FeedbackOut, ProgressIn, ProgressOut, ReminderIn, ReminderOut,
    TemplateOut,
)

router = APIRouter(tags=["tools"])


# ---- 模板 ----
@router.get("/templates", response_model=List[TemplateOut])
def list_templates(
    template_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Template).filter(Template.is_active.is_(True))
    if template_type:
        query = query.filter(Template.template_type == template_type)
    return query.order_by(Template.id).all()


@router.get("/templates/{template_id}", response_model=TemplateOut)
def get_template(template_id: int, db: Session = Depends(get_db)):
    t = db.query(Template).filter(Template.id == template_id, Template.is_active.is_(True)).first()
    if not t:
        raise HTTPException(status_code=404, detail="模板不存在")
    return t


# ---- 反馈 ----
@router.post("/feedbacks", response_model=FeedbackOut)
def create_feedback(payload: FeedbackIn, db: Session = Depends(get_db)):
    fb = Feedback(**payload.model_dump())
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb


# ---- 提醒（可选同步） ----
@router.get("/reminders", response_model=List[ReminderOut])
def list_reminders(device_id: str = Query(...), db: Session = Depends(get_db)):
    return db.query(Reminder).filter(Reminder.device_id == device_id).order_by(Reminder.remind_date).all()


@router.post("/reminders", response_model=ReminderOut)
def create_reminder(payload: ReminderIn, db: Session = Depends(get_db)):
    r = Reminder(**payload.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@router.put("/reminders/{reminder_id}", response_model=ReminderOut)
def update_reminder(reminder_id: int, payload: ReminderIn, db: Session = Depends(get_db)):
    r = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="提醒不存在")
    for k, v in payload.model_dump().items():
        setattr(r, k, v)
    db.commit()
    db.refresh(r)
    return r


@router.delete("/reminders/{reminder_id}")
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    r = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="提醒不存在")
    db.delete(r)
    db.commit()
    return {"ok": True}


# ---- 进度聚合 ----
@router.get("/progress", response_model=List[ProgressOut])
def list_progress(device_id: str = Query(...), db: Session = Depends(get_db)):
    return db.query(ProgressItem).filter(ProgressItem.device_id == device_id).order_by(ProgressItem.created_at.desc()).all()


@router.post("/progress", response_model=ProgressOut)
def create_progress(payload: ProgressIn, db: Session = Depends(get_db)):
    p = ProgressItem(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.delete("/progress/{progress_id}")
def delete_progress(progress_id: int, db: Session = Depends(get_db)):
    p = db.query(ProgressItem).filter(ProgressItem.id == progress_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="记录不存在")
    db.delete(p)
    db.commit()
    return {"ok": True}
