# Preverjanje projekta

Pri vsakem primeru izpolnita dejanski rezultat, preden projekt oddasta. Samo prisotnost testa v kodi ne pomeni, da je delovanje že preverjeno.

| Test | Kaj preizkusiva | Pričakovani rezultat 
|---|---|---|---|
| T1 | Administrator doda predmet | Predmet se pojavi na seznamu 
| T2 | Administrator doda učitelja in učenca | Oba računa se ustvarita 
| T3 | Učitelj odpre svoj predmet | Predmet se odpre  
| T4 | Učenec odpre izbrani predmet | Predmet se odpre 
| T5 | Učitelj naloži in odstrani gradivo | Gradivo se doda in odstrani 
| T6 | Učenec odda nalogo | Naloga se shrani |
| T7 | Ponovna oddaja brez potrditve | Stara naloga ostane 
| T8 | Ponovna oddaja s potrditvijo | Naloga se zamenja 
| T9 | Dostop do tujega predmeta/naloge | Dostop je zavrnjen 
| T10 | Javna stran HTTPS | Stran se odpre prek HTTPS 
| T11 | Ukaz za 120 testnih računov se izvede dvakrat | Računi se ne podvojijo 


Na Windows: `TESTI.bat`. Na Linuxu z Dockerjem: `sudo docker compose exec aplikacija python manage.py test`.


