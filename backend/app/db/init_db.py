import logging
from sqlalchemy.orm import Session

from app.db.database import engine, Base
from app.core.security import get_password_hash
from app.models.user import User
from app.models.monitoring import PigHouse, AlertLevel, AlertStatus
from app.models.pig import PigGender, PigHealthStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    """初始化数据库"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建完成")

def create_initial_data(db: Session) -> None:
    """创建初始数据"""
    # 创建管理员用户
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="系统管理员",
            role="admin",
            is_active=True,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        logger.info("管理员用户创建成功")
    else:
        logger.info("管理员用户已存在")
    
    # 创建技术员用户
    tech_user = db.query(User).filter(User.username == "technician").first()
    if not tech_user:
        tech_user = User(
            username="technician",
            email="tech@example.com",
            hashed_password=get_password_hash("tech123"),
            full_name="技术员",
            role="technician",
            is_active=True,
        )
        db.add(tech_user)
        db.commit()
        db.refresh(tech_user)
        logger.info("技术员用户创建成功")
    else:
        logger.info("技术员用户已存在")
    
    # 创建饲养员用户
    breeder_user = db.query(User).filter(User.username == "breeder").first()
    if not breeder_user:
        breeder_user = User(
            username="breeder",
            email="breeder@example.com",
            hashed_password=get_password_hash("breeder123"),
            full_name="饲养员",
            role="breeder",
            is_active=True,
        )
        db.add(breeder_user)
        db.commit()
        db.refresh(breeder_user)
        logger.info("饲养员用户创建成功")
    else:
        logger.info("饲养员用户已存在")
    
    # 创建示例猪舍
    pig_house = db.query(PigHouse).filter(PigHouse.name == "示例猪舍").first()
    if not pig_house:
        pig_house = PigHouse(
            name="示例猪舍",
            description="用于演示的猪舍",
            capacity=100,
            current_count=0,
            status="normal",
        )
        db.add(pig_house)
        db.commit()
        db.refresh(pig_house)
        logger.info("示例猪舍创建成功")
    else:
        logger.info("示例猪舍已存在")

if __name__ == "__main__":
    logger.info("初始化数据库...")
    init_db()
    
    # 创建数据库会话
    from app.db.database import SessionLocal
    db = SessionLocal()
    try:
        logger.info("创建初始数据...")
        create_initial_data(db)
        logger.info("初始数据创建完成")
    finally:
        db.close() 