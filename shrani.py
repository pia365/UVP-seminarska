import csv
import os

import izlusci

MAPA_PODATKI = "podatki"

POLJA_EKIPE = [
    "kratica", "leto", "ime", "play_off", "zmage", "porazi",
    "tocke_na_tekmo", "prejete_tocke_na_tekmo", "srs",
]
POLJA_IGRALCI = ["id", "ime", "datum_rojstva", "drzava", "fakulteta"]
POLJA_NASTOPI = [
    "id_igralca", "kratica", "leto", "stevilka", "pozicija",
    "visina_cm", "teza_lb", "izkusnje",
]
POLJA_STATISTIKA = ["id_igralca", "kratica", "leto", "koncnica"] + [
    ime for ime, _ in izlusci.POLJA_STATISTIKE.values()
]


def shrani_csv(ime_datoteke, polja, vrstice):
    """Zapiše seznam slovarjev v CSV datoteko v mapi podatki."""
    os.makedirs(MAPA_PODATKI, exist_ok=True)
    pot = os.path.join(MAPA_PODATKI, ime_datoteke)
    with open(pot, "w", encoding="utf-8", newline="") as dat:
        pisatelj = csv.DictWriter(dat, fieldnames=polja, extrasaction="ignore")
        pisatelj.writeheader()
        pisatelj.writerows(vrstice)


def shrani_vse(ekipe, igralci, nastopi, statistika):
    shrani_csv("ekipe.csv", POLJA_EKIPE, ekipe)
    shrani_csv("igralci.csv", POLJA_IGRALCI, igralci)
    shrani_csv("nastopi.csv", POLJA_NASTOPI, nastopi)
    shrani_csv("statistika.csv", POLJA_STATISTIKA, statistika)