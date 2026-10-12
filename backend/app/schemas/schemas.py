"""Pydantic 响应/请求模型"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# ---- 分类 ----
class CategoryOut(BaseModel):
    id: int
    code: str
    name: str
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# ---- 区县 ----
class DistrictOut(BaseModel):
    id: int
    code: str
    name: str
    city: Optional[str] = None
    province: Optional[str] = None

    class Config:
        from_attributes = True


# ---- 材料 ----
class MaterialOut(BaseModel):
    id: int
    name: str
    material_type: str
    copy_requirement: str
    need_electronic: bool
    quantity: int
    note: Optional[str] = None

    class Config:
        from_attributes = True


# ---- 避坑 ----
class PitfallOut(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    tag: Optional[str] = None

    class Config:
        from_attributes = True


# ---- 窗口 ----
class WindowOut(BaseModel):
    id: int
    name: str
    address: str
    office_time: Optional[str] = None
    phone: Optional[str] = None
    parking: Optional[str] = None
    bus: Optional[str] = None
    appointment_url: Optional[str] = None
    queue_note: Optional[str] = None

    class Config:
        from_attributes = True


# ---- 事项 ----
class MatterBrief(BaseModel):
    id: int
    code: str
    name: str
    short_name: Optional[str] = None
    summary: Optional[str] = None
    fee_type: str
    time_limit: Optional[str] = None
    is_online: bool
    is_offline: bool
    need_appointment: bool
    is_high_frequency: bool

    class Config:
        from_attributes = True


class MatterDetail(MatterBrief):
    description: Optional[str] = None
    fee_desc: Optional[str] = None
    legal_basis: Optional[str] = None
    official_title: Optional[str] = None
    official_url: Optional[str] = None
    official_source: Optional[str] = None
    appointment_note: Optional[str] = None
    elderly_tip: Optional[str] = None
    category: Optional[CategoryOut] = None
    materials: List[MaterialOut] = []
    pitfalls: List[PitfallOut] = []
    windows: List[WindowOut] = []

    class Config:
        from_attributes = True


# ---- 模板 ----
class TemplateOut(BaseModel):
    id: int
    code: str
    name: str
    template_type: str
    content: str
    usage_note: Optional[str] = None
    disclaimer: Optional[str] = None

    class Config:
        from_attributes = True


# ---- 反馈 ----
class FeedbackIn(BaseModel):
    matter_id: Optional[int] = None
    feedback_type: str = "other"
    content: str
    contact: Optional[str] = None


class FeedbackOut(BaseModel):
    id: int
    matter_id: Optional[int] = None
    feedback_type: str
    content: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---- 提醒 ----
class ReminderIn(BaseModel):
    device_id: str
    title: str
    reminder_type: str = "matter"
    remind_date: datetime
    advance_days: int = 7
    note: Optional[str] = None


class ReminderOut(ReminderIn):
    id: int
    is_done: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---- 进度 ----
class ProgressIn(BaseModel):
    device_id: str
    title: str
    category_code: Optional[str] = None
    platform: Optional[str] = None
    platform_url: Optional[str] = None
    status: str = "processing"
    note: Optional[str] = None


class ProgressOut(ProgressIn):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---- 通用 ----
class Message(BaseModel):
    code: int = 0
    message: str = "ok"
    data: Optional[dict] = None
