@echo off
REM Quick Start Demo for SmartFileSort
REM This batch file runs a complete demonstration

echo ===============================================
echo SmartFileSort - Quick Start Demo
echo ===============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python is available, starting demo...
echo.

REM Change to the project directory
cd /d "%~dp0.."

REM Run the full demo
echo Running complete demonstration...
echo.
python tests\demo_setup.py --full-demo

echo.
echo ===============================================
echo Demo complete! 
echo.
echo To run the GUI: python gui\gui_app.py
echo To run tests: python tests\test_smartfilesort.py
echo To setup automation: Run scripts\setup_scheduler.ps1 as Administrator
echo ===============================================
pause