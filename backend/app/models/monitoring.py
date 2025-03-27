from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base

class PigHouse(Base):
    """猪舍模型"""
    __tablename__ = "pig_houses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    capacity = Column(Integer, default=0)
    current_count = Column(Integer, default=0)
    status = Column(String(20), default="normal")  # normal, warning, error
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    environment_records = relationship("EnvironmentRecord", back_populates="pig_house")
    pigs = relationship("Pig", back_populates="pig_house")

class EnvironmentRecord(Base):
    """环境记录模型"""
    __tablename__ = "environment_records"
    
    id = Column(Integer, primary_key=True, index=True)
    pig_house_id = Column(Integer, ForeignKey("pig_houses.id"), nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    ammonia = Column(Float)
    co2 = Column(Float)
    light = Column(Float)
    noise = Column(Float)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    pig_house = relationship("PigHouse", back_populates="environment_records")

class AlertLevel(str, enum.Enum):
    """告警级别枚举"""
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"

class AlertStatus(str, enum.Enum):
    """告警状态枚举"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"

class Alert(Base):
    """告警模型"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    pig_house_id = Column(Integer, ForeignKey("pig_houses.id"))
    type = Column(String(50), nullable=False)
    level = Column(Enum(AlertLevel), default=AlertLevel.INFO)
    message = Column(Text, nullable=False)
    details = Column(Text)
    status = Column(Enum(AlertStatus), default=AlertStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    acknowledged_at = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))
    acknowledged_by = Column(Integer, ForeignKey("users.id"))
    resolved_by = Column(Integer, ForeignKey("users.id"))
    
    # 关系
    pig_house = relationship("PigHouse")
    acknowledger = relationship("User", foreign_keys=[acknowledged_by])
    resolver = relationship("User", foreign_keys=[resolved_by])

class Device(Base):
    """设备模型"""
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    device_type = Column(String(50), nullable=False)
    model = Column(String(100))
    serial_number = Column(String(100), unique=True)
    pig_house_id = Column(Integer, ForeignKey("pig_houses.id"))
    status = Column(String(20), default="online")  # online, offline, maintenance
    last_online = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    pig_house = relationship("PigHouse")

class Camera(Base):
    """摄像头模型"""
    __tablename__ = "cameras"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    pig_house_id = Column(Integer, ForeignKey("pig_houses.id"))
    status = Column(String(20), default="online")  # online, offline
    last_online = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    pig_house = relationship("PigHouse") 