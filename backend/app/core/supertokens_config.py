import os
from typing import Dict, Any

import supertokens_python as stk
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe import emailpassword, session, thirdparty
from supertokens_python.recipe.thirdparty.provider import Github, Google
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from starlette.middleware.cors import CORSMiddleware

# SuperTokens核心配置
stk.init(
    app_info=stk.InputAppInfo(
        app_name="泓泰生物科技",
        api_domain="http://localhost:8000",
        website_domain="http://localhost:8080",
        api_base_path="/auth",
        website_base_path="/auth"
    ),
    framework='fastapi',
    supertokens_config=stk.ConnectionConfig(
        connection_uri="http://localhost:3567",
    ),
    recipe_list=[
        session.init(),
        emailpassword.init(
            sign_up_feature=emailpassword.InputSignUpFeature(
                form_fields=[
                    emailpassword.InputFormField(id="username"),
                    emailpassword.InputFormField(id="email", optional=True),
                ]
            )
        ),
        thirdparty.init(
            sign_in_up_feature=thirdparty.SignInUpFeature(
                providers=[
                    # Github登录配置
                    Github(
                        client_id=os.getenv("GITHUB_CLIENT_ID", "your_github_client_id"),
                        client_secret=os.getenv("GITHUB_CLIENT_SECRET", "your_github_client_secret")
                    ),
                    # Google登录配置
                    Google(
                        client_id=os.getenv("GOOGLE_CLIENT_ID", "your_google_client_id"),
                        client_secret=os.getenv("GOOGLE_CLIENT_SECRET", "your_google_client_secret")
                    )
                ]
            )
        )
    ]
)

# FastAPI中间件配置
middleware = [
    get_middleware(),
    CORSMiddleware(
        allow_origins=["http://localhost:8080"],
        allow_credentials=True,
        allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Content-Type"] + stk.get_required_headers()
    )
]

# 用户角色管理
async def get_user_roles(user_id: str) -> list:
    """获取用户角色"""
    # TODO: 从数据库获取用户角色
    return ["user"]

async def assign_role_on_signup(user_id: str, user_info: Dict[str, Any]) -> None:
    """注册时分配用户角色"""
    # TODO: 在用户注册时分配适当的角色
    pass

# Session验证装饰器
verify_session_optional = verify_session(session_required=False)
verify_session_required = verify_session(session_required=True)
