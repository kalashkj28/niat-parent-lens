@echo off
set "PYTHONPATH=%~dp0"
echo Resetting NIAT Parent Lens database to clean 14/11/6 baseline...
"C:\Users\KALASH JAIN\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\python.exe" "%~dp0backend\reset_and_seed_clean_db.py"
echo Done! Refresh your browser (Ctrl + F5).
timeout /t 3
