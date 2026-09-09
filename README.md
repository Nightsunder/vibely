# Vibely – Your world, your vibes.

Muziekquiz over de Belgische (Junior Eurosong) en Nederlandse (Junior Songfestival) voorrondes
van het Junior Eurovisiesongfestival, 2003–2026. Werkt als web-app op je iPhone – zonder pc,
zodra de bestanden op GitHub Pages staan.

## Wat zit erin

| Bestand / map        | Wat het doet |
|----------------------|--------------|
| `index.html`         | De volledige app (HTML + CSS + JavaScript in één bestand, alles in het Nederlands). |
| `songs.js`           | De nummerlijst: jaar, artiest, titel, land, YouTube-link, bron, mp3-bestandsnaam en groepsleden. |
| `audio/`             | **Hier zet je je mp3's.** (Zie hieronder.) |
| `logo.png`, `icons/` | Logo en app-icoontjes (beginscherm iPhone). |
| `manifest.json`      | Zorgt dat de app als “echte” app op je beginscherm kan. |
| `.nojekyll`          | Zorgt dat GitHub Pages alle bestanden ongewijzigd publiceert. |
| `tools/`             | Je Excel-blad, de ledenlijst (`leden.json`) en `maak_songs.py` om `songs.js` opnieuw te maken. |

## Stap 1 – mp3's op de juiste plek

Zet al je mp3-bestanden in de map **`audio/`**. De bestandsnaam moet exact overeenkomen met de kolom
**MP3-bestandsnaam** in `tools/Vibely.xlsx` (dat is ook het veld `mp3` in `songs.js`), bijvoorbeeld

```
audio/2003 - Laura - Wees zeker.mp3
audio/2017 - Fource - Love Me.mp3
audio/2006 - The Fireflies - Waarom -.mp3
```

Hoofdletters, spaties en leestekens tellen mee. Nummers waarvan het bestand nog ontbreekt worden
automatisch overgeslagen; onder **Instellingen › Nummers** zie je in de app welke bestanden ontbreken.
Voeg je later mp3's toe, dan pikt de app die vanzelf op (of tik op “Nummers opnieuw controleren”).

Tip voor de bestandsgrootte: GitHub raadt aan een repository onder 1 GB te houden en GitHub Pages
publiceert sites tot ongeveer 1 GB. Zijn je mp3's groot, verklein ze dan eerst met ffmpeg
(kwaliteit blijft prima voor een quiz):

```
# Windows PowerShell (in de map met de originele mp3's; uitvoer in de map "klein")
mkdir klein
Get-ChildItem *.mp3 | ForEach-Object { ffmpeg -i "$($_.Name)" -b:a 96k "klein\$($_.Name)" }
```

## Stap 2 – naar GitHub

Zet de inhoud van deze map (inclusief `audio/`) in je repository `Nightsunder/vibely`.
Het makkelijkst op een pc is **GitHub Desktop**:

1. GitHub Desktop → *File › Clone repository* → kies `Nightsunder/vibely`.
2. Kopieer alle bestanden uit deze map naar de gekloonde map.
3. Zet je mp3's in de map `audio/`.
4. In GitHub Desktop: typ een korte omschrijving, klik **Commit to main** en daarna **Push origin**.
   (Bij honderden mp3's kan het uploaden even duren.)

## Stap 3 – GitHub Pages aanzetten (eenmalig)

1. Ga op github.com naar je repository → **Settings** → **Pages**.
2. Bij *Build and deployment* → *Source*: kies **Deploy from a branch**.
3. Branch: **main**, map: **/ (root)** → **Save**.
4. Na een minuut of twee staat de app op **https://nightsunder.github.io/vibely/**

Elke keer dat je iets pusht, wordt de site automatisch bijgewerkt.

## Stap 4 – op je iPhone

1. Open **https://nightsunder.github.io/vibely/** in Safari.
2. Tik op het deel-icoon (vierkant met pijl omhoog) → **Zet op beginscherm** → **Voeg toe**.
3. Vibely staat nu als app met logo op je beginscherm en opent schermvullend.

Je scores en instellingen worden op de telefoon zelf bewaard (het scorebord bewaart datum, naam en score
van elke gestopte ronde).

## Zo werkt de quiz

* Bij elke vraag speelt automatisch het begin van een willekeurig nummer (standaard 3 seconden).
  Daarna kun je kiezen: **Nog 3 s** (verder), **Willekeurig 3 s** (ergens midden in het nummer) of **Volledig**.
* Het vraagtype is willekeurig: **jaartal**, **artiest**, **titel** of **groepslid** (alleen bij groepen en duo's).
* **Tip** kost je 1 punt: je krijgt dan nog 1 punt in plaats van 2 bij een juist antwoord.
  Bij het jaartal krijg je een periode van zes jaar, bij meerkeuze verdwijnen twee foute antwoorden,
  bij typen krijg je de artiest / de eerste letter / de groepsnaam.
* **Stop** bewaart je score met datum op het scorebord.
* **Instellingen**: lengte van de fragmenten, marge op het jaartal, meerkeuze of typen, welke vraagtypes
  en welke landen meedoen, automatisch afspelen aan/uit.

## Nummers toevoegen of aanpassen

1. Vul `tools/Vibely.xlsx` aan (zelfde kolommen).
2. Groepsleden staan in `tools/leden.json` (jaar + artiest moeten overeenkomen met het Excel-blad).
   Duo's en trio's waarvan de namen al in de artiestennaam staan (bv. *Tessa & Marloes*) hoef je niet
   toe te voegen; die worden automatisch afgeleid.
3. Maak `songs.js` opnieuw:

   ```
   cd tools
   pip install openpyxl      (eenmalig)
   python maak_songs.py
   ```

4. Commit en push. Je mag `songs.js` ook rechtstreeks in een teksteditor aanpassen (één nummer per regel).

Bij drie acts konden de leden niet gevonden worden (Swing 2007, Las Niñas 2009, Tune 2009) en bij
Mystery of Darkness (2008) komen de namen alleen uit de songtekst; vul die gerust aan in `leden.json`.

## Lokaal testen op de pc (optioneel)

Open `index.html` niet rechtstreeks (dubbelklik), maar via een kleine webserver, anders kan de browser
niet in de mp3's “springen” voor het willekeurige fragment:

```
pip install rangehttpserver      (eenmalig)
python -m RangeHTTPServer 8000
```

Ga dan naar http://localhost:8000/ in je browser.
