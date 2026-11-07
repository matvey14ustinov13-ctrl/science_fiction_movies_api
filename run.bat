@echo off
setlocal
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    where py >nul 2>nul
    if errorlevel 1 (
        python -m venv venv
    ) else (
        py -m venv venv
    )
)

"venv\Scripts\python.exe" -m pip install --quiet --disable-pip-version-check -r requirements.txt || exit /b 1
"venv\Scripts\python.exe" -m compileall -q main.py || exit /b 1
"venv\Scripts\python.exe" -m uvicorn main:app --reload
