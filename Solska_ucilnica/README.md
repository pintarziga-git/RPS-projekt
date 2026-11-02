# Šolska učilnica

Preprosta spletna učilnica za šolski projekt dveh dijakov. Aplikacija je narejena s Pythonom, Djangom in MariaDB. Za zagon uporablja Docker.

**Javna stran:** https://solska-ucilnica2026.duckdns.org (delovanje je odvisno od strežnika Oracle Cloud).

## Kaj omogoča

- **Administrator** dodaja in ureja uporabnike ter predmete.
- **Učitelj** vidi svoje predmete, dodaja gradiva in pregleduje oddane naloge.
- **Učenec** izbira predmete, prenaša gradiva in oddaja naloge.

## Dokumentacija

- [Projektna dokumentacija (Word)](docs/Projektna_dokumentacija_Solska_ucilnica.docx)
- [ER-diagram](docs/ER_diagram.png)
- [Opis tabel in povezav](docs/PODATKOVNA_BAZA.md)
- [Skice uporabniškega vmesnika](docs/skice.png)
- [Diagram zgradbe aplikacije](docs/arhitektura.png)
- [Testni primeri](docs/TESTIRANJE.md)
- [Delo dveh članov](docs/DELO_SKUPINE.md)

## Lokalni zagon (Windows)

1. Namesti Docker Desktop in ga zaženi.
2. Kopiraj `.env.example` v `.env`, zamenjaj VSA označena gesla in `SECRET_KEY` z naključnimi vrednostmi.
3. V mapi projekta zaženi `ZAGON.bat` ali `docker compose up -d --build`.
4. Odpri http://localhost:8000. Administrator je na `/admin/`.
5. Pravega administratorja ustvari z `docker compose exec aplikacija python manage.py createsuperuser`.

Za konec uporabimo `USTAVI.bat` ali `docker compose down` (brez `-v`, da ostanejo podatki).

## Ponovno ustvari 20 učiteljev in 100 učencev

Ustvarjeni računi so **izmišljeni**, namenjeni samo predstavitvi. Privzetih skupnih gesel ni. Vsak novi uporabnik dobi svoje naključno geslo.

**Windows:** zaženi `USTVARI_120_UPORABNIKOV.bat` v mapi projekta. Gesla so v lokalni datoteki `testni_racuni.csv`. Datoteke ne objavi.

**Oracle Cloud / Ubuntu:** če imaš že nameščeno posodobljeno kodo, v mapi projekta zaženi:

```bash
bash USTVARI_120_UPORABNIKOV_LINUX.sh
```

Če na Oracle še teče prejšnja različica kode, lahko brez njene zamenjave na strežnik preneseš in zaženeš `USTVARI_120_NA_OBSTOJECEM_ORACLE.sh`. CSV z novimi gesli se shrani v `/home/ubuntu/testni_racuni.csv` in ni del repozitorija. Ob ponovnem izvajanju ukaz že obstoječih računov ne spremeni ali podvoji. Za novo kodo v vsebniku je potrebna ponovna gradnja Docker slike (`sudo docker compose up -d --build`), brez brisanja volumnov.

Za preizkus najprej naredi varnostno kopijo baze. Na javni strani naj bodo testni računi dovoljeni le med predstavitvijo in z ustreznimi pravicami. Računi imajo običajne pravice učencev/učiteljev, ne administratorskih.

## Kaj je še treba preveriti pred oddajo

- Izvesti teste iz `docs/TESTIRANJE.md` in zapisati dejanske rezultate.
- Dodati člana skupine v GitHub repozitorij in imeti zgodovino sprememb obeh.
- V Wordovi dokumentaciji po potrebi osvežiti stanje projekta (javni HTTPS je bil pozneje nastavljen).
- Preveriti varnostne kopije, požarni zid in delovanje po ponovnem zagonu strežnika.
- Nikoli ne objaviti `.env`, SSH ključev, DuckDNS tokena ali CSV z gesli.

## Zgradba projekta

- `ucilnica/models.py` – podatkovni modeli.
- `ucilnica/views.py` in `ucilnica/upravljanje.py` – logika spletnih strani.
- `ucilnica/forms.py` – obrazci.
- `templates/`, `static/` – videz aplikacije.
- `docker-compose.yml` – storitve baze, aplikacije in Nginxa.
- `ucilnica/management/commands/ustvari_testne_uporabnike.py` – testni uporabniki.
