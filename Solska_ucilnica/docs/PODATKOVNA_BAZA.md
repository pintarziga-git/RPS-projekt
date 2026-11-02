# Podatkovna baza

Uporabljamo MariaDB in Djangove modele. ER-diagram: [slika](ER_diagram.png) / [izvorna datoteka](ER_diagram.dot).

## Glavne tabele

| Tabela | Pomembna polja | Povezava |
|---|---|---|
| `auth_user` | `id` (PK), `username`, `first_name`, `last_name`, `password` | Uporabniki aplikacije; gesla so shranjena kot zgoščene vrednosti. |
| `ucilnica_predmet` | `id` (PK), `naziv` | Šolski predmeti. |
| `ucilnica_gradivo` | `id` (PK), `predmet_id` (FK), `naslov`, `datoteka` | Gradivo pripada enemu predmetu. |
| `ucilnica_naloga` | `id` (PK), `predmet_id` (FK), `ucenec_id` (FK), `naslov`, `datoteka` | Oddana naloga pripada predmetu in učencu. |
| `ucilnica_predmet_ucitelji` | `predmet_id` (FK), `user_id` (FK) | Povezava več-na-več med predmeti in učitelji. |
| `ucilnica_predmet_ucenci` | `predmet_id` (FK), `user_id` (FK) | Povezava več-na-več med predmeti in učenci. |

Django sam ustvari tudi druge sistemske tabele za prijavo, dovoljenja, skupine in seje. Imeni povezovalnih tabel temeljita na modelih iz `ucilnica/models.py`.

## Povezave

- En predmet ima lahko več gradiv in več oddanih nalog.
- En učenec lahko odda več nalog.
- En učitelj lahko poučuje več predmetov; predmet ima lahko več učiteljev.
- En učenec lahko obiskuje več predmetov; predmet ima lahko več učencev.
- Za naloge velja omejitev: isti učenec pri istem predmetu ne more imeti dveh oddaj z enakim naslovom.

## Testni podatki

Ukaz `ustvari_testne_uporabnike --izvozi-gesla` ustvari do 20 testnih učiteljev (`ucitelj1`–`ucitelj20`) in 100 učencev (`ucenec1`–`ucenec100`). Vsak učitelj dobi 2 predmeta, učenec 3. Nove račune ustvari le, če uporabniško ime še ne obstaja. Obstoječih gesel ne spreminja. Naključna gesla so v zasebnem CSV, ki **ne sme na GitHub**.
