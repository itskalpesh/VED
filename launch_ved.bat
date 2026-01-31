@echo off
title VED SYSTEM LAUNCHER
cd /d %~dp0

:: 1. Define Python Interpreter Path (prefer venv, fallback to system python)
set PYTHON_EXE=venv\Scripts\python.exe
if not exist "%PYTHON_EXE%" (
    set PYTHON_EXE=python
    echo [INFO] Using system Python. Create a venv for isolation: python -m venv venv
) else (
    "%PYTHON_EXE%" -c "exit 0" 2>nul
    if errorlevel 1 (
        set PYTHON_EXE=python
        echo [INFO] Venv points to missing Python. Using system Python. Delete 'venv' folder to remove this message.
    ) else (
        echo [INFO] Activating venv...
        call venv\Scripts\activate.bat
        set PYTHON_EXE=python
        echo [INFO] Using venv.
    )
)

echo ======================================
echo           VED AI SYSTEM
echo ======================================
echo.
echo [1] CLI (Terminal Mode)
echo [2] GUI (Jarvis UI Mode)
echo.
set /p mode="Select Mode (1/2): "

if "%mode%"=="1" (
    :: Try root file first, then module
    if exist "main.py" (
        "%PYTHON_EXE%" main.py
    ) else (
        echo [INFO] Loading Kernel Module...
        "%PYTHON_EXE%" -m kernel.main
    )
) else (
    :: Try root UI file first
    if exist "jarvis_ui.py" (
        "%PYTHON_EXE%" jarvis_ui.py
    ) else (
        echo [ERROR] jarvis_ui.py not found in root.
        echo Checking for 'ui' module...
        "%PYTHON_EXE%" -m ui.jarvis_ui
    )
)

pause