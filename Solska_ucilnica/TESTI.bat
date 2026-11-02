@echo off
cd /d "%~dp0"
echo Testiranje funkcij s testno SQLite bazo.
docker compose exec -e USE_SQLITE=1 aplikacija python manage.py test ucilnica
pause
