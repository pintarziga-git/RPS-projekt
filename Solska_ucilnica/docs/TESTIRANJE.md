# Preverjanje projekta

Pri vsakem primeru izpolnita dejanski rezultat, preden projekt oddasta. Samo prisotnost testa v kodi ne pomeni, da je delovanje že preverjeno.

| Test | Kaj preizkusiva | Pričakovani rezultat | Dejanski rezultat |
|---|---|---|---|
| T1 | Administrator doda predmet | Predmet se pojavi na seznamu | Za preveriti |
| T2 | Administrator doda učitelja in učenca | Oba računa se ustvarita | Za preveriti |
| T3 | Učitelj odpre svoj predmet | Predmet se odpre | Za preveriti |
| T4 | Učenec odpre izbrani predmet | Predmet se odpre | Za preveriti |
| T5 | Učitelj naloži in odstrani gradivo | Gradivo se doda in odstrani | Za preveriti |
| T6 | Učenec odda nalogo | Naloga se shrani | Za preveriti |
| T7 | Ponovna oddaja brez potrditve | Stara naloga ostane | Za preveriti |
| T8 | Ponovna oddaja s potrditvijo | Naloga se zamenja | Za preveriti |
| T9 | Dostop do tujega predmeta/naloge | Dostop je zavrnjen | Za preveriti |
| T10 | Javna stran HTTPS | Stran se odpre prek HTTPS | Za preveriti |
| T11 | Ukaz za 120 testnih računov se izvede dvakrat | Računi se ne podvojijo | Za preveriti |

### Avtomatski testi

Na Windows: `TESTI.bat`. Na Linuxu z Dockerjem: `sudo docker compose exec aplikacija python manage.py test`.

Napake zapišita med GitHub Issues. Ne objavljajta gesel ali osebnih podatkov.
