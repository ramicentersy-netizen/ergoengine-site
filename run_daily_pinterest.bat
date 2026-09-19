@echo off
cd /d C:\Users\TOPTECH\Desktop\AI-Affiliate-Engine

:: 1. تفعيل البيئة الافتراضية
call .venv\Scripts\activate.bat

:: 2. تنزيل وتصميم صور جديدة إذا كان المخزون بحاجة لتعزيز
python daily_content_engine.py

:: 3. تشغيل كروم في وضع التحكم إذا لم يكن قيد التشغيل مسبقاً
tasklist /FI "IMAGENAME eq chrome.exe" 2>NUL | find /I /N "chrome.exe">NUL
if "%ERRORLEVEL%"=="1" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebugProfile"
    timeout /t 6 /nobreak >nul
)

:: 4. رفع وجدولة حصة اليوم (2-3 دبابيس)
python auto_pin_uploader.py

exit