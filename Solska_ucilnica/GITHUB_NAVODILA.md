# Objava na GitHub

1. V https://github.com se prijavi ali ustvari račun.
2. Izberi **New repository** in napiši `solska-ucilnica`. Za šolski projekt lahko začneš z **Private**.
3. Pri ustvarjanju ne dodaj samodejnega README, da ne bo konflikta.
4. Razširi ZIP in odpri mapo `solska_ucilnica_koncna` v VS Code.
5. V terminalu VS Code preveri, da imaš Git (`git --version`), nato zaženi:

```bash
git init
git add .
git commit -m "Zacetni projekt solska ucilnica"
git branch -M main
git remote add origin https://github.com/TVOJE_UPORABNISKO_IME/solska-ucilnica.git
git push -u origin main
```

Besedilo `TVOJE_UPORABNISKO_IME` zamenjaj s svojim dejanskim GitHub uporabniškim imenom. GitHub te lahko pozove k prijavi v brskalniku.

6. V repozitoriju odpri **Settings → Collaborators** in povabi drugega dijaka.
7. Odpri **Issues** in dodaj dejanske naloge ali napake. Oba člana naj prispevata svoje spremembe.

**Varnost:** `.env` in CSV z gesli nista v ZIP-u in ju `.gitignore` izključuje. Pred objavo vseeno preveri `git status` in `git diff --cached --name-only`. Če vidiš datoteko z gesli, jo odstrani iz stage: `git restore --staged IME_DATOTEKE`.
