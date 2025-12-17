@echo off
title AGENT 50 - Launcher
echo =====================================
echo      AGENT 50 - AUTO LAUNCHER
echo =====================================
echo.

REM Move to Agent 50 folder
cd /d "C:\Users\ADMIN\Desktop\agent 50"

REM Activate virtual environment
echo Activating virtual environment...
call .\.venv\Scripts\activate

echo.
echo Virtual environment activated.
echo.

echo =====================================
echo Choose what you want to run:
echo =====================================
echo 1 - Run auto_save_system.py
echo 2 - Run demo_file_creator.py
echo 3 - Run app.py (your main agent UI)
echo 4 - Run multi_file_agent.py
echo 5 - Open Python Shell inside Agent50
echo 6 - Exit
echo =====================================

set /p choice="Enter option number: "

if "%choice%"=="1" (
    echo Running auto_save_system.py ...
    python auto_save_system.py
    goto end
)

if "%choice%"=="2" (
    echo Running demo_file_creator.py ...
    python demo_file_creator.py
    goto end
)

if "%choice%"=="3" (
    echo Running app.py ...
    python app.py
    goto end
)

if "%choice%"=="4" (
    echo Running multi_file_agent.py ...
    python multi_file_agent.py
    goto end
)

if "%choice%"=="5" (
    echo Starting Python Shell in Agent50 venv...
    python
    goto end
)

if "%choice%"=="6" (
    echo Bye!
    exit
)

echo Invalid option. Closing...
:end
echo.
pause
