@echo off
cd /d "%~dp0"
echo Ustvarjanje testnih uporabnikov ...
echo Gesla se shranijo v zasebno datoteko testni_racuni.csv.
if exist "testni_racuni.csv" (
    echo testni_racuni.csv ze obstaja. Ne bom ga prepisal.
    pause
    exit /b 1
)
docker compose exec -T aplikacija python manage.py ustvari_testne_uporabnike --izvozi-gesla > testni_racuni.csv
if errorlevel 1 (
    echo Prislo je do napake. Preveri Docker.
) else (
    echo Koncano. Datoteke testni_racuni.csv NE nalagaj na GitHub.
)
pause
