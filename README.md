# Analiza lige NBA (sezone 2016–2026)

Projektna naloga pri predmetu Uvod v programiranje (FMF, Univerza v Ljubljani).

Program s spletne strani [Basketball-Reference](https://www.basketball-reference.com) zajame podatke o ekipah in igralcih lige NBA za enajst sezon, jih shrani v štiri povezane CSV tabele in v Jupyter Notebooku analizira, kako se je igra spreminjala in kdo so najpomembnejši igralci.

## Vir podatkov

Podatki so zajeti v dveh ravneh:

1. stran vsake sezone (`/leagues/NBA_<leto>.html`) vsebuje seznam ekip in njihovo statistiko,
2. stran vsake ekipe v sezoni (`/teams/<KRATICA>/<leto>.html`) vsebuje seznam igralcev ter njihovo statistiko na tekmo v rednem delu sezone in v končnici.

Leto pri sezoni pomeni leto, v katerem se sezona konča (npr. 2026 je sezona 2025/26). Skupaj je 341 prenesenih strani (11 strani sezon in 330 strani ekip).

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

Program je preizkušen s Pythonom 3.13. Potrebne knjižnice: `requests`, `pandas`, `matplotlib`, `jupyter`.

```
pip install requests pandas matplotlib jupyter
python main.py pridobi    # prenese strani (približno 25 minut) in izlušči podatke
python main.py            # samo izlušči podatke iz že shranjenih strani
```

Prenos strani je prvič počasen, ker program med zahtevki počaka nekaj sekund, da ne preobremeni strežnika. Že prenesene strani se ob ponovnem zagonu ne prenašajo znova.

Analizo odpreš v datoteki `analiza.ipynb` (Jupyter Notebook ali Visual Studio Code). Zvezek bere samo CSV datoteke iz mape `podatki/`, zato za zagon ne potrebuje prenosa strani. CSV datoteke so že priložene.

## Tabele

| Tabela | Vsebina | Vrstic |
|---|---|---|
| `ekipe.csv` | ekipa in sezona, zmage, porazi, točke in prejete točke na tekmo, razlika v točkah (SRS), uvrstitev v končnico | 330 |
| `igralci.csv` | podatki o igralcu, ki se ne spreminjajo (ime, datum rojstva, država, fakulteta) | 1556 |
| `nastopi.csv` | igralec v ekipi v določeni sezoni (številka dresa, pozicija, višina, teža, izkušnje) | 6819 |
| `statistika.csv` | statistika igralca na tekmo v ekipi in sezoni, ločeno za redni del in končnico (stolpec `koncnica`) | 9215 |

Tabele povezujeta `id_igralca` ter par `kratica` in `leto`. Podatki, ki se za igralca ne spreminjajo, so samo v tabeli `igralci`, zato se ne ponavljajo pri vsaki sezoni (normalizacija).

## Pasti v podatkih

- Igralec, ki je bil v sezoni zamenjan, ima več vrstic (po eno za vsako ekipo), minute in statistika pa so zapisane po ekipah.
- Nekateri igralci so na seznamu ekipe, vendar v sezoni niso odigrali nobene tekme, zato nimajo vrstice statistike.
- Sezoni 2020 in 2021 sta bili krajši, zato je delež zmag izračunan z dejanskim številom tekem ekipe.
- Statistika na tekmo je na strani zaokrožena na eno decimalko, zato so vsote, izračunane iz nje, približne.
- Odstotki metov so prazni, če igralec ni oddal nobenega meta te vrste.
- Polje fakultete je prazno pri igralcih, ki niso igrali na ameriški fakulteti (npr. tuji klubi).
- Končnica je zajeta v tabeli `statistika` (stolpec `koncnica`), vendar je analiza ne uporablja.

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

### Glavne ugotovitve

- Ekipe so med sezonama 2016 in 2026 bistveno več metale trojke (poskusi so se povečali s 24,1 na 37,0 na tekmo), točke ekipe pa so zrasle precej manj.
- Delež zmag je najmočneje povezan z razliko med doseženimi in prejetimi točkami (korelacija 0,97), zadete trojke imajo zmerno povezavo (0,36).
- Najuspešnejša ekipa v povprečju enajstih sezon so Boston Celtics, najboljša posamezna sezona pa sezona 2016 Golden State Warriors (73 zmag).
- Pozicija močno vpliva na skoke, asistence in višino igralcev.

## Uporaba umetne inteligence

Pri nastajanju projekta sem uporabljala umetno inteligenco (Claude). Kaj je naredila ona in kaj sem naredila jaz, je opisano v datoteki `uporaba-ui.md`, celoten potek pogovora pa je v datoteki `uporaba-ui-celoten-pogovor.md`.