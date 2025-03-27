from typing import Optional, List, Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime
from enum import Enum

# 猪舍状态枚举
class PigHouseStatus(str, Enum):
    NORMAL = "normal"
    WARNING = "warning"
    ERROR = "error"

# 猪舍基础模型
class PigHouseBase(BaseModel):
    name: str
    description: Optional[str] = None
    capacity: Optional[int] = 0

# 创建猪舍请求模型
class PigHouseCreate(PigHouseBase):
    pass

# 更新猪舍请求模型
class PigHouseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[PigHouseStatus] = None

# 猪舍响应模型
class PigHouse(PigHouseBase):
    id: int
    current_count: int
    status: PigHouseStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# 环境记录基础模型
class EnvironmentRecordBase(BaseModel):
    pig_house_id: int
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    ammonia: Optional[float] = None
    co2: Optional[float] = None
    light: Optional[float] = None
    noise: Optional[float] = None

# 创建环境记录请求模型
class EnvironmentRecordCreate(EnvironmentRecordBase):
    pass

# 环境记录响应模型
class EnvironmentRecord(EnvironmentRecordBase):
    id: int
    recorded_at: datetime
    
    class Config:
        orm_mode = True

# 告警级别枚举
class AlertLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"

# 告警状态枚举
class AlertStatus(str, Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"

# 告警基础模型
class AlertBase(BaseModel):
    pig_house_id: Optional[int] = None
    type: str
    level: AlertLevel
    message: str
    details: Optional[str] = None

# 创建告警请求模型
class AlertCreate(AlertBase):
    pass

# 更新告警请求模型
class AlertUpdate(BaseModel):
    status: Optional[AlertStatus] = None
    details: Optional[str] = None

# 告警响应模型
class Alert(AlertBase):
    id: int
    status: AlertStatus
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    acknowledged_by: Optional[int] = None
    resolved_by: Optional[int] = None
    
    class Config:
        orm_mode = True

# 设备状态枚举
class DeviceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"

# 设备基础模型
class DeviceBase(BaseModel):
    name: str
    device_type: str
    model: Optional[str] = None
    serial_number: Optional[str] = None
    pig_house_id: Optional[int] = None

# 创建设备请求模型
class DeviceCreate(DeviceBase):
    pass

# 更新设备请求模型
class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    device_type: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    pig_house_id: Optional[int] = None
    status: Optional[DeviceStatus] = None

# 设备响应模型
class Device(DeviceBase):
    id: int
    status: DeviceStatus
    last_online: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# 摄像头基础模型
class CameraBase(BaseModel):
    name: str
    url: str
    pig_house_id: Optional[int] = None

# 创建摄像头请求模型
class CameraCreate(CameraBase):
    pass

# 更新摄像头请求模型
class CameraUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    pig_house_id: Optional[int] = None
    status: Optional[str] = None

# 摄像头响应模型
class Camera(CameraBase):
    id: int
    status: str
    last_online: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# 环境数据响应模型
class EnvironmentData(BaseModel):
    temperature: List[Dict[str, Any]]
    humidity: List[Dict[str, Any]]
    ammonia: List[Dict[str, Any]]

# 猪群数据响应模型
class PigData(BaseModel):
    totalCount: int
    weightDistribution: List[Dict[str, Any]]
    healthStatus: Dict[str, int]

# 饲喂数据响应模型
class FeedingData(BaseModel):
    dailyConsumption: List[Dict[str, Any]]
    feedStock: int

# 告警数据响应模型
class AlertsData(BaseModel):
    active: List[Alert]
    history: List[Alert]

# 监控数据响应模型
class MonitoringData(BaseModel):
    environmentData: EnvironmentData
    pigData: PigData
    feedingData: FeedingData
    alertsData: AlertsData
    cameraStreams: List[Camera]
    lastUpdated: datetime 