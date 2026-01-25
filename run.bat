@echo off
:: ============== 核心修复：解决编码问题 + 路径/错误处理 ==============
:: 1. 强制CMD使用UTF-8编码（解决中文/特殊字符显示）
chcp 65001 > nul
:: 2. 强制Python输出/输入使用UTF-8（核心解决UnicodeEncodeError）
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=utf-8
:: 3. 切换到脚本所在目录（避免路径错误，关键！）
cd /d "%~dp0"
:: 4. 设置控制台字体（避免UTF-8字符显示成方块）
reg add "HKCU\Console\%~n0" /v "FaceName" /t REG_SZ /d "Consolas" /f > nul 2>&1
reg add "HKCU\Console\%~n0" /v "CodePage" /t REG_DWORD /d 65001 /f > nul 2>&1

:: ============== 原有逻辑：安装依赖 + 启动项目 ==============
echo [INFO] 开始安装/更新项目依赖...
pip install -r requirements.txt
:: 检查pip安装是否失败
if errorlevel 1 (
    echo [ERROR] 依赖安装失败！请检查requirements.txt或网络。
    pause
    exit /b 1
)
echo [INFO] 依赖安装完成，启动项目...
echo.
echo [INFO] ✅ 服务器运行中！局域网下其他设备请访问：http://10.117.28.10:8000
:: 启动Python项目
python backend\server.py

:: ============== 错误处理 + 窗口暂停 ==============
:: 检查项目启动是否失败
if errorlevel 1 (
    echo.
    echo [ERROR] 项目启动失败！错误码：%errorlevel%
    pause
    exit /b 1
)

:: 项目正常退出时暂停（可选，避免窗口闪退）
echo [INFO] 项目已正常退出。
pause