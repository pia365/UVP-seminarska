import sys  # dostop do argumentov, ki jih podamo ob zagonu programa

import izlusci
import pridobi
import shrani

LETA = pridobi.LETA  # sezone, ki jih obdelamo (določene v pridobi.py)


def pridobi_vse(leta):
    """Prenese strani sezon in strani vseh ekip v teh sezonah."""
    pridobi.pridobi_sezone(leta)
    for leto in leta:
        pridobi.pridobi_ekipe(leto)


def zberi_podatke(leta):
    """Iz shranjenih strani izlušči podatke za vse tabele."""
    # igralci je slovar (ključ je ID), da je vsak igralec samo enkrat,
    # čeprav igra v več sezonah in za več ekip.
    ekipe, igralci, nastopi, statistika = [], {}, [], []

    for leto in leta:
        print(f"Izluščujem sezono {leto} ...")
        for ekipa in izlusci.ekipe_v_sezoni(leto):
            ekipe.append(ekipa)
            kratica = ekipa["kratica"]

            for igralec in izlusci.igralci_v_ekipi(kratica, leto):
                # setdefault shrani igralca le, če ga še ni v slovarju.
                igralci.setdefault(igralec["id"], igralec)
                # Isti slovar služi za tabelo nastopi, zato mu dodamo
                # stolpec id_igralca (kopija, original ostane nespremenjen).
                nastopi.append(dict(igralec, id_igralca=igralec["id"]))

            # Statistiko beremo iz dveh tabel na strani ekipe: iz tabele
            # rednega dela sezone in iz tabele končnice.
            for tabela, koncnica in (
                ("per_game_stats", False),
                ("per_game_stats_post", True),
            ):
                zapisi = izlusci.statistika_igralcev(kratica, leto, tabela)
                for zapis in zapisi:
                    zapis["koncnica"] = koncnica  # redni del ali končnica
                    statistika.append(zapis)

    return ekipe, list(igralci.values()), nastopi, statistika


# Ta del se izvede samo, če program zaženemo neposredno (python main.py),
# ne pa, če ga uvozimo iz druge datoteke.
if __name__ == "__main__":
    # Strani prenesemo samo, če ob zagonu podamo besedo "pridobi"
    # (python main.py pridobi), da po nesreči ne sprožimo stotin zahtevkov.
    if len(sys.argv) > 1 and sys.argv[1] == "pridobi":
        pridobi_vse(LETA)

    podatki = zberi_podatke(LETA)
    shrani.shrani_vse(*podatki)  # * razpakira četvorko v štiri argumente
    ekipe, igralci, nastopi, statistika = podatki
    print(
        f"Ekipe: {len(ekipe)}, igralci: {len(igralci)}, "
        f"nastopi: {len(nastopi)}, statistika: {len(statistika)}"
    )