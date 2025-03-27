from fastapi import APIRouter

from app.api.endpoints import auth, users, monitoring

api_router = APIRouter()

# 添加各个模块的路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["监控系统"]) 