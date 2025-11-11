@echo off
chcp 65001 >nul

echo ========================================
echo NFC 文件传输站 - mDNS版 启动脚本
echo ========================================
echo.
echo 正在启动Flask和mDNS服务...
echo.
echo --------------------------------------------------
echo ?? 服务已启动！
echo    请将以下地址写入NFC标签:
echo    http://nfc-pc.local:18080
echo --------------------------------------------------
echo.
echo 按任意键停止服务...
echo.

:: 在新窗口中启动Flask (mDNS会在Flask启动时自动注册)
start "Flask & mDNS Server" python app.py

:: 等待用户按键来停止服务
pause >nul

:: --- 清理工作 ---
echo.
echo 正在停止服务...
taskkill /f /im python.exe >nul 2>&1
echo ? 服务已停止。
