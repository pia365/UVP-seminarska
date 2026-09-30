import os  # delo z datotekami in mapami
import time  # čakanje med zahtevki

import requests

import izlusci

# Program je vračal 403; User-Agent pove, kakšen odjemalec pošilja zahtevek.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0.0.0 Safari/537.36"
    )
}
MAPA_HTML = "html"
PREMOR = 4  # sekund med zahtevki
ST_POSKUSOV = 3
LETA = range(2016, 2027)


def pridobi_stran(url, pot):
    """Prenese stran in jo shrani v datoteko.

    Če datoteka že obstaja, se stran ne prenese znova.
    Vrne True, če je stran na voljo.
    """
    if os.path.exists(pot):  # preveri, ali datoteka že obstaja
        return True

    os.makedirs(os.path.dirname(pot), exist_ok=True)  # ustvari mapo

    for poskus in range(1, ST_POSKUSOV + 1):
        try:
            odgovor = requests.get(url, headers=HEADERS, timeout=30)
        except requests.exceptions.RequestException as napaka:
            print(f"Napaka pri {url}: {napaka}")
        else:
            if odgovor.status_code == 200:  # strežnik uspešno vrne stran
                odgovor.encoding = "utf-8"  # sicer se pokvarijo šumniki
                with open(pot, "w", encoding="utf-8") as dat:
                    dat.write(odgovor.text)
                time.sleep(PREMOR)
                return True
            print(f"Koda {odgovor.status_code} pri {url}")
            if odgovor.status_code == 404:
                return False
            if odgovor.status_code == 429:  # preveč zahtevkov
                time.sleep(60)
        time.sleep(PREMOR * poskus * 2)  # čakamo vedno dlje
    return False


def pridobi_sezone(leta):
    for leto in leta:
        url = f"https://www.basketball-reference.com/leagues/NBA_{leto}.html"
        pot = os.path.join(MAPA_HTML, "sezone", f"{leto}.html")
        if pridobi_stran(url, pot):
            print(f"Sezona {leto} je na voljo.")


def pridobi_ekipe(leto):
    """Prenese stran vsake ekipe, ki je igrala v dani sezoni."""
    for ekipa in izlusci.ekipe_v_sezoni(leto):
        kratica = ekipa["kratica"]
        url = f"https://www.basketball-reference.com/teams/{kratica}/{leto}.html"
        pot = os.path.join(MAPA_HTML, "ekipe", f"{kratica}_{leto}.html")
        if pridobi_stran(url, pot):
            print(f"Ekipa {kratica} {leto} je na voljo.")


if __name__ == "__main__":
    pridobi_sezone(LETA)
    pridobi_ekipe(2026)