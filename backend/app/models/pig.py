from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.db.database import Base

class PigGender(str, enum.Enum):
    """猪性别枚举"""
    MALE = "male"
    FEMALE = "female"

class PigHealthStatus(str, enum.Enum):
    """猪健康状态枚举"""
    HEALTHY = "healthy"
    ATTENTION = "attention"
    SICK = "sick"
    TREATMENT = "treatment"
    ISOLATION = "isolation"

class Pig(Base):
    """猪模型"""
    __tablename__ = "pigs"
    
    id = Column(Integer, primary_key=True, index=True)
    ear_tag = Column(String(50), unique=True, index=True, nullable=False)
    gender = Column(Enum(PigGender), nullable=False)
    breed = Column(String(100))
    birth_date = Column(Date)
    entry_date = Column(Date)
    entry_weight = Column(Float)
    current_weight = Column(Float)
    health_status = Column(Enum(PigHealthStatus), default=PigHealthStatus.HEALTHY)
    pig_house_id = Column(Integer, ForeignKey("pig_houses.id"))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    pig_house = relationship("PigHouse", back_populates="pigs")
    weight_records = relationship("WeightRecord", back_populates="pig")
    health_records = relationship("HealthRecord", back_populates="pig")

class WeightRecord(Base):
    """体重记录模型"""
    __tablename__ = "weight_records"
    
    id = Column(Integer, primary_key=True, index=True)
    pig_id = Column(Integer, ForeignKey("pigs.id"), nullable=False)
    weight = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    recorded_by = Column(Integer, ForeignKey("users.id"))
    
    # 关系
    pig = relationship("Pig", back_populates="weight_records")
    recorder = relationship("User")

class HealthRecord(Base):
    """健康记录模型"""
    __tablename__ = "health_records"
    
    id = Column(Integer, primary_key=True, index=True)
    pig_id = Column(Integer, ForeignKey("pigs.id"), nullable=False)
    status = Column(Enum(PigHealthStatus), nullable=False)
    temperature = Column(Float)
    symptoms = Column(Text)
    diagnosis = Column(Text)
    treatment = Column(Text)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    recorded_by = Column(Integer, ForeignKey("users.id"))
    
    # 关系
    pig = relationship("Pig", back_populates="health_records")
    recorder = relationship("User")

class FeedingRecord(Base):
    """饲喂记录模型"""
    __tablename__ = "feeding_records"
    
    id = Column(Integer, primary_key=True, index=True)
    pig_house_id = Column(Integer, ForeignKey("pig_houses.id"), nullable=False)
    feed_type = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)  # 单位：kg
    feeding_time = Column(DateTime(timezone=True), server_default=func.now())
    recorded_by = Column(Integer, ForeignKey("users.id"))
    
    # 关系
    pig_house = relationship("PigHouse")
    recorder = relationship("User")

class FeedStock(Base):
    """饲料库存模型"""
    __tablename__ = "feed_stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    feed_type = Column(String(50), nullable=False)
    current_amount = Column(Float, nullable=False)
    capacity = Column(Float, nullable=False)
    last_refill_date = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now) 