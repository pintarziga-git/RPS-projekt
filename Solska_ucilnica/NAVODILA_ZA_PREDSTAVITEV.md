# Kratka predstavitev projekta

**Cilj:** Izdelati spletno učilnico za šolsko delo na daljavo.

**Orodja:** Python, Django, HTML, CSS, MariaDB, Docker, Nginx in GitHub.

**Podatki:** Predmet, gradivo in oddana naloga. Učence in učitelje predstavljajo uporabniki sistema. Relacije: učitelji–predmeti, učenci–predmeti ter naloge–učenci–predmeti.

**Pogledi:**

1. Administrator v administraciji dodaja/ureja/briše uporabnike in predmete.
2. Učitelj vidi samo predmete, ki jih poučuje, lahko naloži gradivo ali pogleda oddane naloge.
3. Učenec si izbere predmete, prenese gradivo in odda nalogo. Pri ponovni oddaji potrdi zamenjavo.

**Predlagana demonstracija:**

1. Prijavi se kot admin in pokaži urejanje predmetov.
2. Prijavi se kot `ucitelj1`, odpri Matematiko, dodaj gradivo.
3. Prijavi se kot `ucenec1`, odpri Matematiko, prenesi gradivo in oddaj nalogo.
4. Vrni se kot učitelj in pokaži oddano nalogo.
5. Pokaži Docker Desktop, da se aplikacija in baza zaganjata v ločenih vsebnikih.

**Varnost:** Gesla so zgoščena z Django mehanizmom, uporabniki ne morejo prenesti tujih datotek, obrazci uporabljajo CSRF zaščito, datoteke so omejene po vrsti in velikosti.

**Javni naslov za predstavitev:** https://solska-ucilnica2026.duckdns.org – na Ubuntu strežniku Oracle Cloud uporablja Caddy in HTTPS. Pred predstavitvijo preveri delovanje strani.
