import os  # delo z datotekami in mapami
import time  # čakanje med zahtevki

import requests  # pošiljanje zahtevkov na spletne strani

import izlusci  # iz strani sezone preberemo seznam ekip

OSNOVNI_URL = "https://www.basketball-reference.com"
MAPA_HTML = "html"  # mapa, kamor shranimo prenesene strani
PREMOR = 4  # sekund čakanja med zahtevki, da ne preobremenimo strežnika
ST_POSKUSOV = 3  # največ toliko poskusov prenosa ene strani
LETA = range(2016, 2027)  

# Strežnik zavrne zahtevke, ki niso videti kot brskalnik (koda 403).
# User-Agent pove, kakšen odjemalec pošilja zahtevek, zato se predstavimo
# kot običajen brskalnik.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0.0.0 Safari/537.36"
    )
}


def pridobi_stran(url, pot):
    """Prenese stran in jo shrani v datoteko.

    Če datoteka že obstaja, se stran ne prenese znova.
    Vrne True, če je stran na voljo, sicer False.
    """
    # Predpomnjenje: že shranjene strani ne prenašamo še enkrat.
    if os.path.exists(pot):
        return True

    # Mapo za datoteko ustvarimo, če še ne obstaja.
    os.makedirs(os.path.dirname(pot), exist_ok=True)

    for poskus in range(1, ST_POSKUSOV + 1):
        try:
            odgovor = requests.get(url, headers=HEADERS, timeout=30)
        except requests.exceptions.RequestException as napaka:
            # Težava s povezavo (npr. ni interneta): izpišemo napako.
            print(f"Napaka pri {url}: {napaka}")
        else:
            if odgovor.status_code == 200:  # 200 = stran je bila prenesena
                # Brez tega se šumniki in tuji znaki pokvarijo.
                odgovor.encoding = "utf-8"
                with open(pot, "w", encoding="utf-8") as dat:
                    dat.write(odgovor.text)
                time.sleep(PREMOR)  # premor pred naslednjim zahtevkom
                return True
            print(f"Koda {odgovor.status_code} pri {url}")
            if odgovor.status_code == 404:  # strani ni, ponovitev ne pomaga
                return False
            if odgovor.status_code == 429:  # preveč zahtevkov: počakamo
                time.sleep(60)
        time.sleep(PREMOR * poskus * 2)  # vedno daljše čakanje (8, 16, 24 s)
    return False


def pridobi_sezone(leta):
    """Prenese stran vsake sezone iz danega zaporedja let."""
    for leto in leta:
        url = f"{OSNOVNI_URL}/leagues/NBA_{leto}.html"
        pot = os.path.join(MAPA_HTML, "sezone", f"{leto}.html")
        if pridobi_stran(url, pot):
            print(f"Sezona {leto} je na voljo.")


def pridobi_ekipe(leto):
    """Prenese stran vsake ekipe, ki je igrala v dani sezoni."""
    for ekipa in izlusci.ekipe_v_sezoni(leto):
        kratica = ekipa["kratica"]
        url = f"{OSNOVNI_URL}/teams/{kratica}/{leto}.html"
        pot = os.path.join(MAPA_HTML, "ekipe", f"{kratica}_{leto}.html")
        if pridobi_stran(url, pot):
            print(f"Ekipa {kratica} {leto} je na voljo.")

