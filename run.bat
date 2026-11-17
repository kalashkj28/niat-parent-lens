@echo off
set "PYTHONPATH=%~dp0"
echo ==========================================================
echo Starting NIAT Parent Decision Lens (Growth System)...
echo ==========================================================
start http://localhost:8080
"C:\Users\KALASH JAIN\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\python.exe" "%~dp0backend\server.py"
pause
