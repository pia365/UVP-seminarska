import csv
import os

import izlusci

MAPA_PODATKI = "podatki"  # mapa, kamor zapišemo CSV datoteke

# Stolpci vsake tabele (vrstni red stolpcev v CSV datoteki).
# Podatki so razdeljeni v štiri povezane tabele, da se isti podatki ne
# ponavljajo: podatki o igralcu, ki se ne spreminjajo, so le v `igralci`,
# tisto, kar velja za eno sezono, pa v `nastopi` in `statistika`.
POLJA_EKIPE = [
    "kratica", "leto", "ime", "play_off", "zmage", "porazi",
    "tocke_na_tekmo", "prejete_tocke_na_tekmo", "srs",
]
POLJA_IGRALCI = ["id", "ime", "datum_rojstva", "drzava", "fakulteta"]
POLJA_NASTOPI = [
    "id_igralca", "kratica", "leto", "stevilka", "pozicija",
    "visina_cm", "teza_lb", "izkusnje",
]
# Naša imena stolpcev statistike vzamemo iz izlusci.py, da jih ni treba
# prepisovati na dveh mestih.
POLJA_STATISTIKA = ["id_igralca", "kratica", "leto", "koncnica"] + [
    ime for ime, _ in izlusci.POLJA_STATISTIKE.values()
]


def shrani_csv(ime_datoteke, polja, vrstice):
    """Zapiše seznam slovarjev v CSV datoteko v mapi podatki."""
    os.makedirs(MAPA_PODATKI, exist_ok=True)  # mapo ustvarimo, če je ni
    pot = os.path.join(MAPA_PODATKI, ime_datoteke)
    # newline="" pustimo csv modulu, da sam poskrbi za konce vrstic
    # (sicer bi bile na Windows med vrsticami prazne vrstice).
    with open(pot, "w", encoding="utf-8", newline="") as dat:
        # extrasaction="ignore": slovar lahko vsebuje več ključev, kot jih
        # potrebuje tabela; odvečne preprosto preskočimo.
        pisatelj = csv.DictWriter(
            dat, fieldnames=polja, extrasaction="ignore"
        )
        pisatelj.writeheader()  # prva vrstica: imena stolpcev
        pisatelj.writerows(vrstice)  # nato po ena vrstica za vsak slovar


def shrani_vse(ekipe, igralci, nastopi, statistika):
    """Zapiše vse štiri tabele v CSV datoteke."""
    shrani_csv("ekipe.csv", POLJA_EKIPE, ekipe)
    shrani_csv("igralci.csv", POLJA_IGRALCI, igralci)
    shrani_csv("nastopi.csv", POLJA_NASTOPI, nastopi)
    shrani_csv("statistika.csv", POLJA_STATISTIKA, statistika)