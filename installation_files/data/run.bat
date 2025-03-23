@echo off
REM Check Python version installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed on this machine. Please install Python 3.13 or higher. Python can be installed via the Microsoft Store.
    pause
    exit
)

REM Get the Python version
for /f "tokens=2" %%a in ('python --version 2^>^&1') do set python_version=%%a

REM Check if the Python version meets the requirement
if "%python_version%" geq "3.13" (
	cd.
    pythonw -m srgssr_news_downloader
) else (
    echo Python version %python_version% is not compatible. Python 3.13 or higher needs to be installed.
	pause
	exit
)
pause
exit