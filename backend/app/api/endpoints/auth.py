from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_active_user,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import Token, Login
from app.schemas.user import User as UserSchema, UserPermissions

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 兼容的令牌登录，获取访问令牌
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="用户未激活"
        )
    
    # 设置访问令牌过期时间
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/login/json", response_model=Token)
def login_json(
    login_data: Login, db: Session = Depends(get_db)
) -> Any:
    """
    JSON格式的登录，获取访问令牌
    """
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="用户未激活"
        )
    
    # 设置访问令牌过期时间
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    if login_data.remember_me:
        # 如果选择"记住我"，则延长令牌有效期
        access_token_expires = timedelta(days=30)
    
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserSchema)
def read_users_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取当前用户信息
    """
    return current_user

@router.get("/permissions", response_model=UserPermissions)
def get_user_permissions(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取当前用户权限
    """
    # 根据用户角色分配权限
    permissions = []
    
    # 所有角色都有的基本权限
    base_permissions = [
        "view_dashboard",
        "view_monitoring",
    ]
    permissions.extend(base_permissions)
    
    # 技术员和管理员的权限
    if current_user.role in ["technician", "admin"]:
        tech_permissions = [
            "manage_pigs",
            "manage_feeding",
            "manage_devices",
            "acknowledge_alerts",
        ]
        permissions.extend(tech_permissions)
    
    # 仅管理员的权限
    if current_user.role == "admin":
        admin_permissions = [
            "manage_users",
            "manage_settings",
            "view_reports",
            "export_data",
        ]
        permissions.extend(admin_permissions)
    
    return {"permissions": permissions} 