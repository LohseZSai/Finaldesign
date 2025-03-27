import logging
import os
import sys
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_issues():
    """修复系统问题"""
    logger.info("开始修复系统问题...")
    
    # 1. 安装缺少的依赖
    logger.info("安装缺少的依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "email-validator"])
    subprocess.run([sys.executable, "-m", "pip", "install", "pydantic[email]"])
    
    # 2. 重新初始化数据库
    logger.info("重新初始化数据库...")
    # 删除旧的数据库文件
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "hongtai_farm.db")
    if os.path.exists(db_path):
        os.remove(db_path)
        logger.info(f"已删除旧数据库文件: {db_path}")
    
    # 重新初始化数据库
    from app.db.init_db import init_db, create_initial_data
    from app.db.database import SessionLocal
    
    init_db()
    db = SessionLocal()
    try:
        create_initial_data(db)
    finally:
        db.close()
    
    # 3. 重新生成测试数据
    logger.info("重新生成测试数据...")
    from app.scripts.generate_test_data import generate_test_data
    
    db = SessionLocal()
    try:
        generate_test_data(db)
    finally:
        db.close()
    
    logger.info("系统问题修复完成！")

if __name__ == "__main__":
    fix_issues() 
import logging
import os
import sys
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_issues():
    """修复系统问题"""
    logger.info("开始修复系统问题...")
    
    # 1. 安装缺少的依赖
    logger.info("安装缺少的依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "email-validator"])
    subprocess.run([sys.executable, "-m", "pip", "install", "pydantic[email]"])
    
    # 2. 重新初始化数据库
    logger.info("重新初始化数据库...")
    # 删除旧的数据库文件
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "hongtai_farm.db")
    if os.path.exists(db_path):
        os.remove(db_path)
        logger.info(f"已删除旧数据库文件: {db_path}")
    
    # 重新初始化数据库
    from app.db.init_db import init_db, create_initial_data
    from app.db.database import SessionLocal
    
    init_db()
    db = SessionLocal()
    try:
        create_initial_data(db)
    finally:
        db.close()
    
    # 3. 重新生成测试数据
    logger.info("重新生成测试数据...")
    from app.scripts.generate_test_data import generate_test_data
    
    db = SessionLocal()
    try:
        generate_test_data(db)
    finally:
        db.close()
    
    logger.info("系统问题修复完成！")

if __name__ == "__main__":
    fix_issues() 