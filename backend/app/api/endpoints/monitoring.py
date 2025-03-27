from typing import Any, List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.core.security import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.models.monitoring import (
    PigHouse, EnvironmentRecord, Alert, AlertStatus, AlertLevel, Device, Camera
)
from app.models.pig import Pig, PigHealthStatus, FeedingRecord, FeedStock
from app.schemas.monitoring import (
    PigHouse as PigHouseSchema,
    PigHouseCreate,
    PigHouseUpdate,
    EnvironmentRecord as EnvironmentRecordSchema,
    EnvironmentRecordCreate,
    Alert as AlertSchema,
    AlertCreate,
    AlertUpdate,
    Device as DeviceSchema,
    DeviceCreate,
    DeviceUpdate,
    Camera as CameraSchema,
    CameraCreate,
    CameraUpdate,
    MonitoringData,
    EnvironmentData,
    PigData,
    FeedingData,
    AlertsData
)

router = APIRouter()

# 猪舍相关接口
@router.get("/pig-houses", response_model=List[PigHouseSchema])
def read_pig_houses(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取所有猪舍列表
    """
    pig_houses = db.query(PigHouse).offset(skip).limit(limit).all()
    return pig_houses

@router.post("/pig-houses", response_model=PigHouseSchema)
def create_pig_house(
    *,
    db: Session = Depends(get_db),
    pig_house_in: PigHouseCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    创建新猪舍
    """
    # 检查是否有权限
    if current_user.role not in ["admin", "technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )
    
    # 创建新猪舍
    pig_house = PigHouse(
        name=pig_house_in.name,
        description=pig_house_in.description,
        capacity=pig_house_in.capacity,
        current_count=0,
        status="normal",
    )
    db.add(pig_house)
    db.commit()
    db.refresh(pig_house)
    return pig_house

@router.get("/pig-houses/{pig_house_id}", response_model=PigHouseSchema)
def read_pig_house(
    *,
    db: Session = Depends(get_db),
    pig_house_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取指定猪舍信息
    """
    pig_house = db.query(PigHouse).filter(PigHouse.id == pig_house_id).first()
    if not pig_house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="猪舍不存在",
        )
    return pig_house

@router.put("/pig-houses/{pig_house_id}", response_model=PigHouseSchema)
def update_pig_house(
    *,
    db: Session = Depends(get_db),
    pig_house_id: int,
    pig_house_in: PigHouseUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    更新猪舍信息
    """
    # 检查是否有权限
    if current_user.role not in ["admin", "technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )
    
    pig_house = db.query(PigHouse).filter(PigHouse.id == pig_house_id).first()
    if not pig_house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="猪舍不存在",
        )
    
    # 更新猪舍信息
    update_data = pig_house_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pig_house, field, value)
    
    db.add(pig_house)
    db.commit()
    db.refresh(pig_house)
    return pig_house

# 环境记录相关接口
@router.post("/environment", response_model=EnvironmentRecordSchema)
def create_environment_record(
    *,
    db: Session = Depends(get_db),
    record_in: EnvironmentRecordCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    创建新环境记录
    """
    # 检查猪舍是否存在
    pig_house = db.query(PigHouse).filter(PigHouse.id == record_in.pig_house_id).first()
    if not pig_house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="猪舍不存在",
        )
    
    # 创建新环境记录
    record = EnvironmentRecord(**record_in.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    
    # 检查是否需要创建告警
    if record.temperature and (record.temperature > 30 or record.temperature < 15):
        level = AlertLevel.WARNING if (record.temperature > 28 or record.temperature < 18) else AlertLevel.DANGER
        alert = Alert(
            pig_house_id=record.pig_house_id,
            type="温度异常",
            level=level,
            message=f"温度{'过高' if record.temperature > 30 else '过低'} ({record.temperature}°C)",
            details=f"猪舍 {pig_house.name} 温度{'超过30°C' if record.temperature > 30 else '低于15°C'}，可能影响猪群健康。",
            status=AlertStatus.ACTIVE,
        )
        db.add(alert)
    
    if record.humidity and (record.humidity > 80 or record.humidity < 40):
        level = AlertLevel.WARNING if (record.humidity > 75 or record.humidity < 45) else AlertLevel.DANGER
        alert = Alert(
            pig_house_id=record.pig_house_id,
            type="湿度异常",
            level=level,
            message=f"湿度{'过高' if record.humidity > 80 else '过低'} ({record.humidity}%)",
            details=f"猪舍 {pig_house.name} 湿度{'超过80%' if record.humidity > 80 else '低于40%'}，可能影响猪群健康。",
            status=AlertStatus.ACTIVE,
        )
        db.add(alert)
    
    if record.ammonia and record.ammonia > 10:
        level = AlertLevel.WARNING if record.ammonia < 15 else AlertLevel.DANGER
        alert = Alert(
            pig_house_id=record.pig_house_id,
            type="氨气异常",
            level=level,
            message=f"氨气浓度过高 ({record.ammonia} ppm)",
            details=f"猪舍 {pig_house.name} 氨气浓度超过10ppm，可能影响猪群健康，建议增强通风。",
            status=AlertStatus.ACTIVE,
        )
        db.add(alert)
    
    db.commit()
    return record

@router.get("/environment", response_model=List[EnvironmentRecordSchema])
def read_environment_records(
    db: Session = Depends(get_db),
    pig_house_id: Optional[int] = None,
    time_range: str = "24h",
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取环境记录列表
    """
    # 根据时间范围计算起始时间
    now = datetime.now()
    if time_range == "24h":
        start_time = now - timedelta(hours=24)
    elif time_range == "7d":
        start_time = now - timedelta(days=7)
    elif time_range == "30d":
        start_time = now - timedelta(days=30)
    else:
        start_time = now - timedelta(hours=24)
    
    # 构建查询
    query = db.query(EnvironmentRecord).filter(EnvironmentRecord.recorded_at >= start_time)
    
    # 如果指定了猪舍ID，则只查询该猪舍的记录
    if pig_house_id:
        query = query.filter(EnvironmentRecord.pig_house_id == pig_house_id)
    
    # 按时间降序排序，并分页
    records = query.order_by(desc(EnvironmentRecord.recorded_at)).offset(skip).limit(limit).all()
    return records

# 告警相关接口
@router.get("/alerts", response_model=List[AlertSchema])
def read_alerts(
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    pig_house_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取告警列表
    """
    # 构建查询
    query = db.query(Alert)
    
    # 如果指定了状态，则只查询该状态的告警
    if status:
        query = query.filter(Alert.status == status)
    
    # 如果指定了猪舍ID，则只查询该猪舍的告警
    if pig_house_id:
        query = query.filter(Alert.pig_house_id == pig_house_id)
    
    # 按时间降序排序，并分页
    alerts = query.order_by(desc(Alert.created_at)).offset(skip).limit(limit).all()
    return alerts

@router.post("/alerts", response_model=AlertSchema)
def create_alert(
    *,
    db: Session = Depends(get_db),
    alert_in: AlertCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    创建新告警
    """
    # 如果指定了猪舍ID，检查猪舍是否存在
    if alert_in.pig_house_id:
        pig_house = db.query(PigHouse).filter(PigHouse.id == alert_in.pig_house_id).first()
        if not pig_house:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="猪舍不存在",
            )
    
    # 创建新告警
    alert = Alert(
        pig_house_id=alert_in.pig_house_id,
        type=alert_in.type,
        level=alert_in.level,
        message=alert_in.message,
        details=alert_in.details,
        status=AlertStatus.ACTIVE,
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

@router.post("/alerts/{alert_id}/acknowledge", response_model=AlertSchema)
def acknowledge_alert(
    *,
    db: Session = Depends(get_db),
    alert_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    确认告警
    """
    # 检查是否有权限
    if current_user.role not in ["admin", "technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )
    
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="告警不存在",
        )
    
    # 更新告警状态
    alert.status = AlertStatus.ACKNOWLEDGED
    alert.acknowledged_at = datetime.now()
    alert.acknowledged_by = current_user.id
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

@router.post("/alerts/{alert_id}/resolve", response_model=AlertSchema)
def resolve_alert(
    *,
    db: Session = Depends(get_db),
    alert_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    解决告警
    """
    # 检查是否有权限
    if current_user.role not in ["admin", "technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )
    
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="告警不存在",
        )
    
    # 更新告警状态
    alert.status = AlertStatus.RESOLVED
    alert.resolved_at = datetime.now()
    alert.resolved_by = current_user.id
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

# 设备相关接口
@router.get("/devices", response_model=List[DeviceSchema])
def read_devices(
    db: Session = Depends(get_db),
    pig_house_id: Optional[int] = None,
    device_type: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取设备列表
    """
    # 构建查询
    query = db.query(Device)
    
    # 如果指定了猪舍ID，则只查询该猪舍的设备
    if pig_house_id:
        query = query.filter(Device.pig_house_id == pig_house_id)
    
    # 如果指定了设备类型，则只查询该类型的设备
    if device_type:
        query = query.filter(Device.device_type == device_type)
    
    # 如果指定了状态，则只查询该状态的设备
    if status:
        query = query.filter(Device.status == status)
    
    # 分页
    devices = query.offset(skip).limit(limit).all()
    return devices

@router.post("/devices", response_model=DeviceSchema)
def create_device(
    *,
    db: Session = Depends(get_db),
    device_in: DeviceCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    创建新设备
    """
    # 检查是否有权限
    if current_user.role not in ["admin", "technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )
    
    # 如果指定了猪舍ID，检查猪舍是否存在
    if device_in.pig_house_id:
        pig_house = db.query(PigHouse).filter(PigHouse.id == device_in.pig_house_id).first()
        if not pig_house:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="猪舍不存在",
            )
    
    # 如果指定了序列号，检查序列号是否已存在
    if device_in.serial_number:
        device = db.query(Device).filter(Device.serial_number == device_in.serial_number).first()
        if device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="设备序列号已存在",
            )
    
    # 创建新设备
    device = Device(
        name=device_in.name,
        device_type=device_in.device_type,
        model=device_in.model,
        serial_number=device_in.serial_number,
        pig_house_id=device_in.pig_house_id,
        status="online",
        last_online=datetime.now(),
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return device

@router.put("/devices/{device_id}", response_model=DeviceSchema)
def update_device(
    *,
    db: Session = Depends(get_db),
    device_id: int,
    device_in: DeviceUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    更新设备信息
    """
    # 检查是否有权限
    if current_user.role not in ["admin", "technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )
    
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="设备不存在",
        )
    
    # 如果更新猪舍ID，检查猪舍是否存在
    if device_in.pig_house_id is not None:
        pig_house = db.query(PigHouse).filter(PigHouse.id == device_in.pig_house_id).first()
        if not pig_house:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="猪舍不存在",
            )
    
    # 如果更新序列号，检查序列号是否已存在
    if device_in.serial_number is not None and device_in.serial_number != device.serial_number:
        existing_device = db.query(Device).filter(Device.serial_number == device_in.serial_number).first()
        if existing_device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="设备序列号已存在",
            )
    
    # 更新设备信息
    update_data = device_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(device, field, value)
    
    # 如果更新状态为online，更新最后在线时间
    if device_in.status == "online":
        device.last_online = datetime.now()
    
    db.add(device)
    db.commit()
    db.refresh(device)
    return device

# 摄像头相关接口
@router.get("/cameras", response_model=List[CameraSchema])
def read_cameras(
    db: Session = Depends(get_db),
    pig_house_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取摄像头列表
    """
    # 构建查询
    query = db.query(Camera)
    
    # 如果指定了猪舍ID，则只查询该猪舍的摄像头
    if pig_house_id:
        query = query.filter(Camera.pig_house_id == pig_house_id)
    
    # 如果指定了状态，则只查询该状态的摄像头
    if status:
        query = query.filter(Camera.status == status)
    
    # 分页
    cameras = query.offset(skip).limit(limit).all()
    return cameras

@router.post("/cameras", response_model=CameraSchema)
def create_camera(
    *,
    db: Session = Depends(get_db),
    camera_in: CameraCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    创建新摄像头
    """
    # 检查是否有权限
    if current_user.role not in ["admin", "technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )
    
    # 如果指定了猪舍ID，检查猪舍是否存在
    if camera_in.pig_house_id:
        pig_house = db.query(PigHouse).filter(PigHouse.id == camera_in.pig_house_id).first()
        if not pig_house:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="猪舍不存在",
            )
    
    # 创建新摄像头
    camera = Camera(
        name=camera_in.name,
        url=camera_in.url,
        pig_house_id=camera_in.pig_house_id,
        status="online",
        last_online=datetime.now(),
    )
    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera

@router.put("/cameras/{camera_id}", response_model=CameraSchema)
def update_camera(
    *,
    db: Session = Depends(get_db),
    camera_id: int,
    camera_in: CameraUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    更新摄像头信息
    """
    # 检查是否有权限
    if current_user.role not in ["admin", "technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )
    
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="摄像头不存在",
        )
    
    # 如果更新猪舍ID，检查猪舍是否存在
    if camera_in.pig_house_id is not None:
        pig_house = db.query(PigHouse).filter(PigHouse.id == camera_in.pig_house_id).first()
        if not pig_house:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="猪舍不存在",
            )
    
    # 更新摄像头信息
    update_data = camera_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(camera, field, value)
    
    # 如果更新状态为online，更新最后在线时间
    if camera_in.status == "online":
        camera.last_online = datetime.now()
    
    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera

# 综合监控数据接口
@router.get("/dashboard", response_model=MonitoringData)
def get_monitoring_data(
    db: Session = Depends(get_db),
    time_range: str = "24h",
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取综合监控数据
    """
    # 根据时间范围计算起始时间
    now = datetime.now()
    if time_range == "24h":
        start_time = now - timedelta(hours=24)
    elif time_range == "7d":
        start_time = now - timedelta(days=7)
    elif time_range == "30d":
        start_time = now - timedelta(days=30)
    else:
        start_time = now - timedelta(hours=24)
    
    # 获取环境数据
    env_records = db.query(EnvironmentRecord).filter(
        EnvironmentRecord.recorded_at >= start_time
    ).order_by(EnvironmentRecord.recorded_at).all()
    
    temperature_data = []
    humidity_data = []
    ammonia_data = []
    
    for record in env_records:
        timestamp = record.recorded_at.isoformat()
        if record.temperature is not None:
            temperature_data.append({"time": timestamp, "value": record.temperature})
        if record.humidity is not None:
            humidity_data.append({"time": timestamp, "value": record.humidity})
        if record.ammonia is not None:
            ammonia_data.append({"time": timestamp, "value": record.ammonia})
    
    # 获取猪群数据
    total_count = db.query(func.count(Pig.id)).scalar() or 0
    
    # 获取体重分布
    weight_distribution = []
    weight_ranges = [
        {"min": 0, "max": 50, "label": "<50kg"},
        {"min": 50, "max": 80, "label": "50-80kg"},
        {"min": 80, "max": 100, "label": "80-100kg"},
        {"min": 100, "max": 120, "label": "100-120kg"},
        {"min": 120, "max": 1000, "label": ">120kg"},
    ]
    
    for weight_range in weight_ranges:
        count = db.query(func.count(Pig.id)).filter(
            Pig.current_weight >= weight_range["min"],
            Pig.current_weight < weight_range["max"]
        ).scalar() or 0
        
        weight_distribution.append({
            "name": weight_range["label"],
            "value": count
        })
    
    # 获取健康状态分布
    health_status = {
        "healthy": db.query(func.count(Pig.id)).filter(Pig.health_status == PigHealthStatus.HEALTHY).scalar() or 0,
        "attention": db.query(func.count(Pig.id)).filter(Pig.health_status == PigHealthStatus.ATTENTION).scalar() or 0,
        "sick": db.query(func.count(Pig.id)).filter(Pig.health_status == PigHealthStatus.SICK).scalar() or 0,
        "treatment": db.query(func.count(Pig.id)).filter(Pig.health_status == PigHealthStatus.TREATMENT).scalar() or 0,
        "isolation": db.query(func.count(Pig.id)).filter(Pig.health_status == PigHealthStatus.ISOLATION).scalar() or 0,
    }
    
    # 获取饲喂数据
    feeding_records = db.query(FeedingRecord).filter(
        FeedingRecord.feeding_time >= start_time
    ).order_by(FeedingRecord.feeding_time).all()
    
    daily_consumption = []
    for record in feeding_records:
        daily_consumption.append({
            "time": record.feeding_time.isoformat(),
            "value": record.amount
        })
    
    # 获取饲料库存
    feed_stock = db.query(func.sum(FeedStock.current_amount)).scalar() or 0
    
    # 获取告警数据
    active_alerts = db.query(Alert).filter(Alert.status == AlertStatus.ACTIVE).order_by(desc(Alert.created_at)).all()
    history_alerts = db.query(Alert).filter(
        Alert.status != AlertStatus.ACTIVE,
        Alert.created_at >= start_time
    ).order_by(desc(Alert.created_at)).all()
    
    # 获取摄像头数据
    cameras = db.query(Camera).all()
    
    # 构建返回数据
    return {
        "environmentData": {
            "temperature": temperature_data,
            "humidity": humidity_data,
            "ammonia": ammonia_data
        },
        "pigData": {
            "totalCount": total_count,
            "weightDistribution": weight_distribution,
            "healthStatus": health_status
        },
        "feedingData": {
            "dailyConsumption": daily_consumption,
            "feedStock": feed_stock
        },
        "alertsData": {
            "active": active_alerts,
            "history": history_alerts
        },
        "cameraStreams": cameras,
        "lastUpdated": now
    } 