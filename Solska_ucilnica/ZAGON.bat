@echo off
cd /d "%~dp0"
echo.
echo SOLSKA UCILNICA - ZAGON
 echo.
echo Ce je prejsnji projekt se odprt, ga najprej ustavi v Docker Desktop.
echo.
docker compose up --build -d
if errorlevel 1 (
  echo.
  echo NAPAKA: Preveri, ali je Docker Desktop odprt in ali so vrata 8000 prosta.
  pause
  exit /b 1
)
echo.
echo Projekt se zaganja. Preveri stanje z: docker compose ps
echo Ko je aplikacija zagnana, odpri http://localhost:8000
echo Administracija: http://localhost:8000/admin/
echo.
pause
