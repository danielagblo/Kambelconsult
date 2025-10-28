@echo off
echo ==========================================
echo Kambel Consult - Project Setup
echo ==========================================
echo.

REM Check if Python 3 is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv .venv

echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Installing Django dependencies...
cd django_admin
pip install -r requirements.txt
cd ..

REM Create necessary directories
echo.
echo Creating necessary directories...
if not exist data mkdir data
if not exist static\uploads mkdir static\uploads
if not exist django_admin\media mkdir django_admin\media
if not exist django_admin\static mkdir django_admin\static

REM Set up Django database
echo.
echo Setting up Django database...
cd django_admin
python manage.py migrate
cd ..

echo.
echo ==========================================
echo Setup complete!
echo ==========================================
echo.
echo To activate the virtual environment in the future:
echo   .venv\Scripts\activate
echo.
echo To start the development server:
echo   python app.py
echo.
echo To access Django admin panel:
echo   cd django_admin ^&^& python manage.py runserver 8000
echo   Then visit: http://localhost:8000/admin
echo.
echo To create a Django superuser:
echo   cd django_admin ^&^& python manage.py createsuperuser
echo.

pause

