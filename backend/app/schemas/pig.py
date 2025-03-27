from typing import Optional, List
from pydantic import BaseModel, validator
from datetime import datetime, date
from enum import Enum

# 猪性别枚举
class PigGender(str, Enum):
    MALE = "male"
    FEMALE = "female"

# 猪健康状态枚举
class PigHealthStatus(str, Enum):
    HEALTHY = "healthy"
    ATTENTION = "attention"
    SICK = "sick"
    TREATMENT = "treatment"
    ISOLATION = "isolation"

# 猪基础模型
class PigBase(BaseModel):
    ear_tag: str
    gender: PigGender
    breed: Optional[str] = None
    birth_date: Optional[date] = None
    entry_date: Optional[date] = None
    entry_weight: Optional[float] = None
    current_weight: Optional[float] = None
    health_status: Optional[PigHealthStatus] = PigHealthStatus.HEALTHY
    pig_house_id: Optional[int] = None
    notes: Optional[str] = None

# 创建猪请求模型
class PigCreate(PigBase):
    pass

# 更新猪请求模型
class PigUpdate(BaseModel):
    gender: Optional[PigGender] = None
    breed: Optional[str] = None
    birth_date: Optional[date] = None
    entry_date: Optional[date] = None
    entry_weight: Optional[float] = None
    current_weight: Optional[float] = None
    health_status: Optional[PigHealthStatus] = None
    pig_house_id: Optional[int] = None
    notes: Optional[str] = None

# 猪响应模型
class Pig(PigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# 体重记录基础模型
class WeightRecordBase(BaseModel):
    pig_id: int
    weight: float
    recorded_by: Optional[int] = None

# 创建体重记录请求模型
class WeightRecordCreate(WeightRecordBase):
    pass

# 体重记录响应模型
class WeightRecord(WeightRecordBase):
    id: int
    recorded_at: datetime
    
    class Config:
        orm_mode = True

# 健康记录基础模型
class HealthRecordBase(BaseModel):
    pig_id: int
    status: PigHealthStatus
    temperature: Optional[float] = None
    symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    recorded_by: Optional[int] = None

# 创建健康记录请求模型
class HealthRecordCreate(HealthRecordBase):
    pass

# 健康记录响应模型
class HealthRecord(HealthRecordBase):
    id: int
    recorded_at: datetime
    
    class Config:
        orm_mode = True

# 饲喂记录基础模型
class FeedingRecordBase(BaseModel):
    pig_house_id: int
    feed_type: str
    amount: float
    recorded_by: Optional[int] = None

# 创建饲喂记录请求模型
class FeedingRecordCreate(FeedingRecordBase):
    pass

# 饲喂记录响应模型
class FeedingRecord(FeedingRecordBase):
    id: int
    feeding_time: datetime
    
    class Config:
        orm_mode = True

# 饲料库存基础模型
class FeedStockBase(BaseModel):
    feed_type: str
    current_amount: float = 0
    capacity: Optional[float] = None
    last_refill_date: Optional[date] = None
    last_refill_amount: Optional[float] = None

# 创建饲料库存请求模型
class FeedStockCreate(FeedStockBase):
    pass

# 更新饲料库存请求模型
class FeedStockUpdate(BaseModel):
    current_amount: Optional[float] = None
    capacity: Optional[float] = None
    last_refill_date: Optional[date] = None
    last_refill_amount: Optional[float] = None

# 饲料库存响应模型
class FeedStock(FeedStockBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True 