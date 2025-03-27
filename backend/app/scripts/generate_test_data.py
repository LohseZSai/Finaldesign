import logging
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import User
from app.models.monitoring import (
    PigHouse, EnvironmentRecord, Alert, AlertStatus, AlertLevel, Device, Camera
)
from app.models.pig import (
    Pig, PigGender, PigHealthStatus, WeightRecord, HealthRecord, FeedingRecord, FeedStock
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_test_data(db: Session) -> None:
    """生成测试数据"""
    
    # 创建猪舍
    pig_houses = []
    for i in range(1, 4):
        pig_house = db.query(PigHouse).filter(PigHouse.name == f"猪舍{i}").first()
        if not pig_house:
            pig_house = PigHouse(
                name=f"猪舍{i}",
                description=f"用于测试的猪舍{i}",
                capacity=100,
                current_count=0,
                status="normal",
            )
            db.add(pig_house)
            db.commit()
            db.refresh(pig_house)
            logger.info(f"猪舍{i}创建成功")
        pig_houses.append(pig_house)
    
    # 创建设备
    device_types = ["温度传感器", "湿度传感器", "氨气传感器", "喂食器", "饮水器", "通风设备"]
    for pig_house in pig_houses:
        for device_type in device_types:
            device = db.query(Device).filter(
                Device.pig_house_id == pig_house.id,
                Device.device_type == device_type
            ).first()
            if not device:
                device = Device(
                    name=f"{pig_house.name}-{device_type}",
                    device_type=device_type,
                    model=f"Model-{random.randint(100, 999)}",
                    serial_number=f"SN-{random.randint(10000, 99999)}",
                    pig_house_id=pig_house.id,
                    status="online",
                    last_online=datetime.now(),
                )
                db.add(device)
        db.commit()
        logger.info(f"{pig_house.name}的设备创建成功")
    
    # 创建摄像头
    for pig_house in pig_houses:
        for i in range(1, 3):
            camera = db.query(Camera).filter(
                Camera.pig_house_id == pig_house.id,
                Camera.name == f"{pig_house.name}-摄像头{i}"
            ).first()
            if not camera:
                camera = Camera(
                    name=f"{pig_house.name}-摄像头{i}",
                    url=f"rtsp://example.com/camera/{pig_house.id}/{i}",
                    pig_house_id=pig_house.id,
                    status="online",
                    last_online=datetime.now(),
                )
                db.add(camera)
        db.commit()
        logger.info(f"{pig_house.name}的摄像头创建成功")
    
    # 创建猪只
    for pig_house in pig_houses:
        for i in range(1, 21):
            ear_tag = f"PIG-{pig_house.id}-{i:03d}"
            pig = db.query(Pig).filter(Pig.ear_tag == ear_tag).first()
            if not pig:
                gender = random.choice([PigGender.MALE, PigGender.FEMALE])
                birth_date = datetime.now() - timedelta(days=random.randint(30, 180))
                entry_date = birth_date + timedelta(days=random.randint(7, 30))
                entry_weight = random.uniform(5.0, 15.0)
                current_weight = entry_weight + random.uniform(10.0, 50.0)
                health_status = random.choices(
                    [PigHealthStatus.HEALTHY, PigHealthStatus.ATTENTION, PigHealthStatus.SICK],
                    weights=[0.8, 0.15, 0.05]
                )[0]
                
                pig = Pig(
                    ear_tag=ear_tag,
                    gender=gender,
                    breed="大白猪",
                    birth_date=birth_date,
                    entry_date=entry_date,
                    entry_weight=entry_weight,
                    current_weight=current_weight,
                    health_status=health_status,
                    pig_house_id=pig_house.id,
                    notes="测试数据",
                )
                db.add(pig)
                
                # 更新猪舍当前数量
                pig_house.current_count += 1
                db.add(pig_house)
        
        db.commit()
        logger.info(f"{pig_house.name}的猪只创建成功")
    
    # 创建环境记录
    now = datetime.now()
    for pig_house in pig_houses:
        for i in range(24):  # 24小时的数据
            time_point = now - timedelta(hours=i)
            
            # 随机生成环境参数，但保持一定的连续性
            base_temp = random.uniform(20.0, 25.0)
            base_humidity = random.uniform(60.0, 70.0)
            base_ammonia = random.uniform(5.0, 8.0)
            
            # 添加一些随机波动
            temp_variation = random.uniform(-2.0, 2.0)
            humidity_variation = random.uniform(-5.0, 5.0)
            ammonia_variation = random.uniform(-1.0, 1.0)
            
            # 创建环境记录
            record = EnvironmentRecord(
                pig_house_id=pig_house.id,
                temperature=base_temp + temp_variation,
                humidity=base_humidity + humidity_variation,
                ammonia=base_ammonia + ammonia_variation,
                recorded_at=time_point,
            )
            db.add(record)
        
        db.commit()
        logger.info(f"{pig_house.name}的环境记录创建成功")
    
    # 创建告警
    alert_types = ["温度异常", "湿度异常", "氨气异常", "设备离线", "猪只健康异常"]
    alert_levels = [AlertLevel.INFO, AlertLevel.WARNING, AlertLevel.DANGER]
    alert_statuses = [AlertStatus.ACTIVE, AlertStatus.ACKNOWLEDGED, AlertStatus.RESOLVED]
    
    for pig_house in pig_houses:
        for i in range(5):  # 每个猪舍5个告警
            alert_type = random.choice(alert_types)
            alert_level = random.choice(alert_levels)
            alert_status = random.choice(alert_statuses)
            created_at = now - timedelta(hours=random.randint(1, 48))
            
            alert = Alert(
                pig_house_id=pig_house.id,
                type=alert_type,
                level=alert_level,
                message=f"{alert_type}告警",
                details=f"{pig_house.name}的{alert_type}告警，请及时处理。",
                status=alert_status,
                created_at=created_at,
            )
            
            if alert_status == AlertStatus.ACKNOWLEDGED:
                alert.acknowledged_at = created_at + timedelta(minutes=random.randint(5, 30))
                alert.acknowledged_by = 1  # 管理员ID
            
            if alert_status == AlertStatus.RESOLVED:
                alert.acknowledged_at = created_at + timedelta(minutes=random.randint(5, 30))
                alert.acknowledged_by = 1  # 管理员ID
                alert.resolved_at = alert.acknowledged_at + timedelta(minutes=random.randint(10, 60))
                alert.resolved_by = 1  # 管理员ID
            
            db.add(alert)
        
        db.commit()
        logger.info(f"{pig_house.name}的告警创建成功")
    
    # 创建饲料库存
    feed_types = ["标准饲料", "生长饲料", "育肥饲料"]
    for feed_type in feed_types:
        feed_stock = db.query(FeedStock).filter(FeedStock.feed_type == feed_type).first()
        if not feed_stock:
            feed_stock = FeedStock(
                feed_type=feed_type,
                current_amount=random.uniform(500.0, 2000.0),
                capacity=2000.0,
                last_refill_date=now - timedelta(days=random.randint(1, 10)),
            )
            db.add(feed_stock)
    
    db.commit()
    logger.info("饲料库存创建成功")
    
    # 创建饲喂记录
    for pig_house in pig_houses:
        for i in range(7):  # 7天的饲喂记录
            feeding_time = now - timedelta(days=i)
            feed_type = random.choice(feed_types)
            amount = random.uniform(50.0, 100.0)
            
            feeding_record = FeedingRecord(
                pig_house_id=pig_house.id,
                feed_type=feed_type,
                amount=amount,
                feeding_time=feeding_time,
            )
            db.add(feeding_record)
        
        db.commit()
        logger.info(f"{pig_house.name}的饲喂记录创建成功")
    
    logger.info("测试数据生成完成")

if __name__ == "__main__":
    logger.info("开始生成测试数据...")
    db = SessionLocal()
    try:
        generate_test_data(db)
    finally:
        db.close()
    logger.info("测试数据生成完成") 