@echo off
chcp 65001 >nul
echo 启动后端服务...

REM 检查Python环境
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境，请安装Python
    pause
    exit /b 1
)

REM 检查并安装依赖
echo 检查并安装依赖...
pip install -r requirements.txt

REM 检查端口8000
echo 检查端口8000...
netstat -ano | findstr ":8000" > nul
if %errorlevel% equ 0 (
    echo 警告: 端口8000已被占用，尝试释放端口...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
        taskkill /F /PID %%a
    )
)

REM 启动服务
echo 正在启动FastAPI服务...
python run.py
