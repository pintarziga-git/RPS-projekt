@echo off
cd /d "%~dp0"
docker compose down
echo Projekt je ustavljen. Podatki so ohranjeni.
pause
