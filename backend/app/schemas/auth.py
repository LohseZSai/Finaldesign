from typing import Optional
from pydantic import BaseModel, EmailStr

# 令牌模型
class Token(BaseModel):
    access_token: str
    token_type: str

# 令牌数据模型
class TokenData(BaseModel):
    user_id: Optional[int] = None

# 登录请求模型
class Login(BaseModel):
    username: str
    password: str
    remember_me: Optional[bool] = False

# 注册请求模型
class Register(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
