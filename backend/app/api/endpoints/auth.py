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
from app.schemas.auth import Token, Login, Register
from app.schemas.user import User as UserSchema, UserPermissions

router = APIRouter()

@router.post("/register", response_model=UserSchema)
def register_user(
    user_in: Register,
    db: Session = Depends(get_db)
) -> Any:
    """
    用户注册
    """
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 创建新用户
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name if user_in.full_name else user_in.username,
        role="breeder",  # 默认注册为饲养员角色
        is_active=True
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

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
