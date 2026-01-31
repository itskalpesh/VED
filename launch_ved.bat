@echo off
setlocal EnableDelayedExpansion
title VED SYSTEM LAUNCHER

REM ================================
REM        VED AUTO-FIX LAUNCHER
REM ================================

cd /d %~dp0

echo ======================================
echo           VED AI SYSTEM
echo ======================================
echo.

REM -------------------------------------------------
REM STEP 1: Find Python >= 3.12
REM -------------------------------------------------
set SYS_PY=

for %%P in (python py) do (
    %%P -c "import sys; exit(0 if sys.version_info >= (3,12) else 1)" >nul 2>&1
    if !errorlevel! == 0 (
        set SYS_PY=%%P
        goto :python_found
    )
)

:python_found
if "%SYS_PY%"=="" (
    echo [FATAL] Python 3.12 or newer not found.
    pause
    exit /b 1
)

for /f "delims=" %%V in ('%SYS_PY% -c "import sys; print(sys.version.split()[0])"') do (
    set PY_VER=%%V
)

echo [INFO] Using system Python %PY_VER%

REM -------------------------------------------------
REM STEP 2: Ensure virtual environment
REM -------------------------------------------------
set VENV_PY=venv\Scripts\python.exe

if not exist "%VENV_PY%" (
    echo [INFO] Creating virtual environment...
    %SYS_PY% -m venv venv
)

REM -------------------------------------------------
REM STEP 2.1: Ensure pip exists
REM -------------------------------------------------
"%VENV_PY%" -m ensurepip --upgrade >nul 2>&1

REM -------------------------------------------------
REM STEP 2.2: Upgrade pip tools
REM -------------------------------------------------
"%VENV_PY%" -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [FATAL] pip bootstrap failed.
    pause
    exit /b 1
)

REM -------------------------------------------------
REM STEP 2.3: Install dependencies (BLOCKING)
REM -------------------------------------------------
if exist "ved_requirements.txt" (
    echo [INFO] Installing Python dependencies...
    "%VENV_PY%" -m pip install -r ved_requirements.txt
    if errorlevel 1 (
        echo [FATAL] Dependency installation failed.
        pause
        exit /b 1
    )
) else (
    echo [WARN] ved_requirements.txt not found.
)

set PYTHON=%VENV_PY%
echo [INFO] Environment ready.

REM -------------------------------------------------
REM STEP 3: Mode selection
REM -------------------------------------------------
echo.
echo [1] CLI (Terminal Mode)
echo [2] GUI (Jarvis UI Mode)
echo.

set /p MODE=Select Mode (1/2): 

REM -------------------------------------------------
REM STEP 4: CLI Mode
REM -------------------------------------------------
if "%MODE%"=="1" (
    echo [INFO] Starting VED CLI...
    "%PYTHON%" ved_start.py
    goto :eof
)

REM -------------------------------------------------
REM STEP 5: GUI Mode
REM -------------------------------------------------
if "%MODE%"=="2" (
    echo [INFO] Starting VED GUI...

    if exist "gui\jarvis_ui.py" (
        "%PYTHON%" gui\jarvis_ui.py
        goto :eof
    )

    if exist "ui\jarvis_ui.py" (
        "%PYTHON%" ui\jarvis_ui.py
        goto :eof
    )

    echo [ERROR] GUI entry not found.
    pause
    goto :eof
)

echo [ERROR] Invalid option selected.
pause
