@echo off
cd /d "%~dp0"
echo ==============================================
echo   KINETIC ENERGY ARCADE 2.0 - SETUP
echo ==============================================
py -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Package installation failed. Check that Python is installed and try again.
  pause
  exit /b 1
)
echo.
echo Starting Kinetic Energy Arcade...
py -m streamlit run app.py
if errorlevel 1 pause
