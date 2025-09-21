@echo off
REM SmartFileSort Automation Script for Windows Task Scheduler
REM This script runs the file organizer automatically

SETLOCAL

REM Set paths - Modify these according to your setup
SET SCRIPT_DIR=%~dp0
SET PYTHON_PATH=python
SET SOURCE_DIR=%USERPROFILE%\Downloads
SET TARGET_DIR=%USERPROFILE%\Documents\OrganizedFiles
SET LOG_FILE=%SCRIPT_DIR%..\logs\scheduler_run.log

REM Create log directory if it doesn't exist
if not exist "%SCRIPT_DIR%..\logs" mkdir "%SCRIPT_DIR%..\logs"

REM Log the start time
echo %DATE% %TIME% - Starting SmartFileSort automation >> "%LOG_FILE%"

REM Change to script directory
cd /d "%SCRIPT_DIR%.."

REM Run the Python script
%PYTHON_PATH% src\smartfilesort.py "%SOURCE_DIR%" "%TARGET_DIR%" >> "%LOG_FILE%" 2>&1

REM Log completion
if %ERRORLEVEL% EQU 0 (
    echo %DATE% %TIME% - SmartFileSort completed successfully >> "%LOG_FILE%"
) else (
    echo %DATE% %TIME% - SmartFileSort failed with error code %ERRORLEVEL% >> "%LOG_FILE%"
)

ENDLOCAL