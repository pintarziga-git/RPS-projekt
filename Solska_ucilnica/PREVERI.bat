@echo off
cd /d "%~dp0"
echo PREGLED VSEBNIKOV
docker compose ps
echo.
echo ZADNJI ZAPISI APLIKACIJE
docker compose logs --tail=25 aplikacija
echo.
pause
