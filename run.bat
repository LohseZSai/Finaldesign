@echo off
chcp 65001
echo 启动智能养猪场管理系统...

REM 启动后端服务
echo 启动后端服务...
start cmd /k "cd backend && run.bat"

REM 等待5秒，确保后端服务已启动
timeout /t 5

REM 启动前端服务
echo 启动前端服务...
start cmd /k "cd frontend && run.bat"

echo 服务启动完成！
echo 后端服务地址：http://localhost:8000
echo 前端服务地址：http://localhost:8080
echo 请在浏览器中访问前端服务地址 