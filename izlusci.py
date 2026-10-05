import datetime
import html
import os
import re

MAPA_HTML = "html"  # mapa s shranjenimi stranmi (jih ustvari pridobi.py)

# Podatke iz HTML-ja izluščimo v dveh korakih: najprej z enim vzorcem
# poiščemo vrstico tabele (<tr>), nato z drugim v njej posamezne celice (<td>).

# Vrstica tabele na strani sezone: povezava do ekipe in vse celice za njo.
VZOREC_EKIPE = re.compile(
    r'<tr[^>]*>\s*<th[^>]*data-stat="team_name"[^>]*>'
    r'<a href="/teams/(?P<kratica>[A-Z]{3})/(?P<leto>\d{4})\.html">'
    r"(?P<ime>[^<]+)</a>(?P<zvezdica>\*?)</th>"
    r"(?P<celice>.*?)</tr>",
    re.DOTALL,
)

# Ena celica v vrstici ekipe: ime polja (data-stat) in vrednost.
VZOREC_CELICE_EKIPE = re.compile(
    r'data-stat="(?P<polje>\w+)"[^>]*>(?P<vrednost>[^<]*)</td>'
)

# Vrstica tabele igralcev na strani ekipe: številka, ID in ime igralca.
VZOREC_IGRALCA = re.compile(
    r'<tr\s*><th[^>]*data-stat="number"[^>]*>(?P<stevilka>[^<]*)</th>\s*'
    r'<td[^>]*data-append-csv="(?P<id>\w+)"[^>]*data-stat="player"[^>]*>'
    r'<a href="[^"]*">(?P<ime>[^<]+)</a></td>'
    r"(?P<celice>.*?)</tr>",
    re.DOTALL,
)

# Ena celica v vrstici igralca: atributi in vsebina (lahko vsebuje značke).
VZOREC_TD = re.compile(
    r"<td(?P<atributi>[^>]*)>(?P<vsebina>.*?)</td>", re.DOTALL
)

# Vrstica tabele statistike na tekmo: ID igralca in vse celice za njim.
VZOREC_STATISTIKE = re.compile(
    r'<tr[^>]*>\s*<th[^>]*data-stat="ranker"[^>]*>[^<]*</th>\s*'
    r'<td[^>]*data-append-csv="(?P<id>\w+)"[^>]*data-stat="name_display"[^>]*>'
    r".*?</td>(?P<celice>.*?)</tr>",
    re.DOTALL,
)

# Polja iz tabele statistike: ime polja na strani -> (naše ime, tip vrednosti).
POLJA_STATISTIKE = {
    "age": ("starost", int),
    "games": ("tekme", int),
    "games_started": ("zacetne_tekme", int),
    "mp_per_g": ("minute", float),
    "fg_per_g": ("meti", float),
    "fga_per_g": ("meti_poskusi", float),
    "fg_pct": ("meti_odstotek", float),
    "fg3_per_g": ("trojke", float),
    "fg3a_per_g": ("trojke_poskusi", float),
    "fg3_pct": ("trojke_odstotek", float),
    "ft_per_g": ("prosti_meti", float),
    "fta_per_g": ("prosti_meti_poskusi", float),
    "ft_pct": ("prosti_meti_odstotek", float),
    "orb_per_g": ("skoki_napad", float),
    "drb_per_g": ("skoki_obramba", float),
    "trb_per_g": ("skoki", float),
    "ast_per_g": ("asistence", float),
    "stl_per_g": ("ukradene", float),
    "blk_per_g": ("blokade", float),
    "tov_per_g": ("izgubljene", float),
    "pf_per_g": ("osebne", float),
    "pts_per_g": ("tocke", float),
}


# --- Pomožne funkcije --------------------------------------------------


def preberi_stran(pot):
    """Prebere shranjeno spletno stran in vrne njeno besedilo."""
    with open(pot, encoding="utf-8") as dat:
        return dat.read()


def pocisti(besedilo):
    """Odstrani HTML značke, pretvori posebne znake in odvečne presledke."""
    return html.unescape(re.sub(r"<[^>]+>", "", besedilo)).strip()


def v_stevilo(niz, tip):
    """Pretvori besedilo v število; prazna celica pomeni manjkajoč podatek."""
    return tip(niz) if niz else None


def visina_v_cm(niz):
    """Pretvori višino iz oblike '6-8' (čevlji-palci) v centimetre."""
    if not niz:
        return None
    cevlji, palci = niz.split("-")
    return round((int(cevlji) * 12 + int(palci)) * 2.54)


def datum_v_iso(niz):
    """Pretvori datum iz oblike 'November 7, 1999' v '1999-11-07'."""
    if not niz:
        return None
    return datetime.datetime.strptime(niz, "%B %d, %Y").date().isoformat()


def celice_igralca(besedilo):
    """Vrne slovar {ime polja: besedilo celice} za eno vrstico igralca."""
    celice = {}
    for celica in VZOREC_TD.finditer(besedilo):
        polje = re.search(r'data-stat="(\w+)"', celica["atributi"])
        if polje:
            celice[polje.group(1)] = pocisti(celica["vsebina"])
    return celice


# --- Izluščenje podatkov -----------------------------------------------


def ekipe_v_sezoni(leto):
    """Iz strani sezone izlušči ekipe in njihovo statistiko v tej sezoni."""
    vsebina = preberi_stran(os.path.join(MAPA_HTML, "sezone", f"{leto}.html"))
    ekipe = {}  # ključ je kratica, tako se ekipa ne podvoji

    for najdba in VZOREC_EKIPE.finditer(vsebina):
        celice = {
            c["polje"]: c["vrednost"]
            for c in VZOREC_CELICE_EKIPE.finditer(najdba["celice"])
        }
        ekipe[najdba["kratica"]] = {
            "kratica": najdba["kratica"],
            "ime": najdba["ime"],
            "leto": int(najdba["leto"]),
            "play_off": najdba["zvezdica"] == "*",  # * = uvrstitev v končnico
            "zmage": int(celice["wins"]),
            "porazi": int(celice["losses"]),
            "tocke_na_tekmo": float(celice["pts_per_g"]),
            "prejete_tocke_na_tekmo": float(celice["opp_pts_per_g"]),
            "srs": float(celice["srs"]),
        }

    return list(ekipe.values())


def igralci_v_ekipi(kratica, leto):
    """Iz strani ekipe izlušči igralce, ki so v tej sezoni igrali zanjo."""
    pot = os.path.join(MAPA_HTML, "ekipe", f"{kratica}_{leto}.html")
    vsebina = preberi_stran(pot)
    igralci = {}  # ključ je ID igralca

    for najdba in VZOREC_IGRALCA.finditer(vsebina):
        celice = celice_igralca(najdba["celice"])

        # Oznaka "R" pri izkušnjah pomeni novinca (rookie), torej 0 let.
        izkusnje = celice.get("years_experience")
        if izkusnje == "R":
            izkusnje = "0"

        # Celica z državo vsebuje zastavo in oznako (npr. "ca CA"),
        # zato vzamemo zadnjo besedo.
        drzava = celice.get("flag", "").split()

        igralci[najdba["id"]] = {
            "id": najdba["id"],
            "ime": html.unescape(najdba["ime"]),
            "kratica": kratica,
            "leto": leto,
            "stevilka": najdba["stevilka"] or None,
            "pozicija": celice.get("pos"),
            "visina_cm": visina_v_cm(celice.get("height")),
            "teza_lb": v_stevilo(celice.get("weight"), int),
            "datum_rojstva": datum_v_iso(celice.get("birth_date")),
            "drzava": drzava[-1] if drzava else None,
            "izkusnje": v_stevilo(izkusnje, int),
            "fakulteta": celice.get("college") or None,
        }

    return list(igralci.values())


def izlusci_tabelo(kratica, leto, tabela, polja):
    """Iz strani ekipe izlušči tabelo z danim ID-jem (npr. 'per_game_stats').

    Polja določajo, katere stolpce vzamemo in kako jih poimenujemo.
    """
    pot = os.path.join(MAPA_HTML, "ekipe", f"{kratica}_{leto}.html")
    vsebina = preberi_stran(pot)
    del_tabele = re.search(
        rf'<table[^>]*id="{tabela}".*?</table>', vsebina, re.DOTALL
    )
    if not del_tabele:
        return []

    zapisi = []
    for najdba in VZOREC_STATISTIKE.finditer(del_tabele.group(0)):
        celice = celice_igralca(najdba["celice"])
        zapis = {"id_igralca": najdba["id"], "kratica": kratica, "leto": leto}
        for polje, (ime, tip) in polja.items():
            zapis[ime] = v_stevilo(celice.get(polje), tip)
        zapisi.append(zapis)

    return zapisi


def statistika_igralcev(kratica, leto, tabela="per_game_stats"):
    """Izlušči statistiko igralcev na tekmo.

    'per_game_stats' je redni del sezone, 'per_game_stats_post' končnica.
    """
    return izlusci_tabelo(kratica, leto, tabela, POLJA_STATISTIKE)