@echo off
REM Quick-start batch file for Whisper on AMD Windows
REM Usage: run.bat [command] [args]
REM   run.bat transcribe audio.mp3
REM   run.bat benchmark
REM   run.bat verify
REM   run.bat install

setlocal enabledelayedexpansion

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Could not create virtual environment
        echo Ensure Python 3.10+ is installed and in PATH
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Could not activate virtual environment
    exit /b 1
)

REM Parse command
set "COMMAND=%1"
if "%COMMAND%"=="" (
    echo Whisper AMD Windows — Quick Start
    echo.
    echo Usage:
    echo   run.bat install          - Install dependencies
    echo   run.bat verify           - Verify GPU setup
    echo   run.bat transcribe FILE  - Transcribe audio file
    echo   run.bat benchmark        - Benchmark GPU performance
    echo.
    echo Examples:
    echo   run.bat transcribe podcast.mp3
    echo   run.bat transcribe meeting.wav --model medium
    echo   run.bat benchmark --duration 120
    exit /b 0
)

if /i "%COMMAND%"=="install" (
    echo Installing dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
    exit /b %errorlevel%
)

if /i "%COMMAND%"=="verify" (
    python scripts/verify_gpu.py
    exit /b %errorlevel%
)

if /i "%COMMAND%"=="transcribe" (
    python scripts/transcribe.py %2 %3 %4 %5 %6 %7 %8 %9
    exit /b %errorlevel%
)

if /i "%COMMAND%"=="benchmark" (
    python scripts/benchmark.py %2 %3 %4 %5
    exit /b %errorlevel%
)

echo Unknown command: %COMMAND%
echo Run "run.bat" for help
exit /b 1
