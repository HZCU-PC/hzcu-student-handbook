@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist ".venv\Scripts\mkdocs.exe" (
    echo [错误] 还没装好环境，请先依次执行：
    echo     python -m venv .venv
    echo     .venv\Scripts\python.exe -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo 正在启动本地预览...
echo 网址：http://127.0.0.1:8001/hzcu-student-handbook/
echo 关闭本窗口或按 Ctrl+C 即可停止。
echo.

.venv\Scripts\mkdocs.exe serve --dev-addr 127.0.0.1:8001
pause
