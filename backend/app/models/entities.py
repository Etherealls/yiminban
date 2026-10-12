"""数据模型定义（SQLAlchemy ORM）

设计说明：
- 本系统为「办事向导」，不替代政务系统、不办理业务；
- 事项库由后台人工维护，用户反馈用于信息自迭代；
- 用户数据（证件提醒、进度卡片、收藏）以本地存储为主，仅可选同步到服务端。
"""
from datetime import datetime

from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, String, Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Category(Base):
    """办事分类"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), unique=True, index=True, nullable=False, comment="分类编码")
    name = Column(String(64), nullable=False, comment="分类名称")
    icon = Column(String(64), nullable=True, comment="图标标识")
    color = Column(String(16), nullable=True, comment="主题色")
    sort_order = Column(Integer, default=0, comment="排序")
    description = Column(String(255), nullable=True, comment="分类说明")

    items = relationship("Matter", back_populates="category")


class District(Base):
    """区县（用于生成本地化材料清单）"""
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), unique=True, index=True, nullable=False, comment="区县编码")
    name = Column(String(64), nullable=False, comment="区县名称")
    city = Column(String(64), nullable=True, comment="所属城市")
    province = Column(String(64), nullable=True, comment="所属省份")
    sort_order = Column(Integer, default=0)

    windows = relationship("ServiceWindow", back_populates="district")


class Matter(Base):
    """办事事项"""
    __tablename__ = "matters"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    code = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(128), nullable=False, comment="事项名称")
    short_name = Column(String(64), nullable=True, comment="简称/高频称呼")
    summary = Column(String(255), nullable=True, comment="一句话说明")
    description = Column(Text, nullable=True, comment="详细说明")

    # 办理属性
    is_online = Column(Boolean, default=False, comment="是否支持线上办理")
    is_offline = Column(Boolean, default=False, comment="是否需线下窗口")
    fee_type = Column(String(16), default="free", comment="收费类型: free/charged/mixed")
    fee_desc = Column(String(255), nullable=True, comment="收费标准说明")
    time_limit = Column(String(64), nullable=True, comment="办理时限")
    legal_basis = Column(Text, nullable=True, comment="办理依据")

    # 官方原文溯源
    official_title = Column(String(255), nullable=True, comment="官方原文标题")
    official_url = Column(String(512), nullable=True, comment="官方原文链接")
    official_source = Column(String(128), nullable=True, comment="来源单位")

    # 预约提示
    need_appointment = Column(Boolean, default=False, comment="是否需提前预约")
    appointment_note = Column(String(255), nullable=True, comment="预约说明")

    # 适老模式
    is_high_frequency = Column(Boolean, default=False, comment="是否高频事项（适老模式展示）")
    elderly_tip = Column(String(255), nullable=True, comment="适老提示")

    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="items")
    materials = relationship("Material", back_populates="matter")
    pitfalls = relationship("Pitfall", back_populates="matter")
    windows = relationship("ServiceWindow", back_populates="matter")


class Material(Base):
    """材料要求"""
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    matter_id = Column(Integer, ForeignKey("matters.id"), index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True, index=True)

    name = Column(String(128), nullable=False, comment="材料名称")
    material_type = Column(String(16), default="required", comment="必备/可选: required/optional")
    copy_requirement = Column(String(32), default="original", comment="原件/复印件/原件+复印件/电子版")
    need_electronic = Column(Boolean, default=False, comment="是否需电子版")
    quantity = Column(Integer, default=1, comment="份数")
    note = Column(String(255), nullable=True, comment="备注")
    sort_order = Column(Integer, default=0)

    matter = relationship("Matter", back_populates="materials")


class Pitfall(Base):
    """避坑提示（高频驳回原因、常见误区）"""
    __tablename__ = "pitfalls"

    id = Column(Integer, primary_key=True, index=True)
    matter_id = Column(Integer, ForeignKey("matters.id"), index=True)
    title = Column(String(128), nullable=False, comment="提示标题")
    content = Column(Text, nullable=True, comment="提示内容")
    tag = Column(String(32), nullable=True, comment="标签：驳回/照片/时间/材料等")
    sort_order = Column(Integer, default=0)

    matter = relationship("Matter", back_populates="pitfalls")


class ServiceWindow(Base):
    """办事窗口（地址、时间、电话、交通）"""
    __tablename__ = "service_windows"

    id = Column(Integer, primary_key=True, index=True)
    matter_id = Column(Integer, ForeignKey("matters.id"), index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), index=True)

    name = Column(String(128), nullable=False, comment="窗口/网点名称")
    address = Column(String(255), nullable=False, comment="地址")
    office_time = Column(String(128), nullable=True, comment="办公时间")
    phone = Column(String(64), nullable=True, comment="联系电话")
    parking = Column(String(255), nullable=True, comment="周边停车提示")
    bus = Column(String(255), nullable=True, comment="公交/地铁提示")
    appointment_url = Column(String(512), nullable=True, comment="预约入口（小程序/链接）")
    queue_note = Column(String(255), nullable=True, comment="取号排队参考")

    district = relationship("District", back_populates="windows")
    matter = relationship("Matter", back_populates="windows")


class Template(Base):
    """材料模板（仅供参考）"""
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(64), unique=True, index=True)
    name = Column(String(128), nullable=False, comment="模板名称")
    template_type = Column(String(32), comment="申请书/情况说明/承诺书等")
    content = Column(Text, nullable=False, comment="模板正文")
    usage_note = Column(String(255), nullable=True, comment="使用说明")
    disclaimer = Column(String(255), default="本模板仅供参考，以窗口最终要求为准", comment="免责声明")
    is_active = Column(Boolean, default=True)


class Feedback(Base):
    """用户反馈纠错"""
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    matter_id = Column(Integer, ForeignKey("matters.id"), nullable=True, index=True)
    feedback_type = Column(String(32), comment="信息过时/材料变更/窗口不一致/其他")
    content = Column(Text, nullable=False, comment="反馈内容")
    contact = Column(String(128), nullable=True, comment="联系方式（可选）")
    status = Column(String(16), default="pending", comment="pending/reviewing/accepted/rejected")
    reviewer_note = Column(String(255), nullable=True, comment="审核备注")
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)


class Reminder(Base):
    """证件/事项提醒（服务端可选同步，本地为主）"""
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(64), index=True, comment="设备标识（本地存储主键）")
    title = Column(String(128), nullable=False, comment="提醒标题")
    reminder_type = Column(String(32), default="matter", comment="证件/事项/其他")
    remind_date = Column(DateTime, nullable=False, comment="到期/提醒日期")
    advance_days = Column(Integer, default=7, comment="提前天数")
    note = Column(String(255), nullable=True)
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ProgressItem(Base):
    """进度聚合卡片（仅聚合跳转，不对接政务API）"""
    __tablename__ = "progress_items"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(64), index=True)
    title = Column(String(128), nullable=False, comment="事项名称")
    category_code = Column(String(32), nullable=True)
    platform = Column(String(64), nullable=True, comment="对应官方平台")
    platform_url = Column(String(512), nullable=True, comment="跳转链接")
    status = Column(String(32), default="processing", comment="办理中/已办结等")
    note = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
