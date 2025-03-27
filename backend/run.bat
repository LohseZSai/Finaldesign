@echo off
chcp 65001
echo 启动智能养猪场管理系统后端服务...

REM 检查虚拟环境是否存在
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt

REM 初始化数据库
echo 初始化数据库...
python -m app.db.init_db

REM 生成测试数据
echo 生成测试数据...
python -m app.scripts.generate_test_data

REM 启动服务
echo 启动服务...
python run.py

REM 停用虚拟环境
call venv\Scripts\deactivate 