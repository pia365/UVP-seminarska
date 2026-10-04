# Analiza lige NBA (sezone 2016–2026)

Projektna naloga pri predmetu Uvod v programiranje.

Program s spletne strani [Basketball-Reference](https://www.basketball-reference.com) zajame podatke o ekipah in igralcih lige NBA za enajst sezon, jih shrani v štiri povezane CSV tabele in v Jupyter Notebooku analizira, kako se je igra spreminjala.

## Vir podatkov

Podatki so zajeti v dveh ravneh:

1. stran vsake sezone (`/leagues/NBA_<leto>.html`) vsebuje seznam ekip in njihovo statistiko,
2. stran vsake ekipe v sezoni (`/teams/<KRATICA>/<leto>.html`) vsebuje seznam igralcev ter njihovo statistiko na tekmo v rednem delu sezone in v končnici.

Leto pri sezoni pomeni leto, v katerem se sezona konča (npr. 2026 je sezona 2025/26).

## Struktura projekta

| Datoteka | Naloga |
|---|---|
| `pridobi.py` | prenos strani s `requests`, predpomnjenje v mapo `html/`, premor med zahtevki, ponovni poskusi |
| `izlusci.py` | izluščenje podatkov iz HTML-ja z regularnimi izrazi |
| `shrani.py` | zapis podatkov v CSV tabele |
| `main.py` | zagon celotnega postopka |
| `analiza.ipynb` | analiza podatkov in grafi |
| `podatki/` | CSV tabele (del repozitorija) |
| `html/` | shranjene spletne strani (zaradi velikosti niso v repozitoriju) |
| `uporaba-ui.md` | dokumentacija uporabe umetne inteligence |

## Zagon

Potrebne knjižnice: `requests`, `pandas`, `matplotlib`, `jupyter`.

```
pip install requests pandas matplotlib jupyter
python main.py pridobi    # prenese strani (ok. 20 minut) in izlušči podatke
python main.py            # samo izlušči podatke iz že shranjenih strani
```

Prenos strani je prvič počasen, ker program med zahtevki počaka nekaj sekund, da ne preobremeni strežnika. Že prenesene strani se ob ponovnem zagonu ne prenašajo znova.

## Tabele

- `ekipe.csv`: ekipa in sezona, zmage, porazi, točke in prejete točke na tekmo, razlika v točkah (SRS), uvrstitev v končnico,
- `igralci.csv`: podatki o igralcu, ki se ne spreminjajo (ime, datum rojstva, država, fakulteta),
- `nastopi.csv`: igralec v ekipi v določeni sezoni (številka dresa, pozicija, višina, teža, izkušnje),
- `statistika.csv`: statistika igralca na tekmo v ekipi in sezoni, ločeno za redni del in končnico (stolpec `koncnica`).

Tabele povezujeta `id_igralca` ter par `kratica` in `leto`.

## Pasti v podatkih

- Igralec, ki je bil v sezoni zamenjan, ima več vrstic (po eno za vsako ekipo).
- Nekateri igralci so na seznamu ekipe, vendar v sezoni niso odigrali nobene tekme, zato nimajo vrstice statistike.
- Sezoni 2020 in 2021 sta bili krajši, zato so podatki o tekmah preračunani z dejanskim številom tekem ekipe.
- Statistika na tekmo je na strani zaokrožena na eno decimalko, zato so ekipne vsote, izračunane iz igralskih, približne.
- Odstotki meta so prazni, če igralec ni oddal nobenega meta.
- Minute in statistika so zapisane po ekipah: igralec, ki je bil zamenjan, ima za vsako ekipo svojo vrstico.
- Polje fakultete je prazno pri igralcih, ki niso igrali na ameriški fakulteti (npr. tuji klubi).

## Analiza

Rezultati so v `analiza.ipynb`. Vprašanja so razvrščena v tri skupine:

**A. Kako se je liga spreminjala skozi čas**
1. Kako se je spremenila igra (poskusi in zadetki za tri točke po sezonah)?
2. Ali so igralci v ligi starejši?
3. Kolikšen delež igralcev ni rojen v ZDA?

**B. Ekipe**

4. Katere ekipe so najuspešnejše (povprečni delež zmag)?
5. Katere sezone ekip so bile najboljše?
6. Kaj loči uspešne ekipe (trojke, razlika v točkah, delež zmag)?

**C. Igralci**

7. Kdo so najboljši točkovalci (točke na 36 minut)?
8. Kdo je dosegel največ točk, skokov in asistenc?
9. Ali pozicija vpliva na skoke in asistence?
10. Kako visoki so igralci?
11. Iz katerih fakultet prihajajo igralci?

## Uporaba umetne inteligence

Pri nastajanju projekta je bila uporabljena umetna inteligenca (Claude). Celoten potek pogovora je v datoteki `uporaba-ui.md`.
