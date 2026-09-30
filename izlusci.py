import html
import os
import re

MAPA_HTML = "html"

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
VZOREC_TD = re.compile(r"<td(?P<atributi>[^>]*)>(?P<vsebina>.*?)</td>", re.DOTALL)


def preberi_stran(pot):
    with open(pot, encoding="utf-8") as dat:
        return dat.read()


def pocisti(besedilo):
    """Odstrani HTML značke, pretvori posebne znake in odvečne presledke."""
    return html.unescape(re.sub(r"<[^>]+>", "", besedilo)).strip()


def visina_v_cm(niz):
    """Pretvori višino iz oblike '6-8' (čevlji-palci) v centimetre."""
    if not niz:
        return None
    cevlji, palci = niz.split("-")
    return round((int(cevlji) * 12 + int(palci)) * 2.54)


def celice_igralca(besedilo):
    """Vrne slovar {ime polja: besedilo celice} za eno vrstico igralca."""
    celice = {}
    for celica in VZOREC_TD.finditer(besedilo):
        polje = re.search(r'data-stat="(\w+)"', celica["atributi"])
        if polje:
            celice[polje.group(1)] = pocisti(celica["vsebina"])
    return celice


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
            "play_off": najdba["zvezdica"] == "*",
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
        teza = celice.get("weight")
        izkusnje = celice.get("years_experience")
        drzava = celice.get("flag", "").split()
        igralci[najdba["id"]] = {
            "id": najdba["id"],
            "ime": html.unescape(najdba["ime"]),
            "kratica": kratica,
            "leto": leto,
            "stevilka": najdba["stevilka"] or None,
            "pozicija": celice.get("pos"),
            "visina_cm": visina_v_cm(celice.get("height")),
            "teza_lb": int(teza) if teza else None,
            "datum_rojstva": celice.get("birth_date"),
            "drzava": drzava[-1] if drzava else None,
            "izkusnje": 0 if izkusnje == "R" else (int(izkusnje) if izkusnje else None),
            "fakulteta": celice.get("college") or None,
        }

    return list(igralci.values())


if __name__ == "__main__":
    print(len(ekipe_v_sezoni(2026)))
    igralci = igralci_v_ekipi("BOS", 2026)
    print(len(igralci))
    print([igralec["ime"] for igralec in igralci])
    print(igralci[0])