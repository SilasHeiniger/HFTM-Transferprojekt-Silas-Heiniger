@echo off
echo Stopping database...
docker-compose -f docker-compose.db.yaml down
echo.
echo Database stopped!
pause