@echo off
echo 🚀 Starting Django Server for Android Access
echo ================================================

echo 📱 Finding your computer's IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set IP=%%a
    goto :found
)

:found
set IP=%IP: =%
echo 🌐 Your IP Address: %IP%
echo 📱 Android Access URL: http://%IP%:8000

echo.
echo 🔧 Setting up Django (if needed)...
if not exist db.sqlite3 (
    echo 📊 Creating database...
    python manage.py makemigrations
    python manage.py migrate
    echo 👤 Creating admin user...
    python manage.py setup_voting --create-admin --create-candidates
) else (
    echo ✅ Database already exists
)

echo.
echo 🔥 FIREWALL NOTICE:
echo If Windows Firewall popup appears, click "Allow access"
echo This lets your Android device connect to the server.

echo.
echo 📱 ANDROID INSTRUCTIONS:
echo 1. Connect your Android to the same WiFi network
echo 2. Open browser on Android
echo 3. Go to: http://%IP%:8000
echo 4. Enjoy your mobile voting system!

echo.
echo 🔑 Admin Login:
echo    Email: admin@votingsystem.com
echo    Password: admin123

echo.
echo 🚀 Starting server...
echo Press Ctrl+C to stop
echo ================================================

python manage.py runserver 0.0.0.0:8000

pause