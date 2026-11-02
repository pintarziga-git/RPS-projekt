@echo off
setlocal
cd /d "%~dp0"
echo.
echo BRISANJE UCITELJEV IN UCENCEV
 echo.
echo Skripta izbrise vse racune brez administratorskih pravic.
echo Admin racuni in predmeti ostanejo. Izgubijo se tudi oddane naloge teh uporabnikov.
echo Pred brisanjem naredi kopijo SQL baze v podmapo kopije.
echo.
choice /C DN /M "Nadaljujem (D=da, N=ne)"
if errorlevel 2 exit /b 0
if not exist kopije mkdir kopije
set "KOPIJA=kopije\baza_pred_brisanjem_%RANDOM%.sql"
echo Shranjujem kopijo: %KOPIJA%
docker compose exec -T baza sh -c "mariadb-dump --user=$MARIADB_USER --password=$MARIADB_PASSWORD $MARIADB_DATABASE" > "%KOPIJA%"
if errorlevel 1 (
  echo Kopija NI uspela. Nic ni bilo izbrisano.
  del "%KOPIJA%" 2>nul
  pause
  exit /b 1
)
echo.
echo Brisem ucence in ucitelje ...
docker compose exec aplikacija python manage.py pocisti_uporabnike --potrdi
if errorlevel 1 (
  echo Brisanje ni uspelo. Kopija baze je v %KOPIJA%.
  pause
  exit /b 1
)
echo.
echo Koncano. Admin racuni so ohranjeni.
pause
