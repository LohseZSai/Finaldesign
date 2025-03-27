@echo off
chcp 65001 >nul
echo 启动前端服务...

REM 检查Node.js环境
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Node.js环境，请安装Node.js
    pause
    exit /b 1
)

REM 检查npm
npm --version > nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: npm命令不可用
    pause
    exit /b 1
)

REM 检查端口8080
echo 检查端口8080...
netstat -ano | findstr ":8080" > nul
if %errorlevel% equ 0 (
    echo 警告: 端口8080已被占用，尝试释放端口...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080"') do (
        taskkill /F /PID %%a
    )
    timeout /t 2 /nobreak > nul
)

REM 检查package.json文件
if not exist "package.json" (
    echo 错误: 未找到package.json文件
    pause
    exit /b 1
)

REM 强制安装依赖
echo 正在安装依赖(可能需要几分钟)...
call npm install

REM 确认node_modules存在
if not exist "node_modules" (
    echo 错误: 依赖安装失败，未创建node_modules目录
    pause
    exit /b 1
)

REM 启动服务
echo 正在启动Vue服务...
call npm run serve

if %errorlevel% neq 0 (
    echo 错误: Vue服务启动失败
    pause
    exit /b 1
)
