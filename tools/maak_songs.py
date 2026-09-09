#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maak_songs.py — bouwt ../songs.js uit Vibely.xlsx (+ leden.json).

Gebruik (in de map tools/):
    pip install openpyxl        (eenmalig)
    python maak_songs.py

Verwachte kolommen in het Excel-blad (eerste rij = koppen):
    Land | Jaar | Artiest | Lied | YouTube-link | Bron | MP3-bestandsnaam

Groepsleden komen uit leden.json (jaar + artiest moeten exact overeenkomen met het Excel-blad).
Voor duo's/trio's waarvan de namen in de artiestennaam staan ("Tessa & Marloes",
"Lisa, Amy & Shelley", "Jess 'n Emmy") worden de leden automatisch afgeleid.
"""
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl ontbreekt. Installeer met:  pip install openpyxl")

HIER = Path(__file__).resolve().parent
EXCEL = HIER / "Vibely.xlsx"
LEDEN = HIER / "leden.json"
UITVOER = HIER.parent / "songs.js"


def nfc(s):
    return unicodedata.normalize("NFC", str(s or "")).strip()


def sleutel(jaar, artiest):
    return (int(jaar), nfc(artiest).casefold())


def leden_uit_naam(artiest):
    """'Tessa & Marloes' -> [['Tessa',''],['Marloes','']]; 'Cheyenne Boermans & Mayleen Schoenmaker' -> volledige namen."""
    if " & " not in artiest and ", " not in artiest and " 'n " not in artiest:
        return []
    delen = re.split(r"\s*(?:,|&|\s'n\s)\s*", artiest)
    delen = [d.strip() for d in delen if d.strip()]
    if len(delen) < 2:
        return []
    leden = []
    for d in delen:
        roepnaam = d.split()[0]
        volledig = d if " " in d else ""
        leden.append([roepnaam, volledig])
    return leden


def main():
    if not EXCEL.exists():
        sys.exit(f"Excel-bestand niet gevonden: {EXCEL}")
    wb = openpyxl.load_workbook(EXCEL, data_only=True)
    ws = wb.worksheets[0]
    rijen = list(ws.iter_rows(values_only=True))
    koppen = [nfc(k).casefold() for k in rijen[0]]

    def kol(*namen):
        for n in namen:
            if n in koppen:
                return koppen.index(n)
        sys.exit(f"Kolom niet gevonden: {namen}. Gevonden koppen: {koppen}")

    k_land, k_jaar, k_art, k_titel = kol("land"), kol("jaar"), kol("artiest"), kol("lied", "titel")
    k_yt, k_bron, k_mp3 = kol("youtube-link", "youtube"), kol("bron"), kol("mp3-bestandsnaam", "mp3")

    leden_db = {}
    if LEDEN.exists():
        data = json.loads(LEDEN.read_text(encoding="utf-8"))
        for act in data.get("acts", []):
            leden_db[sleutel(act["jaar"], act["artiest"])] = act

    songs = []
    gebruikt = set()
    for rij in rijen[1:]:
        if not rij or not rij[k_art] or not rij[k_jaar]:
            continue
        artiest = nfc(rij[k_art])
        jaar = int(str(rij[k_jaar]).strip()[:4])
        titel = nfc(rij[k_titel])
        mp3 = nfc(rij[k_mp3]) or f"{jaar} - {artiest} - {titel}.mp3"
        act = leden_db.get(sleutel(jaar, artiest))
        if act:
            gebruikt.add(sleutel(jaar, artiest))
            leden = [[nfc(l[0]), nfc(l[1]) if len(l) > 1 else ""] for l in act.get("leden", [])]
            soort = act.get("soort") or ("groep" if leden else "solo")
            naam = nfc(act.get("volledig", ""))
        else:
            leden = leden_uit_naam(artiest)
            soort = "solo" if not leden else ("duo" if len(leden) == 2 else "groep")
            naam = ""
        song = {
            "id": len(songs) + 1,
            "land": nfc(rij[k_land]),
            "jaar": jaar,
            "artiest": artiest,
            "titel": titel,
            "mp3": mp3,
            "youtube": nfc(rij[k_yt]),
            "bron": nfc(rij[k_bron]),
            "soort": soort,
            "leden": leden,
        }
        if naam:
            song["naam"] = naam
        songs.append(song)

    niet_gebruikt = [k for k in leden_db if k not in gebruikt]
    if niet_gebruikt:
        print("Let op: deze acts uit leden.json staan niet (zo) in het Excel-blad:")
        for k in niet_gebruikt:
            print("   ", k[0], leden_db[k]["artiest"])

    regels = [json.dumps(s, ensure_ascii=False) for s in songs]
    tekst = (
        f"// songs.js — automatisch gegenereerd door tools/maak_songs.py op {date.today().isoformat()} "
        f"uit tools/Vibely.xlsx ({len(songs)} nummers).\n"
        "// Velden: id, land, jaar, artiest, titel, mp3 (bestandsnaam in de map audio/), youtube, bron,\n"
        "//         soort (solo/duo/groep), naam (volledige naam solo-artiest, optioneel), leden ([roepnaam, volledige naam]).\n"
        "// Je mag dit bestand ook met de hand aanpassen; hou dan één nummer per regel.\n"
        "window.VIBELY_SONGS = [\n" + ",\n".join(regels) + "\n];\n"
    )
    UITVOER.write_text(tekst, encoding="utf-8")

    met_leden = sum(1 for s in songs if s["leden"])
    print(f"{len(songs)} nummers weggeschreven naar {UITVOER}")
    print(f"   waarvan {met_leden} met groepsleden (vraagtype 'groepslid').")


if __name__ == "__main__":
    main()
