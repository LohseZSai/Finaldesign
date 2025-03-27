import os
import json
from pydantic import BaseSettings
from typing import List, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Settings(BaseSettings):
    """应用程序设置"""
    
    # 应用信息
    APP_NAME: str = "泓泰生物科技智能养殖管理系统"
    API_V1_STR: str = "/api"
    
    # 安全配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hongtai_farm.db")
    
    # CORS配置
    CORS_ORIGINS: List[str] = json.loads(os.getenv("CORS_ORIGINS", '["http://localhost:8080"]'))
    
    # 调试模式
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    class Config:
        case_sensitive = True

# 创建设置实例
settings = Settings() 