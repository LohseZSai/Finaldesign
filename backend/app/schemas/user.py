from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator, Field
from datetime import datetime

# 用户基础模型
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "breeder"
    is_active: bool = True

# 创建用户请求模型
class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度至少为8个字符')
        return v
    
    @validator('role')
    def role_must_be_valid(cls, v):
        valid_roles = ["admin", "technician", "breeder"]
        if v not in valid_roles:
            raise ValueError(f'角色必须是以下之一: {", ".join(valid_roles)}')
        return v

# 更新用户请求模型
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    
    @validator('password')
    def password_min_length(cls, v):
        if v is not None and len(v) < 8:
            raise ValueError('密码长度至少为8个字符')
        return v
    
    @validator('role')
    def role_must_be_valid(cls, v):
        if v is not None:
            valid_roles = ["admin", "technician", "breeder"]
            if v not in valid_roles:
                raise ValueError(f'角色必须是以下之一: {", ".join(valid_roles)}')
        return v

# 用户响应模型
class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# 用户权限模型
class UserPermissions(BaseModel):
    permissions: List[str] 