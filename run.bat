@echo off
chcp 65001 >nul
echo 正在启动泓泰生物科技智能养殖管理系统...
echo.

REM 检查端口8000
echo 检查后端端口(8000)...
netstat -ano | findstr ":8000" > nul
if %errorlevel% equ 0 (
    echo 停止占用8000端口的进程...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
        taskkill /F /PID %%a
    )
    timeout /t 2 /nobreak > nul
)

REM 检查端口8080
echo 检查前端端口(8080)...
netstat -ano | findstr ":8080" > nul
if %errorlevel% equ 0 (
    echo 停止占用8080端口的进程...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080"') do (
        taskkill /F /PID %%a
    )
    timeout /t 2 /nobreak > nul
)

echo.
echo 启动后端服务...
cd backend
start cmd /k "chcp 65001 > nul && call run.bat"

echo 等待后端服务启动...
timeout /t 10 /nobreak > nul

echo 启动前端服务...
cd ../frontend

REM 方法1：直接在当前窗口启动前端服务
echo.
echo 您也可以选择手动启动前端服务：
echo 1. 打开新的命令行窗口
echo 2. 执行: cd %CD%
echo 3. 执行: npm run serve
echo.

REM 方法2：在新窗口启动前端服务
start cmd /k "chcp 65001 > nul && cd %CD% && call npm run serve"

echo.
echo 系统正在启动，请稍候...
echo 前端地址: http://localhost:8080
echo 后端地址: http://localhost:8000
echo.
echo 前端服务可能需要几分钟才能完全启动
echo 如果浏览器无法立即访问，请稍等片刻后再试
echo.
echo 按任意键退出此窗口(不会关闭已启动的服务)...
pause > nul







