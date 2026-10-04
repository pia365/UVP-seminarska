import sys

import izlusci
import pridobi
import shrani

LETA = pridobi.LETA


def pridobi_vse(leta):
    """Prenese strani sezon in strani vseh ekip v teh sezonah."""
    pridobi.pridobi_sezone(leta)
    for leto in leta:
        pridobi.pridobi_ekipe(leto)


def zberi_podatke(leta):
    """Iz shranjenih strani izlušči podatke za vse tabele."""
    ekipe, igralci, nastopi, statistika = [], {}, [], []

    for leto in leta:
        for ekipa in izlusci.ekipe_v_sezoni(leto):
            ekipe.append(ekipa)
            kratica = ekipa["kratica"]

            for igralec in izlusci.igralci_v_ekipi(kratica, leto):
                igralci.setdefault(igralec["id"], igralec)
                nastopi.append(dict(igralec, id_igralca=igralec["id"]))

            for tabela, koncnica in (
                ("per_game_stats", False),
                ("per_game_stats_post", True),
            ):
                for zapis in izlusci.statistika_igralcev(kratica, leto, tabela):
                    zapis["koncnica"] = koncnica
                    statistika.append(zapis)

    return ekipe, list(igralci.values()), nastopi, statistika


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pridobi":
        pridobi_vse(LETA)

    podatki = zberi_podatke(LETA)
    shrani.shrani_vse(*podatki)
    ekipe, igralci, nastopi, statistika = podatki
    print(
        f"Ekipe: {len(ekipe)}, igralci: {len(igralci)}, "
        f"nastopi: {len(nastopi)}, statistika: {len(statistika)}"
    )