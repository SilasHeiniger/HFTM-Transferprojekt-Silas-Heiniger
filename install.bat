@echo off
echo ====================================
echo Password Manager - Install
echo ====================================
echo.

echo [1/5] Starting database...
docker-compose -f docker-compose.db.yaml up -d

echo.
echo [2/5] Installing dependencies...
if exist uv.lock del uv.lock
uv sync

echo.
echo [3/5] Setting up configuration...
if not exist .env copy .env.example .env

echo.
echo [4/5] Waiting for database...
timeout /t 10 /nobreak >nul

echo.
echo [5/5] Setting up database tables...
uv run python setup_db.py

echo.
echo ====================================
echo Installation Complete!
echo ====================================
echo.
echo Run: start.bat
echo.
pause