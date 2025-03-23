@echo off
REM Definitions
set RUN_PATH=%~dp0
set INSTALL_DATA_PATH=data

REM Python Definitions
set PY_VER=3.13
set REQ_FILE=%INSTALL_DATA_PATH%\requirements.txt

REM Shortcut Definitions
set VBS_FILE=%RUN_PATH%\%INSTALL_DATA_PATH%\run.vbs
set SHORTCUT_NAME=SRGSSR_News_Downloader.lnk
set SHORTCUT_PATH=%RUN_PATH%
set ICON=%RUN_PATH%\srgssr_news_downloader\res\icon.ico

REM Check if files exist
if not exist "%VBS_FILE%" (
	echo .vbs file is missing. Setup cancelled.
	pause
	exit /b 1
)

if not exist "%REQ_FILE%" (
	echo requirements file is missing. Setup cancelled.
	pause
	exit /b 1
)

if not exist "%ICON%" (
	echo ICON file is missing. Setup cancelled.
	pause
	exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install it via the Microsoft Store.
    pause
    exit /b 1
)

REM Get the Python version
for /f "tokens=2" %%a in ('python --version 2^>^&1') do set python_version=%%a

REM Check if the Python version meets the requirement
if "%python_version%" geq "%PY_VER%" (
    echo Python version %python_version% is compatible.
) else (
    echo Python version %python_version% is not compatible. Python 3.13 or higher needs to be installed via the Microsoft Store.
    pause
    exit /b 1
)

REM Check if pip is installed
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed. Please install Python pip.
    pause
    exit /b 1
)

REM Install dependencies from requirements.txt
echo Installing required modules from requirements.txt...
python -m pip install -r "%REQ_FILE%"

REM Check if pip install was successful
if %errorlevel% neq 0 (
    echo Failed to install required modules.
    pause
    exit /b 1
)

REM Create shortcut to .vbs file
echo Creating shortcut...
set SCRIPT="%TEMP%\create_shortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = "%SHORTCUT_PATH%\%SHORTCUT_NAME%" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%VBS_FILE%" >> %SCRIPT%
echo oLink.IconLocation = "%ICON%, 0" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

echo Finished setup succesfully.
pause