#!/usr/bin/env python3
"""
⚔️  Mia's Linux-Abenteuer ⚔️
RPG-Lernspiel für die Linux-Kommandozeile
Steuere Mia durch eine Fantasiewelt und lerne dabei echte Linux-Befehle!
"""

import os, sys, subprocess, time, json, textwrap, configparser
from pathlib import Path

# ── VPS-Konfiguration (optional, aus ~/.mia_vps.ini) ──────────────────────────
try:
    import paramiko as _paramiko
    PARAMIKO_OK = True
except ImportError:
    print("📦  Installiere paramiko (wird nur einmal benoetigt) ...")
    def _install_paramiko():
        # 1) apt (Debian/Ubuntu, kein pip noetig)
        if subprocess.run(["which", "apt-get"], capture_output=True).returncode == 0:
            r = subprocess.run(
                ["sudo", "apt-get", "install", "-y", "-q", "python3-paramiko"],
                capture_output=True
            )
            if r.returncode == 0:
                return
        # 2) pip --user
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "paramiko", "-q", "--user"],
            capture_output=True
        )
        if r.returncode == 0:
            return
        # 3) pip mit ensurepip (falls pip selbst fehlt)
        subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"],
                       capture_output=True)
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "paramiko", "-q", "--user"],
            capture_output=True
        )
        if r.returncode == 0:
            return
        # 4) letzter Ausweg: --break-system-packages
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "paramiko", "-q",
             "--break-system-packages"],
            check=True
        )
    _install_paramiko()
    import paramiko as _paramiko
    PARAMIKO_OK = True

VPS_CONFIG: dict = {}
_vps_cfg = Path.home() / ".mia_vps.ini"
if _vps_cfg.exists():
    _c = configparser.ConfigParser()
    _c.read(_vps_cfg)
    if "vps" in _c:
        VPS_CONFIG = dict(_c["vps"])

# ── Terminal-Breite ────────────────────────────────────────────────────────────
try:
    W = min(os.get_terminal_size().columns, 86)
except OSError:
    W = 80
W = max(W, 76)

# ── Farben ─────────────────────────────────────────────────────────────────────
class F:
    PINK  = '\033[95m'; BLAU  = '\033[94m'; GRUEN = '\033[92m'
    GELB  = '\033[93m'; ROT   = '\033[91m'; CYAN  = '\033[96m'
    WEISS = '\033[97m'; GRAU  = '\033[90m'; BRAUN = '\033[33m'
    FETT  = '\033[1m';  RESET = '\033[0m'

def c(t, *fs): return ''.join(fs) + str(t) + F.RESET
def clr():     os.system('clear' if os.name != 'nt' else 'cls')

def vis_len(s):
    import re
    return len(re.sub(r'\033\[[0-9;]*m', '', s))

def langsam(text, farbe=F.WEISS, delay=0.025, indent=2):
    print(' ' * indent, end='')
    for ch in text:
        print(f"{farbe}{ch}{F.RESET}", end='', flush=True)
        time.sleep(delay)
    print()

# ── ASCII-Kunst pro Raum ───────────────────────────────────────────────────────
KUNST = {
    "dorf": [
        c("  🏠        🏠        🏠  ", F.GELB),
        c(" /##\\     /##\\     /##\\ ", F.BRAUN),
        c("|######| |######| |######|", F.BRAUN),
        c("  ||         ||        ||  ", F.BRAUN),
        c("══════════════════════════ ", F.GRAU),
        c("        Dorfplatz          ", F.GELB + F.FETT),
    ],
    "wald": [
        c(" 🌲    🌲    🌲    🌲    🌲", F.GRUEN),
        c(" /|\\   /|\\   /|\\   /|\\  ", F.GRUEN),
        c("  |     |     |     |      ", F.BRAUN),
        c("~~~~~~~~~~~~~~~~~~~~~~~~~~~ ", F.CYAN),
        c("      Mystischer Wald       ", F.GRUEN + F.FETT),
    ],
    "hoehle": [
        c("   _________________________ ", F.GRAU),
        c("  / ◆   ◆   ◆   ◆   ◆   \\ ", F.CYAN),
        c(" |   ◆   ◆   ◆   ◆   ◆   | ", F.CYAN),
        c(" |  ◆   ◆   ◆   ◆   ◆    | ", F.CYAN),
        c("  \\_______________________/ ", F.GRAU),
        c("        Dunkle Höhle         ", F.GRAU + F.FETT),
    ],
    "see": [
        c("   🦢                       ", F.WEISS),
        c(" ~~~~~ ~~~~ ~~~~ ~~~~~ ~~~ ", F.BLAU),
        c(" ~~~~ ~~~🐟~~~~~ ~~~~ ~~~~~ ", F.BLAU),
        c(" ~~~~~ ~~~~ ~~~~ ~~~~~ ~~~ ", F.BLAU),
        c("                            ", ''),
        c("        Stiller See         ", F.BLAU + F.FETT),
    ],
    "burg": [
        c("  |▓|              |▓|      ", F.GRAU),
        c("  |▓|              |▓|      ", F.GRAU),
        c(" _|▓|______________|▓|_     ", F.GRAU),
        c("|   🚪   |         |    |   ", F.BRAUN),
        c("|________|_________|____|   ", F.GRAU),
        c("         Alte Burg          ", F.GRAU + F.FETT),
    ],
    "markt": [
        c("  ⛺         ⛺         ⛺  ", F.GELB),
        c(" /  \\       /  \\       /  \\ ", F.GELB),
        c("|    |     |    |     |    | ", F.BRAUN),
        c("════════════════════════════ ", F.GRAU),
        c("  🍎  🧄  🪄   🍞  🔑      ", ''),
        c("         Marktplatz          ", F.GELB + F.FETT),
    ],
    "bibliothek": [
        c("  +=========================+", F.BRAUN),
        c(" |   |BUCH| |BUCH| |BUCH|  |", F.BRAUN),
        c(" |   |----| |----| |----|  |", F.BRAUN),
        c(" |   |BUCH| |BUCH| |BUCH|  |", F.BRAUN),
        c(" |   =====================  |", F.BRAUN),
        c("  Bibliothek des Wissens     ", F.BRAUN + F.FETT),
    ],
    "labor": [
        c("  +=========================+", F.CYAN),
        c(" |    (O)    (O)    (O)    |", F.CYAN),
        c(" |     |      |      |     |", F.CYAN),
        c(" |   [~~~]  [~~~]  [~~~]   |", F.CYAN),
        c(" |    ~~ LABOR VON ADA ~~  |", F.CYAN),
        c("       Geheimes Labor        ", F.CYAN + F.FETT),
    ],
    "festung": [
        c(" [|][|][|]  FESTUNG  [|][|][|]", F.GRAU),
        c(" +------------------------------+", F.GRAU),
        c(" |      +----------------+      |", F.GRAU),
        c(" |      |   [= TOR =]    |      |", F.GRAU),
        c(" |      +----------------+      |", F.GRAU),
        c("      Festung der Waechter      ", F.GRAU + F.FETT),
    ],
    "bergpass": [
        c("      (^)         (^)    ", F.BLAU),
        c("     (^ ^)       (^ ^)   ", F.BLAU),
        c("    (^ ## ^)   (^ ## ^)  ", F.BLAU),
        c("   +----BERGPASS------+  ", F.BLAU),
        c("   |  DER  HAENDLER   |  ", F.BLAU),
        c("   Bergpass der Haendler  ", F.BLAU + F.FETT),
    ],
    "hafen": [
        c("  ~  ~  HAFEN DER VERBINDUNGEN  ~  ~", F.BLAU),
        c(" __|__         __|__         __|__  ", F.BLAU),
        c(" |   |~~~~~~~~~|   |~~~~~~~~~|   | ", F.BLAU),
        c("~|___|~~~~~~~~~|___|~~~~~~~~~|___|~", F.BLAU),
        c("~~~~~~~~~~ ANKER GEWORFEN ~~~~~~~~~~", F.BLAU),
        c("      Hafen der Verbindungen        ", F.BLAU + F.FETT),
    ],
    "turm": [
        c("              /\\              ", F.PINK),
        c("             /  \\             ", F.PINK),
        c("            | [] |            ", F.PINK),
        c("            | [] |            ", F.PINK),
        c("            |    |            ", F.PINK),
        c("       Turm der Schreibkunst  ", F.PINK + F.FETT),
    ],
    "drachenfestung": [
        c("   __   *DRACHEN-FESTUNG*   __  ", F.ROT),
        c("  /  \\       REMIRF        /  \\ ", F.ROT),
        c(" | oo |      /\\  /\\       | oo |", F.ROT),
        c(" |    |     /  \\/  \\      |    |", F.ROT),
        c("  \\__/  ~~~~~~~~~~~~~~~   \\__/ ", F.ROT),
        c("   *** ENDKAMPF BEGINNT! ****  ", F.ROT + F.FETT),
    ],
    "schmiede": [
        c("    *   F E U E R   *   ", F.BRAUN),
        c("   /|\\   Esse    /|\\  ", F.BRAUN),
        c("  [===== Amboss =====]  ", F.BRAUN),
        c("  |~~~~  Glut  ~~~~~|  ", F.ROT),
        c("  |___  SCHMIEDE  ___|  ", F.BRAUN + F.FETT),
    ],
    "sternwarte": [
        c("   *  .  * Sterne *  .  *  ", F.BLAU),
        c("    .   *   .   *   .   *  ", F.BLAU),
        c("   |    ( Teleskop  )   |  ", F.BLAU),
        c("   |___/   Sockel   \\__|  ", F.GRAU),
        c("   [====  STERNWARTE ====] ", F.BLAU + F.FETT),
    ],
    "akademie": [
        c("  | |  AKADEMIE  | |   ", F.GELB),
        c("  |=|  _________  |=| ", F.GELB),
        c("  | | | Variablen| | | ", F.GELB),
        c("  | | |__________| | | ", F.GELB),
        c("  | |  Saeulenhalle | | ", F.GELB),
        c("  |__|______________|__| ", F.GELB + F.FETT),
    ],
    "taverne": [
        c("  [======= TAVERNE =======]  ", F.BRAUN),
        c("  | Fass |  Theke  | Fass |  ", F.BRAUN),
        c("  | [=]  | [=] [=] |  [=] |  ", F.BRAUN),
        c("  |    * Kerzenschein *    |  ", F.GELB),
        c("  |______warm und gut______|  ", F.BRAUN + F.FETT),
    ],
    "magierschule": [
        c("  ✨  *   MAGIERSCHULE   *  ✨  ", F.PINK),
        c("  🪄      der Skripte      🪄  ", F.PINK),
        c("  |   *   Bash-Zauber   *   |  ", F.PINK),
        c("  |   Skripte entstehen!    |  ", F.PINK),
        c("   \\________________________/  ", F.PINK),
        c("    ✨   bash  scripts   ✨    ", F.PINK + F.FETT),
    ],
    "palast": [
        c("        👑  PALAST  👑        ", F.WEISS),
        c("       / der Benutzer \\      ", F.GRAU),
        c("      | 🏛️  |  🏛️  |  🏛️ |   ", F.GRAU),
        c("      |   ==  THRON  ==  |   ", F.WEISS),
        c("       \\_________________/   ", F.GRAU),
        c("         *  Willkommen  *    ", F.GRAU + F.WEISS),
    ],
    "bibliothekskeller": [
        c("  ~~~~ KELLER der TEXTE ~~~~  ", F.CYAN),
        c("  | 📜   Runen und Magie   |  ", F.CYAN),
        c("  | ░░ sort | uniq | awk ░░|  ", F.CYAN),
        c("  | ░░  sed  |  tr | cut ░░|  ", F.CYAN),
        c("  |_________________________|  ", F.CYAN),
        c("   ~~ Awk beobachtet dich ~~  ", F.CYAN + F.FETT),
    ],
    "garten": [
        c("    🌸      GARTEN      🌸    ", F.GRUEN),
        c("  🌺 . 🌿 . 🌼 . 🌿 . 🌼 . 🌺  ", F.GRUEN),
        c("  | 🌳   Verknuepfungen  🌳 |  ", F.GRUEN),
        c("  |    find  .  ln  .  du  |  ", F.GRUEN),
        c("   \\_______________________/  ", F.GRUEN),
        c("    🌸    Willkommen!    🌸   ", F.GRUEN + F.FETT),
    ],
    "schluesselschmiede": [
        c("  🔑  🔑  🔑  🔑  🔑  🔑  ", F.GELB),
        c("  ┌─────────────────────┐  ", F.BRAUN),
        c("  │ ssh-keygen ed25519  │  ", F.GRUEN + F.FETT),
        c("  │ ~/.ssh/id_ed25519   │  ", F.GRUEN),
        c("  └─────────────────────┘  ", F.BRAUN),
        c("  🔑  Schlüsselschmiede  🔑 ", F.GELB + F.FETT),
    ],
    "zeituhr": [
        c("       ⏰  12  ⏰       ", F.GELB),
        c("    ┌──────────────┐    ", F.GRAU),
        c("    │  * * * * *   │    ", F.CYAN + F.FETT),
        c("    │  cron jobs   │    ", F.CYAN),
        c("    └──────────────┘    ", F.GRAU),
        c("   ⏰  Zeituhr der Zeit  ", F.GELB + F.FETT),
    ],
    "webwerkstatt": [
        c("  <html>              </html>  ", F.GRUEN),
        c("    <head> 🌐 </head>         ", F.GELB),
        c("    <body>                    ", F.CYAN),
        c("      <h1>Web-Werkstatt</h1>  ", F.WEISS + F.FETT),
        c("    </body>                   ", F.CYAN),
        c("  💻  HTML auf dem Server!   ", F.GRUEN + F.FETT),
    ],
    "deploymeisterei": [
        c("  📝 edit  →  📤 scp  →  🌍  ", F.GELB),
        c("  ╔════════════════════════╗  ", F.GRUEN),
        c("  ║  ./deploy.sh  🚀       ║  ", F.GRUEN + F.FETT),
        c("  ║  v1 → v2 → v3 → live  ║  ", F.CYAN),
        c("  ╚════════════════════════╝  ", F.GRUEN),
        c("  🚀   Deploymeisterei    🚀  ", F.GELB + F.FETT),
    ],
    "fernwelt": [
        c("  ╔═══════════════════════╗  ", F.CYAN),
        c("  ║  >_ SSH PORTAL  🌐   ║  ", F.CYAN + F.FETT),
        c("  ║  ~~~~~~~~~~~~~~~~~~~~ ║  ", F.BLAU),
        c("  ║  152.53.225.236:22   ║  ", F.GRUEN),
        c("  ╚═══════════════════════╝  ", F.CYAN),
        c("  ⚡   Fernwelt-Portal   ⚡  ", F.CYAN + F.FETT),
    ],
}

# ── Raum-Definitionen ──────────────────────────────────────────────────────────
RAEUME = {
    "dorf": {
        "name":   "Dorfplatz",
        "emoji":  "🏠",
        "beschreibung": (
            "Du stehst auf dem zentralen Dorfplatz. Die Sonne scheint warm.\n"
            "Alter Stein Finn sitzt auf einer Bank und winkt dir zu."
        ),
        "ausgaenge":  {"wald": "Wald", "see": "See", "markt": "Markt"},
        "npc": {
            "name": "Ältester Finn",
            "bild": "👴",
            "dialoge": [
                "Willkommen, Abenteurerin! Das Böse hat unser Dorf verflucht.\n"
                "7 alte Schriftrollen müssen wir finden!\n"
                "Erste Aufgabe: Schau dich um! Tippe:  ls",
                "Gut gemacht! Kannst du auch sagen, wo du genau bist?\n"
                "Tippe:  pwd",
                "Ausgezeichnet! Du hast die ersten Schriftrollen!\n"
                "Reise in den Wald mit:  cd wald",
            ],
        },
        "quests": [
            {
                "id":       "ls_dorf",
                "ziel":     "Schau dich um mit: ls",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "ls",
                "belohnung":"📜 Schriftrolle des Sehens",
                "lernziel": "ls = list – zeigt alle Dateien und Ordner im aktuellen Verzeichnis",
            },
            {
                "id":       "pwd_dorf",
                "ziel":     "Zeige deinen genauen Standort: pwd",
                "check":    lambda cmd, out, p: cmd.strip() == "pwd",
                "belohnung":"📜 Schriftrolle des Wissens",
                "lernziel": "pwd = print working directory – dein aktueller Pfad im Dateisystem",
            },
            {
                "id":       "ls_la_dorf",
                "ziel":     "Zeige auch versteckte Dateien: ls -la",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='ls' and ('-la' in cmd or '-al' in cmd),
                "belohnung":"📜 Schriftrolle der Verborgenen",
                "lernziel": "ls -la zeigt alle Dateien inklusive versteckter (beginnen mit .). Sehr haeufig genutzt!",
            },
            {
                "id":       "ls_lh_dorf",
                "ziel":     "Zeige lesbare Dateigroessen: ls -lh",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='ls' and '-lh' in cmd,
                "belohnung":"📜 Schriftrolle der Groesse",
                "lernziel": "ls -lh zeigt Dateigroessen als 1K/5M/2G statt rohe Bytes. Viel lesbarer!",
            },
            {
                "id":       "ls_lt_dorf",
                "ziel":     "Sortiere Dateien nach Datum: ls -lt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='ls' and '-lt' in cmd,
                "belohnung":"📜 Schriftrolle der Zeit",
                "lernziel": "ls -lt sortiert nach Aenderungsdatum, neuste zuerst. ls -ltr = aelteste zuerst.",
            },
            {
                "id":       "lshelp_dorf",
                "ziel":     "Lies die Hilfe zu ls: ls --help",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='ls' and '--help' in cmd,
                "belohnung":"📜 Schriftrolle des Lesens",
                "lernziel": "--help gibt es bei fast jedem Befehl! Zeigt alle Optionen. Auch: man ls fuer mehr.",
            },
        ],
    },
    "wald": {
        "name":   "Mystischer Wald",
        "emoji":  "🌲",
        "beschreibung": (
            "Die Bäume ragen hoch empor. Eine elegante Waldelfin\n"
            "tritt aus dem Schatten und lächelt dich an."
        ),
        "ausgaenge": {"dorf": "Dorf", "hoehle": "Höhle"},
        "npc": {
            "name": "Waldelfin Lyra",
            "bild": "🧝",
            "dialoge": [
                "Psst! Ich bin Lyra. Es gibt eine geheime Höhle!\n"
                "Erst erkunde hier: ls\n"
                "Dann: cd hoehle",
                "Du hast den Wald erkundet!\n"
                "Geh tiefer: cd hoehle",
                "Du kennst nun alle Wege im Wald!\n"
                "Mit 'cd ..' kommst du immer wieder zurück.",
            ],
        },
        "quests": [
            {
                "id":       "ls_wald",
                "ziel":     "Erkunde den Wald: ls",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "ls",
                "belohnung":"📜 Schriftrolle des Waldes",
                "lernziel": "ls hat viele Optionen: ls -l (Details), ls -lh (Größe lesbar)",
            },
            {
                "id":       "mkdir_wald",
                "ziel":     "Erstelle einen neuen Ordner: mkdir waldlager",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='mkdir' and len(cmd.split())>=2,
                "belohnung":"📜 Schriftrolle der Erschaffung",
                "lernziel": "mkdir = make directory. mkdir -p pfad/zu/ordner erstellt verschachtelte Ordner.",
            },
            {
                "id":       "touch_wald",
                "ziel":     "Erstelle eine leere Datei: touch karte.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='touch' and len(cmd.split())>=2,
                "belohnung":"📜 Schriftrolle der Entstehung",
                "lernziel": "touch erstellt leere Dateien. Aktualisiert auch Zeitstempel bestehender Dateien.",
            },
            {
                "id":       "rm_wald",
                "ziel":     "Loesche die Datei: rm karte.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='rm' and len(cmd.split())>=2,
                "belohnung":"📜 Schriftrolle des Endes",
                "lernziel": "rm loescht Dateien ENDGUELTIG (kein Papierkorb!). rm -r loescht Ordner rekursiv.",
            },
            {
                "id":       "lsR_wald",
                "ziel":     "Zeige alle Unterordner rekursiv: ls -R",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='ls' and '-R' in cmd,
                "belohnung":"📜 Schriftrolle der Tiefe",
                "lernziel": "ls -R zeigt alle Dateien durch alle Unterordner. Gut fuer Ueberblick ueber Strukturen.",
            },
        ],
    },
    "hoehle": {
        "name":   "Dunkle Höhle",
        "emoji":  "⛏️",
        "beschreibung": (
            "Es ist dunkel und feucht hier. Edelsteine glänzen.\n"
            "Ein bärtiger Zwerg klopft mit einem Hammer und grinst."
        ),
        "ausgaenge": {"wald": "Wald"},
        "npc": {
            "name": "Zwerg Bruno",
            "bild": "🧔",
            "dialoge": [
                "Ha! Eine Besucherin! Ich baue hier ein Lager.\n"
                "Du auch? Erstelle einen Ordner: mkdir lager",
                "Gut gebaut! Jetzt eine Lagerdatei:\n"
                "touch proviant.txt",
                "Perfekt! Das Lager steht! Hier ist deine Belohnung!",
            ],
        },
        "quests": [
            {
                "id":    "mkdir_hoehle",
                "ziel":  "Baue ein Lager: mkdir lager",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "mkdir" and len(cmd.split()) > 1,
                "belohnung":"📜 Schriftrolle der Erschaffung",
                "lernziel": "mkdir = make directory – erstellt einen neuen Ordner",
            },
            {
                "id":    "touch_hoehle",
                "ziel":  "Lege Vorräte an: touch proviant.txt",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "touch" and len(cmd.split()) > 1,
                "belohnung":"📜 Schriftrolle der Berührung",
                "lernziel": "touch datei.txt – erstellt eine neue leere Datei",
            },
            {
                "id":       "cat_hoehle",
                "ziel":     "Lies die Datei: cat proviant.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='cat' and len(cmd.split())>=2,
                "belohnung":"📜 Schriftrolle des Lesens",
                "lernziel": "cat zeigt Dateiinhalt. cat -n zeigt Zeilennummern. cat datei1 datei2 verbindet Dateien.",
            },
            {
                "id":       "append_hoehle",
                "ziel":     "Haenge Text an: echo 'Wasser' >> proviant.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='echo' and '>>' in cmd,
                "belohnung":"📜 Schriftrolle des Anhaengens",
                "lernziel": ">> haengt an ohne zu loeschen. > ueberschreibt. Immer doppeltes >> zum Anhaengen!",
            },
            {
                "id":       "wc_hoehle",
                "ziel":     "Zaehle Zeilen: wc -l proviant.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='wc' and '-l' in cmd,
                "belohnung":"📜 Schriftrolle der Zahlen",
                "lernziel": "wc = word count. -l zaehlt Zeilen, -w Woerter, -c Zeichen. wc -l *.txt zaehlt alle.",
            },
            {
                "id":       "rmdir_hoehle",
                "ziel":     "Erstelle und loesche Ordner: mkdir test_temp && rmdir test_temp",
                "check":    lambda cmd, out, p: bool(cmd.split()) and 'rmdir' in cmd,
                "belohnung":"📜 Schriftrolle des Raeumens",
                "lernziel": "rmdir loescht NUR leere Ordner. rm -rf ordner/ loescht alles darin (Vorsicht!).",
            },
        ],
    },
    "see": {
        "name":   "Stiller See",
        "emoji":  "🌊",
        "beschreibung": (
            "Der See liegt ruhig da, sein Wasser glasklar.\n"
            "Eine Wassernixe taucht auf und lächelt geheimnisvoll."
        ),
        "ausgaenge": {"dorf": "Dorf"},
        "npc": {
            "name": "Nixe Marina",
            "bild": "🧜",
            "dialoge": [
                "Willkommen! Ich bewache eine Schriftrolle.\n"
                "Lies erst die Fels-Inschrift: cat fels.txt",
                "Jetzt schreibe deine eigene Nachricht:\n"
                'echo "Hallo Welt!" > nachricht.txt',
                "Wunderbar! Du hast meinen Test bestanden!\n"
                "Die Schriftrolle gehört dir!",
            ],
        },
        "quests": [
            {
                "id":    "cat_see",
                "ziel":  "Lies die Fels-Inschrift: cat fels.txt",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "cat" and len(cmd.split()) > 1,
                "belohnung":"📜 Schriftrolle des Lesens",
                "lernziel": "cat datei.txt – zeigt den Inhalt einer Datei an",
            },
            {
                "id":    "echo_see",
                "ziel":  'Schreibe eine Nachricht: echo "Text" > datei.txt',
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "echo" and ">" in cmd,
                "belohnung":"📜 Schriftrolle des Schreibens",
                "lernziel": 'echo "Text" > datei.txt – schreibt Text in eine Datei',
            },
            {
                "id":       "cat_see2",
                "ziel":     "Lies deine Nachricht: cat nachricht.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='cat' and 'nachricht' in cmd,
                "belohnung":"📜 Schriftrolle der Bestaetigung",
                "lernziel": "cat zeigt was du gerade geschrieben hast. Gut zum Pruefen nach echo > Datei.",
            },
            {
                "id":       "append_see",
                "ziel":     "Haenge Text an: echo 'Der See ist schoen' >> nachricht.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='echo' and '>>' in cmd,
                "belohnung":"📜 Schriftrolle des Wachstums",
                "lernziel": ">> haengt an ohne zu loeschen. Denk daran: double-arrow = append, single = overwrite!",
            },
            {
                "id":       "wc_see",
                "ziel":     "Zaehle Woerter: wc -w nachricht.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='wc' and '-w' in cmd,
                "belohnung":"📜 Schriftrolle der Worte",
                "lernziel": "wc -w zaehlt Woerter. wc ohne Optionen zeigt Zeilen/Woerter/Zeichen gleichzeitig.",
            },
            {
                "id":       "head_see",
                "ziel":     "Zeige erste Zeile: head -1 nachricht.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='head' and len(cmd.split())>=2,
                "belohnung":"📜 Schriftrolle des Anfangs",
                "lernziel": "head zeigt die ersten N Zeilen. Standard: head = 10 Zeilen. Ideal fuer grosse Dateien.",
            },
        ],
    },
    "markt": {
        "name":   "Marktplatz",
        "emoji":  "🏪",
        "beschreibung": (
            "Bunte Marktstände, Händler rufen ihre Waren.\n"
            "Eine Händlerin mit Zylinder winkt dich heran."
        ),
        "ausgaenge": {"dorf": "Dorf", "bibliothek": "Bibliothek", "garten": "Garten"},
        "npc": {
            "name": "Händlerin Zara",
            "bild": "🎩",
            "dialoge": [
                "Ich handele mit Waren – ich kann sie kopieren!\n"
                "Auf dem Markt liegt schon eine Datei.\n"
                "Probiere: cp preisliste.txt kopie.txt",
                "Perfekt! Und verschieben oder umbenennen:\n"
                "mv kopie.txt neues_exemplar.txt",
                "Meisterhaft! Du bist eine echte Händlerin!\n"
                "Nimm diese Schriftrolle als Dank!",
            ],
        },
        "quests": [
            {
                "id":    "cp_markt",
                "ziel":  "Kopiere eine Datei: cp preisliste.txt kopie.txt",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "cp" and len(cmd.split()) >= 3,
                "belohnung":"📜 Schriftrolle des Kopierens",
                "lernziel": "cp quelle.txt ziel.txt – kopiert eine Datei (das Original bleibt!)",
            },
            {
                "id":    "mv_markt",
                "ziel":  "Benenne um: mv kopie.txt neues_exemplar.txt",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "mv" and len(cmd.split()) >= 3,
                "belohnung":"📜 Schriftrolle der Bewegung",
                "lernziel": "mv alt.txt neu.txt – verschiebt oder benennt eine Datei um",
            },
            {
                "id":       "cat_markt",
                "ziel":     "Lies die Preisliste: cat preisliste.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='cat' and len(cmd.split())>=2,
                "belohnung":"📜 Schriftrolle des Lesens",
                "lernziel": "cat zum Lesen. Nach cp immer pruefen ob Kopie korrekt ist. Gute Gewohnheit!",
            },
            {
                "id":       "lsl_markt",
                "ziel":     "Zeige Dateidetails: ls -l",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='ls' and '-l' in cmd,
                "belohnung":"📜 Schriftrolle der Details",
                "lernziel": "ls -l zeigt Berechtigungen, Groesse, Datum. Sehr informativ fuer Dateidetails.",
            },
            {
                "id":       "rm_markt",
                "ziel":     "Loesche die Kopie: rm kopie.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='rm' and len(cmd.split())>=2,
                "belohnung":"📜 Schriftrolle der Ordnung",
                "lernziel": "rm loescht endgueltig. Tipp: rm -i fragt vor dem Loeschen (interaktiver Modus).",
            },
            {
                "id":       "find_markt",
                "ziel":     "Finde alle Textdateien: find . -name '*.txt'",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='find' and '.txt' in cmd,
                "belohnung":"📜 Schriftrolle des Suchens",
                "lernziel": "find . -name '*.txt' findet alle .txt Dateien. Wildcards: * = beliebig viele Zeichen.",
            },
        ],
    },
    "bibliothek": {
        "name":   "Bibliothek des Wissens",
        "emoji":  "📚",
        "beschreibung": (
            "Die uralte Bibliothek ist voller Staub und geheimnisvoller Buecher,\n"
            "die in langen Regalen bis zur Decke reichen. Ein goldener Kristallleuchter\n"
            "taucht tausend Schriften in warmes Licht."
        ),
        "ausgaenge": {"markt": "Markt", "labor": "Labor", "bibliothekskeller": "Buchkeller"},
        "npc": {
            "name": "Gelehrter Otto",
            "bild": "📖",
            "dialoge": [
                "Willkommen, junge Abenteurerin! Diese Bibliothek birgt unendliches Wissen,\n"
                "doch ein Fluch hat unsere Buecher durcheinandergebracht.\n"
                "Suche nach dem Wort 'Wissen' in unserer Sammlung: grep 'Wissen' buecher.txt",
                "Ausgezeichnet! Doch manche Buecher liegen noch versteckt und verloren.\n"
                "Finde alle Textdateien in diesem Verzeichnis: find . -name '*.txt'",
                "Wunderbar! Nun moechte ich wissen, wie viele Zeilen unsere Buechersammlung hat.\n"
                "Verbinde cat und wc mit einer Pipe: cat buecher.txt | wc -l",
                "Meisterhaft! Du hast alle Geheimnisse der Bibliothek entschluesselt.\n"
                "Die drei Schriftrollen gehoeren nun dir, tapfere Wissende!",
            ],
        },
        "quests": [
            {
                "id":    "grep_bib",
                "ziel":  "Suche in buecher.txt nach dem Begriff 'Wissen'. Nutze: grep 'Wissen' buecher.txt",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "grep" and len(cmd.split()) >= 3,
                "belohnung":"📜 Schriftrolle der Suche",
                "lernziel": "grep Muster datei.txt – durchsucht eine Datei nach Text. Unverzichtbar!",
            },
            {
                "id":    "find_bib",
                "ziel":  "Finde alle .txt-Dateien im aktuellen Verzeichnis. Nutze: find . -name '*.txt'",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "find",
                "belohnung":"📜 Schriftrolle des Findens",
                "lernziel": "find . -name '*.txt' – findet Dateien anhand des Namensmusters",
            },
            {
                "id":    "pipe_bib",
                "ziel":  "Zaehle die Zeilen in buecher.txt mit einer Pipe. Nutze: cat buecher.txt | wc -l",
                "check": lambda cmd, out, p: "|" in cmd and "wc" in cmd,
                "belohnung":"📜 Schriftrolle der Rohre",
                "lernziel": "| (Pipe) leitet Ausgabe weiter. wc -l zaehlt Zeilen. Befehle kombinieren!",
            },
        ],
    },

    "labor": {
        "name":   "Geheimes Labor",
        "emoji":  "⚗️",
        "beschreibung": (
            "Das verborgene Labor von Professorin Ada riecht nach Schwefel und Neugier.\n"
            "Ueberall blubbern Reagenzglaeser und summen seltsame Maschinen.\n"
            "Hier werden Geheimnisse der Dateiberechtigungen erforscht."
        ),
        "ausgaenge": {"bibliothek": "Bibliothek", "festung": "Festung", "palast": "Palast"},
        "npc": {
            "name": "Professorin Ada",
            "bild": "🔬",
            "dialoge": [
                "Ah, endlich eine Assistentin! Mein Labor schuetzt wichtige Experimente\n"
                "durch Berechtigungen – ohne sie waere das Chaos.\n"
                "Zeige mir zuerst alle Dateien mit ihren Zugriffsrechten: ls -l",
                "Sehr gut! 755 bedeutet: Eigentuemerrechte rwx, alle anderen r-x.\n"
                "Setze die Rechte: chmod 755 experiment.sh",
                "Perfekt! Ohne Ausfuehrungsrechte laeuft kein einziges Skript.\n"
                "Mache die Datei ausfuehrbar: chmod +x experiment.sh",
                "Brillant! Du hast Dateiberechtigungen vollstaendig gemeistert.\n"
                "Das Labor und seine Geheimnisse sind in sicheren Haenden!",
            ],
        },
        "quests": [
            {
                "id":    "lsl_labor",
                "ziel":  "Zeige alle Dateien mit ihren Berechtigungen an. Nutze: ls -l",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "ls" and "-l" in cmd,
                "belohnung":"📜 Schriftrolle der Rechte",
                "lernziel": "ls -l zeigt Berechtigungen: rwx = read/write/execute fuer owner, group, others",
            },
            {
                "id":    "chmod_labor",
                "ziel":  "Gib experiment.sh die Berechtigungen 755. Nutze: chmod 755 experiment.sh",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "chmod" and len(cmd.split()) >= 3,
                "belohnung":"📜 Schriftrolle der Macht",
                "lernziel": "chmod 755 = rwxr-xr-x. 7=rwx, 5=r-x, 4=r--. Zahlen = Berechtigungen!",
            },
            {
                "id":    "chmodx_labor",
                "ziel":  "Mache experiment.sh ausfuehrbar. Nutze: chmod +x experiment.sh",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "chmod" and "+x" in cmd,
                "belohnung":"📜 Schriftrolle der Ausfuehrung",
                "lernziel": "chmod +x macht eine Datei ausfuehrbar. Noetig fuer eigene Skripte!",
            },
            {
                "id":       "whoami_lab",
                "ziel":     "Wer bist du? whoami",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='whoami',
                "belohnung":"📜 Schriftrolle der Identitaet",
                "lernziel": "whoami zeigt deinen Benutzernamen. In Skripten oft genutzt um Root-Rechte zu pruefen.",
            },
            {
                "id":       "id_lab",
                "ziel":     "Zeige deine IDs: id",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='id',
                "belohnung":"📜 Schriftrolle der Gruppen",
                "lernziel": "id zeigt uid, gid und alle Gruppen. Wichtig bei Berechtigungsproblemen!",
            },
            {
                "id":       "chmod644_lab",
                "ziel":     "Nur-Lesen fuer andere: chmod 644 experiment.sh",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='chmod' and '644' in cmd,
                "belohnung":"📜 Schriftrolle der Grenzen",
                "lernziel": "chmod 644 = rw-r--r--. Owner lesen+schreiben, alle anderen nur lesen. Standard fuer Dateien.",
            },
            {
                "id":       "stat_lab",
                "ziel":     "Zeige Dateidetails: stat experiment.sh",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='stat' and len(cmd.split())>=2,
                "belohnung":"📜 Schriftrolle der Details",
                "lernziel": "stat zeigt alles: Groesse, Inode, Zugriffszeiten, Berechtigungen. Sehr detailliert.",
            },
        ],
    },
    "festung": {
        "name":   "Festung der Waechter",
        "emoji":  "🏰",
        "beschreibung": (
            "Die maechtigen Steinmauern der Festung ragen hoch in den stuermischen Himmel.\n"
            "Hunderte Waechter patrouillieren auf den Zinnen.\n"
            "General Klaus beobachtet mit wachsamem Blick jeden Prozess im System."
        ),
        "ausgaenge": {"labor": "Labor", "bergpass": "Bergpass", "schmiede": "Schmiede"},
        "npc": {
            "name": "General Klaus",
            "bild": "🛡️",
            "dialoge": [
                "Halt! Niemand betritt meine Festung ohne Pruefung.\n"
                "Beweise, dass du Prozesse verstehst!\n"
                "Zeige mir deine eigenen laufenden Prozesse: ps",
                "Gut! Aber ich brauche einen vollstaendigen Ueberblick ueber ALLE Waechter.\n"
                "Zeige alle Prozesse mit CPU- und RAM-Details: ps aux",
                "Beeindruckend! Starte nun einen Waechter, der 10 Sekunden im Hintergrund schlaeft.\n"
                "Fuehre aus: sleep 10 &",
                "Exzellent, Kommandant! Du hast die Kunst der Prozessverwaltung gemeistert.\n"
                "Die Festung steht unter deinem Kommando!",
            ],
        },
        "quests": [
            {
                "id":    "ps_festung",
                "ziel":  "Zeige deine laufenden Prozesse an. Nutze: ps",
                "check": lambda cmd, out, p: cmd.strip() == "ps",
                "belohnung":"📜 Schriftrolle der Waechter",
                "lernziel": "ps zeigt deine laufenden Prozesse. Jeder Prozess hat eine PID (Nummer).",
            },
            {
                "id":    "psaux_festung",
                "ziel":  "Zeige alle Prozesse mit Details an. Nutze: ps aux",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "ps" and "aux" in cmd,
                "belohnung":"📜 Schriftrolle aller Waechter",
                "lernziel": "ps aux zeigt ALLE Prozesse mit CPU/RAM-Nutzung. Sehr nuetzlich!",
            },
            {
                "id":    "bg_festung",
                "ziel":  "Starte einen Prozess im Hintergrund. Nutze: sleep 10 &",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "sleep" and "&" in cmd,
                "belohnung":"📜 Schriftrolle des Hintergrunds",
                "lernziel": "& am Ende startet einen Prozess im Hintergrund. Mit 'jobs' siehst du ihn.",
            },
            {
                "id":       "jobs_fest",
                "ziel":     "Zeige Hintergrundjobs: jobs",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='jobs',
                "belohnung":"📜 Schriftrolle der Arbeit",
                "lernziel": "jobs zeigt Hintergrundjobs. fg %1 bringt Job 1 in den Vordergrund. bg %1 in den Hintergrund.",
            },
            {
                "id":       "kill_fest",
                "ziel":     "Beende sleep-Job: kill %1",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='kill' and len(cmd.split())>=2,
                "belohnung":"📜 Schriftrolle des Endes",
                "lernziel": "kill %1 beendet Job 1. kill -9 PID = Sofortbeendigung. kill -15 PID = sanftes Beenden.",
            },
            {
                "id":       "uptime_fest",
                "ziel":     "Zeige Systemlaufzeit: uptime",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='uptime',
                "belohnung":"📜 Schriftrolle der Ausdauer",
                "lernziel": "uptime zeigt Laufzeit und Load Average (1/5/15-Min-Schnitt). >CPU-Kerne = ueberlastet.",
            },
            {
                "id":       "top_fest",
                "ziel":     "Zeige Prozessauslastung: top -bn1",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='top',
                "belohnung":"📜 Schriftrolle der Last",
                "lernziel": "top zeigt CPU/RAM-Auslastung live. -bn1 = batch/einmal. htop ist die modernere Alternative.",
            },
        ],
    },
    "bergpass": {
        "name":   "Bergpass der Haendler",
        "emoji":  "⛰️",
        "beschreibung": (
            "Auf dem beschwerlichen Bergpass zwischen schroffen Felsen und eisigem Wind\n"
            "treibt Haendler Gerhard seinen Handel mit begehrter Software.\n"
            "Wer die richtigen apt-Befehle kennt, findet hier alles!"
        ),
        "ausgaenge": {"festung": "Festung", "hafen": "Hafen", "sternwarte": "Sternwarte"},
        "npc": {
            "name": "Haendler Gerhard",
            "bild": "🏔️",
            "dialoge": [
                "Willkommen auf dem Bergpass, Reisende! Ich handle mit der wertvollsten Ware:\n"
                "Software-Pakete! Suche zunaechst nach einem Texteditor:\n"
                "apt-cache search texteditor",
                "Gut! Nun schau dir die Details zum beliebten Paket 'nano' genauer an.\n"
                "Nutze: apt-cache show nano",
                "Ausgezeichnet! Zum Schluss: Welche Software ist bereits auf deinem System?\n"
                "Pruefe mit: apt list --installed",
                "Fantastisch! Du bist nun ein wahres Talent im Software-Handel.\n"
                "Mein Bergpass steht dir jederzeit offen!",
            ],
        },
        "quests": [
            {
                "id":    "aptsearch_berg",
                "ziel":  "Suche nach einem Texteditor in den Paketquellen. Nutze: apt-cache search texteditor",
                "check": lambda cmd, out, p: ("apt-cache" in cmd and "search" in cmd) or (bool(cmd.split()) and cmd.split()[0] == "apt" and "search" in cmd),
                "belohnung":"📜 Schriftrolle der Software",
                "lernziel": "apt-cache search sucht nach Software in den Paketquellen (kein sudo noetig).",
            },
            {
                "id":    "aptshow_berg",
                "ziel":  "Zeige Details zum Paket nano an. Nutze: apt-cache show nano",
                "check": lambda cmd, out, p: ("apt-cache" in cmd and "show" in cmd) or (bool(cmd.split()) and cmd.split()[0] == "apt" and "show" in cmd),
                "belohnung":"📜 Schriftrolle der Information",
                "lernziel": "apt-cache show zeigt Details zu einem Paket. apt install NAME installiert es.",
            },
            {
                "id":    "aptlist_berg",
                "ziel":  "Liste alle installierten Pakete auf. Nutze: apt list --installed",
                "check": lambda cmd, out, p: "apt" in cmd and "list" in cmd,
                "belohnung":"📜 Schriftrolle der Pakete",
                "lernziel": "apt list --installed zeigt alle installierten Pakete. sudo apt install fuer neue!",
            },
            {
                "id":       "which_berg",
                "ziel":     "Finde wo nano liegt: which nano",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='which' and len(cmd.split())>=2,
                "belohnung":"📜 Schriftrolle des Weges",
                "lernziel": "which findet den vollen Pfad eines Programms (z.B. /usr/bin/nano). Gut in Skripten.",
            },
            {
                "id":       "dpkgl_berg",
                "ziel":     "Liste installierte Pakete: dpkg -l | head -20",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='dpkg' and '-l' in cmd,
                "belohnung":"📜 Schriftrolle der Inventur",
                "lernziel": "dpkg -l listet alle installierten Pakete. dpkg -l | grep python sucht spezifische.",
            },
            {
                "id":       "aptdep_berg",
                "ziel":     "Zeige Abhaengigkeiten: apt-cache depends nano",
                "check":    lambda cmd, out, p: bool(cmd.split()) and 'depends' in cmd,
                "belohnung":"📜 Schriftrolle der Beziehungen",
                "lernziel": "apt-cache depends zeigt welche Pakete benoetigt werden. Wichtig bei Installationsproblemen.",
            },
            {
                "id":       "aptinstall_berg",
                "ziel":     "Simuliere Installation: apt-get install -s sl",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] in ['apt-get','apt'] and 'install' in cmd,
                "belohnung":"📜 Schriftrolle der Magie",
                "lernziel": "apt-get install -s simuliert ohne wirklich zu installieren. sudo apt install NAME installiert.",
            },
        ],
    },
    "hafen": {
        "name":   "Hafen der Verbindungen",
        "emoji":  "⚓",
        "beschreibung": (
            "Der Hafen der Verbindungen liegt am digitalen Meer, wo unzaehlige Datenpakete\n"
            "wie Schiffe ein- und auslaufen. Hier lernt Mia, wie Computer miteinander\n"
            "kommunizieren und Dateien aus dem Internet heruntergeladen werden."
        ),
        "ausgaenge": {"bergpass": "Bergpass", "turm": "Turm", "akademie": "Akademie", "fernwelt": "Fernwelt-Portal"},
        "npc": {
            "name": "Kapitaenin Sara",
            "bild": "🚢",
            "dialoge": [
                "Willkommen im Hafen, Abenteurerin! Ich bin Kapitaenin Sara.\n"
                "Unser Hafen ist das Tor zur digitalen Welt!\n"
                "Mit 'ping' kannst du pruefen, ob ein Server erreichbar ist.",
                "Mit 'ping -c 3 8.8.8.8' sendest du genau 3 Pakete an Googles DNS-Server!\n"
                "Probier es: ping -c 3 8.8.8.8",
                "'wget' laedt Dateien aus dem Internet herunter!\n"
                "Probiere: wget https://example.com",
                "Ausgezeichnet! Du hast den Hafen gemeistert!\n"
                "Jetzt kannst du im Netzwerk navigieren wie eine echte Kapitaenin.\n"
                "Weiter zum Turm der Schreibkunst!",
            ],
        },
        "quests": [
            {
                "id":    "ping_hafen",
                "ziel":  "Teste die Netzwerkverbindung zu Googles DNS-Server! Sende genau 3 Pakete: ping -c 3 8.8.8.8",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "ping" and len(cmd.split()) >= 2,
                "belohnung":"📜 Schriftrolle des Netzwerks",
                "lernziel": "ping testet ob ein Server erreichbar ist. -c 3 sendet genau 3 Pakete.",
            },
            {
                "id":    "wget_hafen",
                "ziel":  "Lade eine Webseite aus dem Internet herunter! Nutze wget: wget https://example.com",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "wget" and len(cmd.split()) >= 2,
                "belohnung":"📜 Schriftrolle des Downloads",
                "lernziel": "wget laedt Dateien aus dem Internet herunter. Sehr nuetzlich fuer Skripte!",
            },
            {
                "id":    "curl_hafen",
                "ziel":  "Sende eine HTTP-Anfrage an eine Webseite! Nutze curl: curl https://example.com",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "curl" and len(cmd.split()) >= 2,
                "belohnung":"📜 Schriftrolle der Abfrage",
                "lernziel": "curl sendet HTTP-Anfragen und zeigt Antworten. curl -O laedt Dateien herunter.",
            },
            {
                "id":       "curlI_haf",
                "ziel":     "Zeige HTTP-Header: curl -I https://example.com",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='curl' and '-I' in cmd,
                "belohnung":"📜 Schriftrolle der Kopfzeilen",
                "lernziel": "curl -I zeigt nur HTTP-Header (Status-Code, Content-Type etc.) ohne Body. Sehr nuetzlich!",
            },
            {
                "id":       "hostname_haf",
                "ziel":     "Zeige deinen Hostnamen: hostname",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='hostname',
                "belohnung":"📜 Schriftrolle des Namens",
                "lernziel": "hostname zeigt den Computernamen. hostname -I zeigt alle IP-Adressen. Aenderbar in /etc/hostname.",
            },
            {
                "id":       "ss_haf",
                "ziel":     "Zeige offene Ports: ss -tuln",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] in ['ss','netstat'],
                "belohnung":"📜 Schriftrolle der Verbindungen",
                "lernziel": "ss -tuln zeigt offene Ports und Verbindungen. netstat -tuln ist die aeltere Alternative.",
            },
            {
                "id":       "nslookup_haf",
                "ziel":     "Schlage IP nach: nslookup google.com",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] in ['nslookup','dig','host'] and len(cmd.split())>=2,
                "belohnung":"📜 Schriftrolle der Adressen",
                "lernziel": "nslookup loest Domainnamen zu IP-Adressen (DNS). dig ist modernere Alternative.",
            },
        ],
    },
    "turm": {
        "name":   "Turm der Schreibkunst",
        "emoji":  "🗼",
        "beschreibung": (
            "Der Turm der Schreibkunst ragt hoch ueber der Landschaft Binarias auf,\n"
            "umgeben von schwebenden Schriftzeichen und leuchtenden Bash-Formeln.\n"
            "Zauberer Xan huetet die alten Geheimnisse der Skripte."
        ),
        "ausgaenge": {"hafen": "Hafen", "drachenfestung": "Drachenfestung", "taverne": "Taverne"},
        "npc": {
            "name": "Zauberer Xan",
            "bild": "🔮",
            "dialoge": [
                "Ah, eine neue Schuelerin! Ich bin Zauberer Xan, Meister der Textmagie!\n"
                "In meinem Turm lernst du, wie man Zauberformeln – Skripte – erschafft!\n"
                "Oeffne den Texteditor nano: nano zauber.txt",
                "Der maechtigste Zauber ist 'nano' – ein Texteditor im Terminal!\n"
                "Strg+O speichert, Strg+X beendet. Erstelle nun ein Skript:\n"
                "echo '#!/bin/bash' > zauber.sh",
                "Bash-Skripte beginnen immer mit '#!/bin/bash' – die Shebang-Zeile!\n"
                "Jetzt hauch dem Skript Leben ein:\n"
                "chmod +x zauber.sh",
                "Mit 'chmod +x zauber.sh' wird das Skript ausfuehrbar!\n"
                "Dann kannst du es mit './zauber.sh' starten.\n"
                "Viel Erfolg in der Drachenfestung!",
            ],
        },
        "quests": [
            {
                "id":    "nano_turm",
                "ziel":  "Oeffne den Texteditor nano und erstelle eine neue Zauberdatei! Tippe: nano zauber.txt",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "nano" and len(cmd.split()) >= 2,
                "belohnung":"📜 Schriftrolle der Textmagie",
                "lernziel": "nano ist ein einfacher Texteditor im Terminal. Strg+O speichert, Strg+X beendet.",
            },
            {
                "id":    "script_turm",
                "ziel":  "Erstelle ein Bash-Skript mit der Shebang-Zeile! Tippe: echo '#!/bin/bash' > zauber.sh",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "echo" and ">" in cmd and ".sh" in cmd,
                "belohnung":"📜 Schriftrolle der Skripte",
                "lernziel": "#!/bin/bash ist die 'Shebang'-Zeile. Sie sagt: dieses Skript ist ein Bash-Skript!",
            },
            {
                "id":    "chmod_turm",
                "ziel":  "Mache das Skript ausfuehrbar mit dem chmod-Befehl! Tippe: chmod +x zauber.sh",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "chmod" and "+x" in cmd and ".sh" in cmd,
                "belohnung":"📜 Schriftrolle des Lebens",
                "lernziel": "chmod +x macht das Skript ausfuehrbar. Dann starten mit: ./skript.sh",
            },
            {
                "id":       "execute_turm",
                "ziel":     "Fuehre das Skript aus: ./experiment.sh",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0].startswith('./'),
                "belohnung":"📜 Schriftrolle der Ausfuehrung",
                "lernziel": "./ fuehrt Skript im aktuellen Ordner aus. Braucht chmod +x vorher. Beginnt mit #!/bin/bash.",
            },
            {
                "id":       "osrelease_turm",
                "ziel":     "Welches Ubuntu? cat /etc/os-release",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='cat' and 'os-release' in cmd,
                "belohnung":"📜 Schriftrolle des Systems",
                "lernziel": "cat /etc/os-release zeigt Ubuntu-Version und Systeminfos. lsb_release -a ist alternativ.",
            },
            {
                "id":       "uname_turm",
                "ziel":     "Zeige Kernel-Info: uname -a",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='uname',
                "belohnung":"📜 Schriftrolle des Kerns",
                "lernziel": "uname -a zeigt Kernel-Version, Architektur, Hostname. uname -r = nur Kernel-Version.",
            },
            {
                "id":       "history_turm",
                "ziel":     "Zeige Befehlshistorie: history",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='history',
                "belohnung":"📜 Schriftrolle der Geschichte",
                "lernziel": "history zeigt alle getippten Befehle. !! wiederholt letzten. !42 = Befehl Nr 42. Strg+R sucht.",
            },
        ],
    },
    "drachenfestung": {
        "name":   "Drachenfestung – Endkampf!",
        "emoji":  "🐉",
        "beschreibung": (
            "Die Drachenfestung erhebt sich finster am Ende des Weges –\n"
            "Flammenwolken umhuellen ihre schwarzen Tuerme und der Boden bebt\n"
            "bei jedem Schritt des maechtigen Drachen Remirf!"
        ),
        "ausgaenge": {"turm": "Turm"},
        "npc": {
            "name": "Drache Remirf",
            "bild": "🐲",
            "dialoge": [
                "MWAHAHAHA! So, die kleine Linux-Abenteurerin wagt es, meine Festung zu betreten?!\n"
                "Ich bin REMIRF, der unbesiegbare Drachenkoenig!\n"
                "Du wirst hier scheitern!",
                "Meine Schwaeche?! NIEMALS wirst du sie finden!\n"
                "Oder... warte. Schau dir die Datei an, wenn du dich traust!\n"
                "Tippe: grep \"SCHWAECHE\" drachen_geheimnis.txt",
                "Grr! Du hast mein Geheimnis gefunden!\n"
                "Aber der Zauberbann ist nutzlos ohne Ausfuehrungsrechte! Ha!\n"
                "Tippe 'chmod +x drachenbann.sh' – falls du dich traust!",
                "N-NEIN! Der Bann wirkt! REMIRF verliert seine Macht...\n"
                "Du... du hast es wirklich geschafft! Alle Linux-Befehle gemeistert...\n"
                "Du bist die wahre Herrscherin von Binaria! *REMIRF fliegt davon*",
            ],
        },
        "quests": [
            {
                "id":       "ls_drache",
                "ziel":     "Erkunde die Festung: ls -la",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='ls' and '-l' in cmd,
                "belohnung":"⚔️ Erkundungszeichen",
                "lernziel": "Immer erstmal ls -la! Berechtigungen, versteckte Dateien, alles auf einen Blick.",
            },
            {
                "id":       "cat_drache",
                "ziel":     "Lies das Geheimdokument: cat drachen_geheimnis.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0]=='cat' and 'geheimnis' in cmd,
                "belohnung":"⚔️ Wissenszeichen",
                "lernziel": "cat zum Lesen, grep zum Suchen. Zusammen maechtiger als einzeln!",
            },
            {
                "id":    "grep_drache",
                "ziel":  "Finde die Schwaeche des Drachen! Tippe: grep \"SCHWAECHE\" drachen_geheimnis.txt",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "grep" and len(cmd.split()) >= 3,
                "belohnung":"⚔️ Schwertschlag des Wissens",
                "lernziel": "grep findet verstecktes Wissen – auch in echten Logs und Konfigdateien!",
            },
            {
                "id":    "chmod_drache",
                "ziel":  "Mache den Zauberbann ausfuehrbar! Tippe: chmod +x drachenbann.sh",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "chmod" and "+x" in cmd and "drachenbann" in cmd,
                "belohnung":"⚔️ Schild der Macht",
                "lernziel": "chmod +x macht ein Skript ausfuehrbar. Der Zauberbann ist bereit!",
            },
            {
                "id":    "execute_drache",
                "ziel":  "Fuehre den Drachenbann aus und besiege Remirf! Tippe: ./drachenbann.sh",
                "check": lambda cmd, out, p: "drachenbann" in cmd and cmd.startswith("./"),
                "belohnung":"⚔️ Zepter des Sieges",
                "lernziel": "./ fuehrt ein Skript im aktuellen Verzeichnis aus. Du hast es geschafft!",
            },
        ],
    },

    "schmiede": {
        "name": "Schmiede der Archive",
        "emoji": "⚒️",
        "beschreibung": "Eine mächtige Schmiede mit loderndem Feuer und gluehenden Kohlen, wo Daten zu Archiven verdichtet werden. Hier lernst du tar, gzip und zip zu meistern.",
        "ausgaenge": {"festung": "Festung"},
        "ascii_art": [
            "    *   F E U E R   *   ",
            "   /|\\   Esse    /|\\  ",
            "  [===== Amboss =====]  ",
            "  |~~~~  Glut  ~~~~~|  ",
            "  |___  SCHMIEDE  ___|  ",
        ],
        "npc": {
            "name": "Schmiedin Rosa",
            "bild": "🔨",
            "dialoge": [
                "Willkommen in der Schmiede der Archive! Ich bin Rosa, Hueterin der Archivkunst. Hier formen wir nicht nur Metall, sondern auch Daten! Das wichtigste Werkzeug ist 'tar'. Erstelle dein erstes Archiv: tar -czvf archiv.tar.gz buecher.txt - Merke: c=create, z=gzip, v=verbose, f=filename!",
                "Sehr gut! Jetzt lernst du Archivinhalte zu lesen und zu entpacken. Mit 'tar -tzvf archiv.tar.gz' listest du alle Dateien ohne zu entpacken - immer zuerst schauen was drin ist! Dann mit 'tar -xzvf archiv.tar.gz' entpackst du: x=extract. Das Trio c=erstellen, t=auflisten, x=entpacken ist der Kern von tar!",
                "Ausgezeichnet, Archivschmiedin Mia! Du beherrschst das gesamte Arsenal: tar (c/t/x fuer alles rund ums Archiv), gzip und gunzip fuer Einzeldateien (.gz), zip und unzip fuer Windows-Kompatibilitaet. Backups und Dateiuebertragungen werden dich nie mehr schrecken!",
            ],
        },
        "quests": [
            {
                "id": "tar_create",
                "ziel": "Erstelle Archiv: tar -czvf archiv.tar.gz buecher.txt",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'tar' and '-c' in cmd,
                "belohnung": "📜 Schriftrolle des Archivs",
                "lernziel": "tar -czvf = create, zip, verbose, file. Wichtig fuer Backups!",
            },
            {
                "id": "tar_list",
                "ziel": "Zeige Archivinhalt: tar -tzvf archiv.tar.gz",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'tar' and '-t' in cmd,
                "belohnung": "📜 Schriftrolle des Inhalts",
                "lernziel": "tar -t = list. Immer pruefen bevor man entpackt. Was ist drin?",
            },
            {
                "id": "tar_extract",
                "ziel": "Entpacke Archiv: tar -xzvf archiv.tar.gz",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'tar' and '-x' in cmd,
                "belohnung": "📜 Schriftrolle der Befreiung",
                "lernziel": "tar -x = extract. Merke: c=create, t=table/list, x=extract.",
            },
            {
                "id": "gzip_comp",
                "ziel": "Komprimiere Datei: gzip lagerliste.txt",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'gzip' and len(cmd.split()) >= 2,
                "belohnung": "📜 Schriftrolle der Verdichtung",
                "lernziel": "gzip komprimiert (.gz). Originaldatei wird ersetzt. gunzip zum Dekomprimieren.",
            },
            {
                "id": "gunzip_de",
                "ziel": "Dekomprimiere: gunzip lagerliste.txt.gz",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'gunzip',
                "belohnung": "📜 Schriftrolle der Befreiung",
                "lernziel": "gunzip oder gzip -d dekomprimiert. zcat zeigt komprimierte Dateien ohne Entpacken.",
            },
            {
                "id": "zip_create",
                "ziel": "Erstelle ZIP: zip paket.zip *.txt",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'zip' and len(cmd.split()) >= 3,
                "belohnung": "📜 Schriftrolle der Buendelung",
                "lernziel": "zip ist Windows-kompatibel. unzip zum Entpacken. Plattformuebergreifend!",
            },
        ],
        "dateien": [
            {
                "dateiname": "lagerliste.txt",
                "inhalt": "Vorraete in der Schmiede:\n- Eisen x 50\n- Kohle x 30\n- Kupfer x 20\n",
            },
        ],
    },
    "sternwarte": {
        "name": "Sternwarte des Systems",
        "emoji": "🔭",
        "beschreibung": "Ein hoher Beobachtungsturm mit riesigem Teleskop und freiem Blick auf das gesamte System. Astronom Kepler lehrt dich hier die Systembeobachtung mit uname, df, free und mehr.",
        "ausgaenge": {"bergpass": "Bergpass"},
        "ascii_art": [
            "   *  .  * Sterne *  .  *  ",
            "    .   *   .   *   .   *  ",
            "   |    ( Teleskop  )   |  ",
            "   |___/   Sockel   \\__|  ",
            "   [====  STERNWARTE ====] ",
        ],
        "npc": {
            "name": "Astronom Kepler",
            "bild": "⭐",
            "dialoge": [
                "Willkommen in der Sternwarte des Systems! Ich bin Kepler, Beobachter der digitalen Sterne. Wie ich Himmelskoerper analysiere, analysierst du dein System! Starte mit 'uname -a' - es zeigt Kernel-Version, Hostname und Architektur. Das Fundament jeder Systemanalyse!",
                "Hervorragend! Nun erkunden wir die Ressourcen. 'df -h' zeigt Festplattenplatz - h bedeutet human-readable, also GB und MB statt rohe Bytes. 'free -h' zeigt RAM-Nutzung, entscheidend fuer die Performance! 'du -sh *' zeigt welche Ordner am meisten Platz belegen. Diese drei Befehle retten jeden Administrator!",
                "Fantastisch! Du bist nun Systemastronom! Dein Werkzeugkasten: uname (System-Identitaet), df (Festplattenplatz), free (RAM-Nutzung), du (Ordner-Groessen), date (aktuelles Datum und Zeit), cal (Kalender), uptime (Laufzeit und Load Average). Mit diesen Werkzeugen kennst du deinen Server wie ich die Sterne!",
            ],
        },
        "quests": [
            {
                "id": "uname_stern",
                "ziel": "Zeige Systeminfo: uname -a",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'uname',
                "belohnung": "📜 Schriftrolle des Universums",
                "lernziel": "uname -a: Kernel, Hostname, Architektur. uname -r = nur Kernel-Version.",
            },
            {
                "id": "df_stern",
                "ziel": "Zeige Festplattenplatz: df -h",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'df',
                "belohnung": "📜 Schriftrolle des Raums",
                "lernziel": "df -h zeigt Festplattenplatz. -h = human-readable (GB/MB). Wichtig fuer Admins!",
            },
            {
                "id": "free_stern",
                "ziel": "Zeige RAM-Nutzung: free -h",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'free',
                "belohnung": "📜 Schriftrolle des Gedaechtnisses",
                "lernziel": "free -h zeigt RAM-Nutzung. Buff/Cache kann freigegeben werden. Swap = Auslagerungsdatei.",
            },
            {
                "id": "du_stern",
                "ziel": "Zeige Ordnergroessen: du -sh *",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'du',
                "belohnung": "📜 Schriftrolle der Groesse",
                "lernziel": "du -sh * = disk usage, summary, human-readable. du -sh /home/*/ zeigt Home-Groessen.",
            },
            {
                "id": "date_stern",
                "ziel": "Zeige Datum und Zeit: date",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'date',
                "belohnung": "📜 Schriftrolle der Zeit",
                "lernziel": "date zeigt Datum/Zeit. date '+%Y-%m-%d' = ISO-Format. Sehr nuetzlich in Skripten.",
            },
            {
                "id": "cal_stern",
                "ziel": "Zeige Kalender: cal",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'cal',
                "belohnung": "📜 Schriftrolle des Kalenders",
                "lernziel": "cal zeigt den Monat. cal -3 = 3 Monate. cal 2024 = ganzes Jahr.",
            },
            {
                "id": "uptime_stern",
                "ziel": "Zeige Systemlaufzeit: uptime",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'uptime',
                "belohnung": "📜 Schriftrolle der Ausdauer",
                "lernziel": "uptime: Laufzeit und Load Average (1/5/15 Min). <CPU-Kerne = entspannt.",
            },
        ],
        "dateien": [
            {
                "dateiname": "sternenkarte.txt",
                "inhalt": "=== Systembeobachtung ===\nuname, df, free, du, date, cal\n",
            },
        ],
    },
    "akademie": {
        "name": "Akademie der Variablen",
        "emoji": "🎓",
        "beschreibung": "Eine ehrwuerdige Universitaet mit Saeulengaengen und Bueregalen voller Wissen. Professorin Euler enthuellt hier die Geheimnisse der Umgebungsvariablen und des export-Befehls.",
        "ausgaenge": {"hafen": "Hafen", "magierschule": "Magierschule"},
        "ascii_art": [
            "  | |  AKADEMIE  | |   ",
            "  |=|  _________  |=| ",
            "  | | | Variablen| | | ",
            "  | | |__________| | | ",
            "  | |  Saeulenhalle | | ",
            "  |__|______________|__| ",
        ],
        "npc": {
            "name": "Professorin Euler",
            "bild": "📐",
            "dialoge": [
                "Guten Tag! Ich bin Professorin Euler, und ich heisse dich herzlich willkommen an der Akademie der Variablen! Umgebungsvariablen sind magische Botschaften, die dein System dir bereitstellt. Die wichtigste: $HOME! Probiere: echo $HOME - Das Dollarzeichen sagt Linux: Zeig mir den Wert dieser Variable!",
                "Wunderbar! Weiter geht es mit deinem Benutzernamen: echo $USER zeigt wer du bist, perfekt fuer Skripte! Und echo $PATH zeigt alle Ordner, wo Linux nach Programmen sucht, getrennt durch Doppelpunkte. Wenn ein Programm nicht gefunden wird, liegt es oft am falschen $PATH!",
                "Exzellent! Jetzt erschaffst du eigene Variablen! Mit 'export ZAUBER=Expecto' setzt du eine Variable und machst sie fuer alle Unterprozesse sichtbar. Ohne export ist sie nur in deiner Shell bekannt. 'env | head -10' zeigt alle aktuell gesetzten Variablen - eine ganze Schatzkammer!",
                "Magnifico! Du hast die Akademie der Variablen erfolgreich abgeschlossen! Die wichtigsten Variablen: $HOME (Heimatverzeichnis), $USER (Benutzername), $PATH (Suchpfade fuer Programme), $SHELL (deine aktive Shell). Mit export teilst du Variablen mit Unterprogrammen. printenv prueft einzelne Variablen gezielt. Die Magierschule wartet!",
            ],
        },
        "quests": [
            {
                "id": "home_akad",
                "ziel": "Zeige Home: echo $HOME",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'echo' and 'HOME' in cmd,
                "belohnung": "📜 Schriftrolle des Heims",
                "lernziel": "$HOME = dein Home-Verzeichnis. cd ohne Argumente = cd $HOME.",
            },
            {
                "id": "user_akad",
                "ziel": "Zeige Benutzer: echo $USER",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'echo' and 'USER' in cmd,
                "belohnung": "📜 Schriftrolle des Namens",
                "lernziel": "$USER enthaelt Benutzernamen. $UID = User-ID. Nuetzlich in Skripten.",
            },
            {
                "id": "path_akad",
                "ziel": "Zeige Suchpfad: echo $PATH",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'echo' and 'PATH' in cmd,
                "belohnung": "📜 Schriftrolle der Wege",
                "lernziel": "$PATH: Ordner wo Linux Programme sucht. : als Trenner. which zeigt welcher Pfad genutzt.",
            },
            {
                "id": "export_akad",
                "ziel": "Setze Variable: export ZAUBER='Expecto'",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'export',
                "belohnung": "📜 Schriftrolle der Schoepfung",
                "lernziel": "export macht Variablen fuer Kind-Prozesse sichtbar. Ohne export: nur in Shell sichtbar.",
            },
            {
                "id": "env_akad",
                "ziel": "Zeige Umgebung: env | head -10",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'env',
                "belohnung": "📜 Schriftrolle der Umgebung",
                "lernziel": "env zeigt alle gesetzten Variablen. printenv VARIABLE zeigt einzelne.",
            },
            {
                "id": "printenv_akad",
                "ziel": "Pruefe Variable: printenv HOME",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'printenv',
                "belohnung": "📜 Schriftrolle der Pruefung",
                "lernziel": "printenv NAME zeigt Wert. Gibt nichts aus wenn Variable nicht gesetzt.",
            },
        ],
        "dateien": [
            {
                "dateiname": "variablen.txt",
                "inhalt": "Wichtige Umgebungsvariablen:\n$HOME - Home-Verzeichnis\n$USER - Benutzername\n$PATH - Suchpfad\n$SHELL - Shell-Pfad\n",
            },
        ],
    },
    "taverne": {
        "name": "Taverne der Tricks",
        "emoji": "🍺",
        "beschreibung": "Eine gemütliche Taverne mit Holzfaessern, Kerzen und warmem Herdfeuer. Wirt Gottfried kennt alle Shell-Tricks und teilt sie gerne bei einem Becher Met.",
        "ausgaenge": {"turm": "Turm"},
        "ascii_art": [
            "  [======= TAVERNE =======]  ",
            "  | Fass |  Theke  | Fass |  ",
            "  | [=]  | [=] [=] |  [=] |  ",
            "  |    * Kerzenschein *    |  ",
            "  |______warm und gut______|  ",
        ],
        "npc": {
            "name": "Wirt Gottfried",
            "bild": "🧙",
            "dialoge": [
                "Willkommen in der Taverne der Tricks! Ich bin Gottfried, Wirt und Meister der verborgenen Shell-Kuenste! Setz dich und lass dir von mir die Geheimnisse der Profis verraten! Starte mit: history | tail -20 - Du siehst deine letzten 20 Befehle. Mit !42 fuehrst du Befehl 42 erneut aus. Strg+R sucht im Verlauf!",
                "Bravo! Jetzt die echten Profitricks: Mit 'alias ll=ls -la' erstellst du eigene Kurzbefehle, in ~/.bashrc gespeichert bleiben sie dauerhaft! 'type ls' zeigt ob ls ein Programm, Alias oder Shell-Built-in ist, unverzichtbar zur Fehlersuche. 'which python3' zeigt den vollen Pfad, wichtig bei mehreren installierten Versionen!",
                "Prost auf dich, wahrer Shell-Meister! Meine besten Geheimtipps: history und Strg+R fuer blitzschnelle Befehlssuche, alias spart Tipparbeit, type und which spueren Programme auf, echo $? prueft den letzten Exit-Code (0=Erfolg!), tee zeigt Ausgabe gleichzeitig an und speichert sie. Und vergiss nie die Tab-Taste fuer Autovervollstaendigung!",
            ],
        },
        "quests": [
            {
                "id": "history_tav",
                "ziel": "Zeige Verlauf: history | tail -20",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'history',
                "belohnung": "📜 Schriftrolle der Erinnerung",
                "lernziel": "history zeigt alle Befehle mit Nummern. !42 = Befehl 42. !! = letzter. Strg+R sucht.",
            },
            {
                "id": "alias_tav",
                "ziel": "Erstelle Kurzbefehl: alias ll='ls -la'",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'alias',
                "belohnung": "📜 Schriftrolle der Abkuerzung",
                "lernziel": "alias erstellt Kurzbefehle. In ~/.bashrc = dauerhaft. alias ohne Args = alle anzeigen.",
            },
            {
                "id": "type_tav",
                "ziel": "Was ist ls? type ls",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'type' and len(cmd.split()) >= 2,
                "belohnung": "📜 Schriftrolle der Wahrheit",
                "lernziel": "type zeigt ob Programm, Alias, Shell-Funktion oder Built-in. Nuetzlich zur Fehlersuche.",
            },
            {
                "id": "which_tav",
                "ziel": "Wo liegt Python? which python3",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'which' and len(cmd.split()) >= 2,
                "belohnung": "📜 Schriftrolle des Pfades",
                "lernziel": "which zeigt vollen Pfad. Gut wenn mehrere Versionen installiert sind.",
            },
            {
                "id": "exitcode_tav",
                "ziel": "Pruefe Exit-Code: echo $?",
                "check": lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == 'echo' and '?' in cmd,
                "belohnung": "📜 Schriftrolle des Ergebnisses",
                "lernziel": "$? = Exit-Code des letzten Befehls. 0=Erfolg, sonst Fehler. In Skripten sehr wichtig!",
            },
            {
                "id": "tee_tav",
                "ziel": "Zeige und speichere: ls | tee liste.txt",
                "check": lambda cmd, out, p: 'tee' in cmd,
                "belohnung": "📜 Schriftrolle des T-Stuecks",
                "lernziel": "tee zeigt Ausgabe UND speichert gleichzeitig. Wie ein T-Stueck in einer Wasserleitung!",
            },
        ],
        "dateien": [
            {
                "dateiname": "trickliste.txt",
                "inhalt": "Shell-Tricks:\nStrg+C - Abbrechen\nStrg+L - Leeren\nStrg+A - Zeilenanfang\nTab - Autovervollstaendigung\nPfeil-Oben - Vorheriger Befehl\n",
            },
        ],
    },

    "magierschule": {
        "name": "Magierschule der Skripte",
        "emoji": "🪄",
        "beschreibung": (
            "In der Magierschule der Skripte lernst du die Kunst des Bash-Skriptings: "
            "Variablen setzen, Schleifen schreiben und Bedingungen formulieren. "
            "Mit dem Wissen der Zauberlehrerin Hypathia wirst du deine eigenen Skripte erschaffen!"
        ),
        "ausgaenge": {
            "akademie": "Akademie",
        },
        "npc": {
            "name": "Zauberlehrerin Hypathia",
            "bild": "✨",
            "dialoge": [
                "Willkommen, Zauberlehrling! Ich bin Hypathia, Meisterin der Bash-Skripte! ✨ "
                "Das Fundament aller Magie sind Variablen. Setze deine erste Variable: NAME='Linux' "
                "– kein Leerzeichen um das Gleichheitszeichen, das ist das erste Gesetz der Skript-Magie!",
                "Wunderbar! Jetzt rufe deine Variable mit echo $NAME – das Dollarzeichen beschwört den Wert. 🌟 "
                "Und dann lerne Schleifen: for i in 1 2 3; do echo $i; done "
                "– Wiederholung ist die Mutter der Skript-Magie!",
                "Beeindruckend! Jetzt zu den mächtigsten Zaubern: if [ -f zauber.sh ]; then echo 'Vorhanden'; fi "
                "– Bedingungen entscheiden das Schicksal. ✨ test && kombiniert Zaubersprüche. "
                "Dann erschaffe dein erstes eigenes Skript mit echo und >!",
                "Du hast alle sieben Skript-Zauber gemeistert! 🪄 "
                "Das große Wissen: NAME='Wert' setzt Variablen, $NAME ruft sie, "
                "for...do...done sind Schleifen, if...fi sind Bedingungen. "
                "#!/bin/bash kommt immer zuerst, chmod +x macht ausführbar. "
                "Du bist nun eine echte Skript-Magierin!",
            ],
        },
        "ascii_art": [
            "  ✨  *   MAGIERSCHULE   *  ✨  ",
            "  🪄      der Skripte      🪄  ",
            "  |   *   Bash-Zauber   *   |  ",
            "  |   Skripte entstehen!    |  ",
            "   \\________________________/  ",
            "    ✨   bash  scripts   ✨    ",
        ],
        "quests": [
            {
                "id": "var_mag",
                "ziel": "Setze Variable: NAME='Linux'",
                "check": lambda cmd, out, p: (
                    "=" in cmd
                    and bool(cmd.split())
                    and cmd.split()[0] not in [
                        "cd", "ls", "cat", "echo", "grep", "find",
                        "chmod", "cp", "mv", "rm", "mkdir", "touch", "pwd",
                    ]
                ),
                "belohnung": "📜 Schriftrolle der Beschwörung",
                "lernziel": "Variablen in Bash: NAME='Wert'. Kein Leerzeichen um =! Zugriff mit $NAME.",
            },
            {
                "id": "echo_var_mag",
                "ziel": "Nutze Variable: echo $NAME",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "echo"
                    and "$" in cmd
                ),
                "belohnung": "📜 Schriftrolle des Rufens",
                "lernziel": (
                    "In doppelten Anführungszeichen werden Variablen expandiert. "
                    "In einfachen nicht!"
                ),
            },
            {
                "id": "forloop_mag",
                "ziel": "Erstelle Schleife: for i in 1 2 3; do echo $i; done",
                "check": lambda cmd, out, p: (
                    "for" in cmd
                    and "do" in cmd
                    and "done" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Wiederholung",
                "lernziel": (
                    "for i in LISTE; do BEFEHL; done. "
                    "Auch: for f in *.txt; do cat $f; done"
                ),
            },
            {
                "id": "if_mag",
                "ziel": "Schreibe Bedingung: if [ -f zauber.sh ]; then echo 'Vorhanden'; fi",
                "check": lambda cmd, out, p: (
                    "if" in cmd
                    and "fi" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Entscheidung",
                "lernziel": (
                    "if [ BEDINGUNG ]; then...; fi. "
                    "-f=Datei, -d=Ordner. [ ] braucht Leerzeichen!"
                ),
            },
            {
                "id": "test_mag",
                "ziel": "Teste Datei: test -f zauber.sh && echo 'Ja'",
                "check": lambda cmd, out, p: (
                    "&&" in cmd
                    and ("test" in cmd or "[" in cmd)
                ),
                "belohnung": "📜 Schriftrolle des Tests",
                "lernziel": (
                    "test -f = Datei vorhanden? "
                    "&& = nur wenn Erfolg. || = nur wenn Fehler."
                ),
            },
            {
                "id": "script_mag",
                "ziel": "Schreibe Skript: echo -e '#!/bin/bash\\necho Hallo' > mein.sh",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "echo"
                    and ".sh" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Schöpfung",
                "lernziel": (
                    "#!/bin/bash muss erste Zeile sein (Shebang). "
                    "echo -e erlaubt \\n als Zeilenumbruch."
                ),
            },
            {
                "id": "exec_mag",
                "ziel": "Fuehre Skript aus: chmod +x mein.sh && ./mein.sh",
                "check": lambda cmd, out, p: (
                    "chmod" in cmd
                    and "+x" in cmd
                ),
                "belohnung": "📜 Schriftrolle des Lebens",
                "lernziel": (
                    "chmod +x dann ./ - vollstaendiger Workflow fuer eigene Bash-Skripte. "
                    "Klappt immer!"
                ),
            },
        ],
        "dateien": [
            {
                "dateiname": "zauber_vorlage.sh",
                "inhalt": (
                    "#!/bin/bash\n"
                    "# Kommentar\n"
                    "NAME='Mia'\n"
                    "echo \"Hallo, $NAME!\"\n"
                    "for i in 1 2 3; do echo \"Nr: $i\"; done\n"
                ),
            },
        ],
    },

    "palast": {
        "name": "Palast der Benutzer",
        "emoji": "🏛️",
        "beschreibung": (
            "Im Palast der Benutzer herrscht König Root über alle Konten und Gruppen. "
            "Hier lernst du, Benutzer zu verstehen: whoami, id, groups "
            "und die heiligen Dateien /etc/passwd und /etc/group."
        ),
        "ausgaenge": {
            "labor": "Labor",
        },
        "npc": {
            "name": "Koenig Root",
            "bild": "👑",
            "dialoge": [
                "Ich bin König Root, Herrscher aller Benutzer! 👑 "
                "In meinem Reich kennt jeder seinen Platz. "
                "Erkenne zuerst dich selbst: whoami zeigt deinen Namen, "
                "id zeigt deine vollständige Identität mit uid, gid und allen Gruppen!",
                "Gut gemacht! Nun erkunde die Gilden: groups zeigt deine Mitgliedschaften. 🏛️ "
                "Die sudo-Gruppe ist Adel! Schau in /etc/passwd – dort wohnen alle Untertanen. "
                "Und /etc/group zeigt alle Zünfte des Reiches.",
                "Du kennst mein Reich! 👑 "
                "Das große Wissen: whoami=Name, id=volle Identität (uid/gid/groups), "
                "groups=Mitgliedschaften, /etc/passwd=alle Benutzer (name:x:uid:gid:info:home:shell), "
                "/etc/group=alle Gruppen, sudo -l=deine Rechte. "
                "Mit sudo regierst du das System!",
            ],
        },
        "ascii_art": [
            "        👑  PALAST  👑        ",
            "       / der Benutzer \\      ",
            "      | 🏛️  |  🏛️  |  🏛️ |   ",
            "      |   ==  THRON  ==  |   ",
            "       \\_________________/   ",
            "         *  Willkommen  *    ",
        ],
        "quests": [
            {
                "id": "whoami_pal",
                "ziel": "Wer regiert? whoami",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "whoami"
                ),
                "belohnung": "📜 Schriftrolle der Herrschaft",
                "lernziel": (
                    "whoami zeigt aktuellen Benutzernamen. "
                    "In Skripten: pruefen ob man root ist."
                ),
            },
            {
                "id": "id_pal",
                "ziel": "Zeige alle IDs: id",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "id"
                ),
                "belohnung": "📜 Schriftrolle der Identitaet",
                "lernziel": (
                    "id zeigt uid=N(name) gid=N(name) groups=... "
                    "Unverzichtbar fuer Berechtigungsprobleme."
                ),
            },
            {
                "id": "groups_pal",
                "ziel": "Zeige Gruppen: groups",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "groups"
                ),
                "belohnung": "📜 Schriftrolle der Zungen",
                "lernziel": (
                    "groups zeigt Mitgliedschaften. "
                    "sudo-Gruppe = Admin. docker-Gruppe = Docker nutzen."
                ),
            },
            {
                "id": "passwd_pal",
                "ziel": "Zeige Benutzer: cat /etc/passwd | head -5",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "cat"
                    and "passwd" in cmd
                ),
                "belohnung": "📜 Schriftrolle des Volkes",
                "lernziel": (
                    "/etc/passwd: name:x:uid:gid:info:home:shell. "
                    "Passwort-Hashes in /etc/shadow."
                ),
            },
            {
                "id": "group_pal",
                "ziel": "Zeige Gruppen-Datei: cat /etc/group | head -10",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "cat"
                    and "group" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Gemeinden",
                "lernziel": (
                    "/etc/group: gruppenname:x:gid:mitglieder. "
                    "sudo-Gruppe = Administrator."
                ),
            },
            {
                "id": "sudol_pal",
                "ziel": "Pruefe sudo-Rechte: sudo -l",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "sudo"
                    and len(cmd.split()) >= 2
                ),
                "belohnung": "📜 Schriftrolle der Macht",
                "lernziel": (
                    "sudo -l zeigt erlaubte sudo-Befehle. "
                    "sudo = 'super user do'. Nur mit sudo-Gruppe!"
                ),
            },
        ],
        "dateien": [
            {
                "dateiname": "benutzerhandbuch.txt",
                "inhalt": (
                    "Benutzerverwaltung:\n"
                    "• whoami - Aktueller Benutzer\n"
                    "• id - User-ID und Gruppen\n"
                    "• sudo BEFEHL - Als Root ausfuehren\n"
                    "• useradd NAME - Neuen Benutzer (root)\n"
                ),
            },
        ],
    },

    "bibliothekskeller": {
        "name": "Keller der Textzauberer",
        "emoji": "📜",
        "beschreibung": (
            "Im dunklen Keller der Textzauberer verarbeiten wir Texte mit mächtigen Werkzeugen: "
            "sort, uniq, cut, awk, sed und tr. "
            "Textzauberer Awk kennt alle Geheimnisse der Textverarbeitung."
        ),
        "ausgaenge": {
            "bibliothek": "Bibliothek",
        },
        "npc": {
            "name": "Textzauberer Awk",
            "bild": "🪬",
            "dialoge": [
                "Psst... ich bin Textzauberer Awk! 🪬 "
                "Hier unten im Keller verarbeiten wir Texte mit uralter Magie. "
                "Dein erster Zauber: sort bringt Ordnung ins Chaos. "
                "Sortiere namen.txt und staune über die Wirkung!",
                "Gut! Aber Vorsicht: uniq entfernt nur BENACHBARTE Duplikate "
                "– deshalb immer sort | uniq! 📜 "
                "Und cut schneidet Spalten heraus: cut -d',' -f1 liest das erste Feld einer CSV-Datei. "
                "Meistere die Grundzauber!",
                "Jetzt zur Hochmagie! awk verarbeitet Felder: $1 ist das erste Feld, $NF das letzte. 🪬 "
                "sed ersetzt Text mit s/ALT/NEU/g. "
                "Und tr wandelt Zeichen um: a-z in A-Z für Großbuchstaben "
                "– mächtig und präzise!",
                "MEISTERHAFT! 🪬 Du beherrschst alle Textzauber: "
                "sort|uniq für Duplikate, cut für CSV-Spalten, awk für Feldverarbeitung, "
                "sed für Textersetzung, tr für Zeichenwandlung. "
                "Die Meister-Pipeline verbindet alles zu einem Werk! "
                "Du bist nun Textzauberer des Kellerlabors!",
            ],
        },
        "ascii_art": [
            "  ~~~~ KELLER der TEXTE ~~~~  ",
            "  | 📜   Runen und Magie   |  ",
            "  | ░░ sort | uniq | awk ░░|  ",
            "  | ░░  sed  |  tr | cut ░░|  ",
            "  |_________________________|  ",
            "   ~~ Awk beobachtet dich ~~  ",
        ],
        "quests": [
            {
                "id": "sort_kell",
                "ziel": "Sortiere Namen: sort namen.txt",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "sort"
                    and len(cmd.split()) >= 2
                ),
                "belohnung": "📜 Schriftrolle der Ordnung",
                "lernziel": (
                    "sort sortiert alphabetisch. "
                    "-r=umgekehrt, -n=numerisch, -k 2=nach Spalte 2."
                ),
            },
            {
                "id": "uniq_kell",
                "ziel": "Entferne Duplikate: sort namen.txt | uniq",
                "check": lambda cmd, out, p: "uniq" in cmd,
                "belohnung": "📜 Schriftrolle der Einzigartigkeit",
                "lernziel": (
                    "uniq entfernt BENACHBARTE Duplikate. "
                    "Immer: sort | uniq. uniq -c zaehlt Vorkommnisse."
                ),
            },
            {
                "id": "cut_kell",
                "ziel": "Schneide Spalte: cut -d',' -f1 daten.csv",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "cut"
                    and "-d" in cmd
                ),
                "belohnung": "📜 Schriftrolle des Schnitts",
                "lernziel": (
                    "cut -d',' -f1 = Trennzeichen Komma, Feld 1. "
                    "Perfekt fuer CSV-Dateien."
                ),
            },
            {
                "id": "awk_kell",
                "ziel": "Drucke Spalte: awk '{print $1}' namen.txt",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "awk"
                ),
                "belohnung": "📜 Schriftrolle der Felder",
                "lernziel": (
                    "awk verarbeitet strukturierten Text. "
                    "$1=Feld1, $NF=letztes Feld. Sehr maechtig!"
                ),
            },
            {
                "id": "sed_kell",
                "ziel": "Ersetze Text: sed 's/Anna/Mia/g' namen.txt",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "sed"
                ),
                "belohnung": "📜 Schriftrolle des Wandels",
                "lernziel": (
                    "sed 's/SUCHE/ERSATZ/g' ersetzt alle Vorkommen. "
                    "sed -i fuer direkte Dateibearbeitung."
                ),
            },
            {
                "id": "tr_kell",
                "ziel": "Grossbuchstaben: cat namen.txt | tr 'a-z' 'A-Z'",
                "check": lambda cmd, out, p: (
                    "tr" in cmd
                    and ("a-z" in cmd or "A-Z" in cmd)
                ),
                "belohnung": "📜 Schriftrolle der Verwandlung",
                "lernziel": (
                    "tr = translate characters. "
                    "tr -d loescht Zeichen. tr -s quetscht Wiederholungen."
                ),
            },
            {
                "id": "pipeline_kell",
                "ziel": (
                    "Meister-Pipeline: "
                    "cat daten.csv | cut -d',' -f1 | sort | uniq -c | sort -rn"
                ),
                "check": lambda cmd, out, p: (
                    "|" in cmd
                    and len([c for c in cmd.split("|") if c.strip()]) >= 3
                ),
                "belohnung": "📜 Schriftrolle der Meisterschaft",
                "lernziel": (
                    "Pipes kombinieren zu maechtigem Workflow. "
                    "Dieses Muster sortiert und zaehlt Haeufigkeiten!"
                ),
            },
        ],
        "dateien": [
            {
                "dateiname": "namen.txt",
                "inhalt": (
                    "Anna\nBernd\nClara\nAnna\n"
                    "Dieter\nBernd\nEva\nAnna\n"
                ),
            },
            {
                "dateiname": "daten.csv",
                "inhalt": (
                    "Anna,25,Berlin\n"
                    "Bernd,30,Hamburg\n"
                    "Clara,28,Berlin\n"
                    "Dieter,35,Muenchen\n"
                ),
            },
        ],
    },

    "garten": {
        "name": "Garten der Verknuepfungen",
        "emoji": "🌸",
        "beschreibung": (
            "Im Garten der Verknüpfungen wachsen symbolische Links wie Blumen. "
            "Gärtnerin Fiona zeigt dir ln, find mit verschiedenen Optionen "
            "und du – Werkzeuge für erweiterte Dateioperationen."
        ),
        "ausgaenge": {
            "markt": "Markt",
            "bibliothekskeller": "Keller der Textzauberer",
        },
        "npc": {
            "name": "Gaertnerin Fiona",
            "bild": "🌺",
            "dialoge": [
                "Willkommen in meinem Garten! 🌺 "
                "Ich bin Fiona, und hier wachsen Verknüpfungen wie Blumen. "
                "ln -s erstellt symbolische Links – wie Wegweiser zu Dateien. "
                "Dann zeige sie mit ls -la und entdecke den Pfeil (->)!",
                "Wunderschön! 🌸 Jetzt erkunde deinen Garten mit find. "
                "find -type f findet nur Dateien, -size +1k findet große Dateien, "
                "-mtime -1 findet frisch geänderte. "
                "Jede Option ist eine andere Spur durch den Garten!",
                "Dein Garten blüht! 🌺 "
                "Das große Wissen: ln -s für symbolische Links (Änderungen wirken auf beide!), "
                "ls -la zeigt Pfeile (->), find -type/-size/-mtime für gezielte Suche, "
                "du -sh für Größencheck. "
                "Mit diesen Werkzeugen verlierst du dich nie mehr im Dateisystem!",
            ],
        },
        "ascii_art": [
            "    🌸      GARTEN      🌸    ",
            "  🌺 . 🌿 . 🌼 . 🌿 . 🌼 . 🌺  ",
            "  | 🌳   Verknuepfungen  🌳 |  ",
            "  |    find  .  ln  .  du  |  ",
            "   \\_______________________/  ",
            "    🌸    Willkommen!    🌸   ",
        ],
        "quests": [
            {
                "id": "symlink_gar",
                "ziel": "Erstelle Symlink: ln -s preisliste.txt preis_link.txt",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "ln"
                    and "-s" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Verbindung",
                "lernziel": (
                    "ln -s = symbolischer Link (Verknuepfung). "
                    "Aenderungen wirken auf beide!"
                ),
            },
            {
                "id": "lsla_gar",
                "ziel": "Sieh den Symlink: ls -la",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "ls"
                    and "-la" in cmd
                ),
                "belohnung": "📜 Schriftrolle des Zeigers",
                "lernziel": (
                    "ls -la zeigt Symlinks mit -> Ziel. "
                    "l am Anfang der Rechte = Link."
                ),
            },
            {
                "id": "findtype_gar",
                "ziel": "Finde Dateien: find . -type f",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "find"
                    and "-type" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Dateien",
                "lernziel": (
                    "find -type f = nur Dateien, "
                    "-type d = nur Ordner, -type l = nur Links."
                ),
            },
            {
                "id": "findsize_gar",
                "ziel": "Finde grosse Dateien: find . -size +1k",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "find"
                    and "-size" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Masse",
                "lernziel": (
                    "find -size +1k = groesser als 1 Kilobyte. "
                    "+1M = groesser 1MB. c=Bytes, k=KB, M=MB."
                ),
            },
            {
                "id": "findmtime_gar",
                "ziel": "Finde neue Dateien: find . -mtime -1",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "find"
                    and "-mtime" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Neuheit",
                "lernziel": (
                    "find -mtime -1 = letzten 24h geaendert. "
                    "-mtime +7 = aelter als 7 Tage."
                ),
            },
            {
                "id": "du_gar",
                "ziel": "Groesse anzeigen: du -sh .",
                "check": lambda cmd, out, p: (
                    bool(cmd.split())
                    and cmd.split()[0] == "du"
                ),
                "belohnung": "📜 Schriftrolle der Totalgroesse",
                "lernziel": (
                    "du -sh . = Groesse aktueller Ordner. "
                    "du -sh * = jedes Element. Unverzichtbar bei Platzmangel!"
                ),
            },
        ],
        "dateien": [
            {
                "dateiname": "gartenbuch.txt",
                "inhalt": (
                    "Erweiterte Dateioperationen:\n"
                    "ln -s = Symlink\n"
                    "find -type f = nur Dateien\n"
                    "find -size +1k = nach Groesse\n"
                    "du -sh = Ordnergroesse\n"
                ),
            },
        ],
    },
    "fernwelt": {
        "name":        "Fernwelt-Portal",
        "emoji":       "🌐",
        "beschreibung": (
            "Ein schimmerndes Portal oeffnet sich vor dir – ein Tor zu einem echten\n"
            "Linux-Server weit entfernt. SSH (Secure Shell) ist dein Schluesselbegriff:\n"
            "Du tippst einen Befehl und landest in einer Shell auf einem anderen Rechner!\n\n"
            "So funktioniert es:\n"
            "  1. Tippe:  ssh mia@152.53.225.236   → SSH-Modus startet\n"
            "  2. Du siehst:  mia@server:~$        → du bist JETZT auf dem Server!\n"
            "  3. Tippe Befehle wie gewohnt (ls, mkdir, cd ...)\n"
            "  4. Tippe:  exit                     → zurueck ins Koenigreich\n\n"
            "Tipp: Tippe  sshhilfe  fuer eine Uebersicht!"
        ),
        "ausgaenge": {"hafen": "Hafen", "schluesselschmiede": "Schlüsselschmiede", "zeituhr": "Zeituhr", "webwerkstatt": "Webwerkstatt"},
        "npc": {
            "name": "Vera",
            "bild": "🌐",
            "dialoge": [
                "Willkommen am Fernwelt-Portal! Ich bin Vera, Waerchterin der Verbindungen.\n\n"
                "SSH bedeutet: Secure Shell – eine verschluesselte Verbindung zu einem\n"
                "anderen Linux-Rechner. So verbindest du dich:\n\n"
                "  Schritt 1: Tippe  ssh mia@152.53.225.236\n"
                "  Schritt 2: Du siehst  mia@152.53.225.236:~$  – du bist drin!\n"
                "  Schritt 3: Tippe Befehle auf dem Server (ls, mkdir, ...)\n"
                "  Schritt 4: Tippe  exit  um zurueckzukehren\n\n"
                "Probier es aus! Tippe: sshhilfe  fuer mehr Tipps.",
                "Super! Im SSH-Modus (wenn du  mia@server:~$  siehst) kannst du:\n\n"
                "  ls           – Dateien auf dem Server anzeigen\n"
                "  mkdir website  – Ordner erstellen\n"
                "  pwd          – aktuellen Pfad anzeigen\n"
                "  exit         – zurueck ins Spiel\n\n"
                "Merke: Alles was du dort tippst, laeuft auf dem echten Server!",
                "Jetzt lernst du SCP – Secure Copy. Dateien senden:\n\n"
                "  Schritt 1: Erstelle lokal eine HTML-Datei (du bist NICHT im SSH-Modus):\n"
                "    echo '<h1>Hallo Welt!</h1>' > index.html\n\n"
                "  Schritt 2: Sende sie auf den Server:\n"
                "    scp index.html mia@152.53.225.236:~/website/\n\n"
                "SCP-Format: scp LOKALE-DATEI user@server:ZIELPFAD",
                "Fast geschafft! Starte jetzt den Webserver:\n\n"
                "  Schritt 1: Verbinde dich nochmal:  ssh mia@152.53.225.236\n"
                "  Schritt 2: Wechsle in den Ordner:  cd website\n"
                "  Schritt 3: Starte Server:           python3 -m http.server 8080 &\n"
                "  Schritt 4: Tippe  exit  und dann:\n"
                "             curl http://152.53.225.236:8080\n\n"
                "Das & am Ende laesst den Server im Hintergrund laufen!",
                "Hervorragend! SSH, SCP, Webserver – das ist echte Server-Arbeit!\n"
                "Jeder DevOps-Engineer, jeder Admin, jeder Webentwickler\n"
                "benutzt genau diese Werkzeuge taeglich.\n"
                "Erkunde jetzt die Schluesselschmiede und die Zeituhr!",
            ],
        },
        "quests": [
            {
                "id":       "ssh_connect",
                "modus":    "lokal",
                "ziel":     "ssh mia@152.53.225.236",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "ssh" and "@" in cmd,
                "belohnung":"🌐 Schriftrolle der Fernverbindung",
                "lernziel": "SSH = Secure Shell. Einloggen auf Remote-Server. Standard in der Linux-Welt!",
            },
            {
                "id":       "remote_ls",
                "modus":    "ssh",
                "ziel":     "ls",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "ls" and getattr(p, "in_ssh", False),
                "belohnung":"🌐 Schriftrolle des Fernblicks",
                "lernziel": "ls funktioniert auf jedem Linux-Server gleich. Jetzt laeuft es remote!",
            },
            {
                "id":       "remote_mkdir",
                "modus":    "ssh",
                "ziel":     "mkdir website",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "mkdir" and getattr(p, "in_ssh", False),
                "belohnung":"🌐 Schriftrolle des Fernordners",
                "lernziel": "mkdir auf einem Remote-Server – dein erster eigener Webspace-Ordner!",
            },
            {
                "id":       "create_html",
                "modus":    "lokal",
                "ziel":     "echo '<h1>Hallo Welt!</h1>' > index.html",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "echo" and ".html" in cmd and ">" in cmd,
                "belohnung":"🌐 Schriftrolle des Webs",
                "lernziel": "HTML = HyperText Markup Language. Die Sprache des Webs! Jede Website beginnt mit <h1>.",
            },
            {
                "id":       "scp_upload",
                "modus":    "lokal",
                "ziel":     "scp index.html mia@152.53.225.236:~/website/",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "scp" and ".html" in cmd,
                "belohnung":"🌐 Schriftrolle des Transports",
                "lernziel": "SCP = Secure Copy. Wie cp, aber ueber SSH. Format: scp QUELLE user@host:ZIEL",
            },
            {
                "id":       "start_server",
                "modus":    "ssh",
                "ziel":     "cd website && python3 -m http.server 8080 &",
                "check":    lambda cmd, out, p: "http.server" in cmd and "8080" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"🌐 Schriftrolle des Servers",
                "lernziel": "python3 -m http.server PORT startet sofort einen Webserver. & = laeuft im Hintergrund.",
            },
            {
                "id":       "web_check",
                "modus":    "lokal",
                "ziel":     "curl http://152.53.225.236:8080",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "curl" and "8080" in cmd,
                "belohnung":"🌐 Schriftrolle des World Wide Web",
                "lernziel": "curl macht HTTP-Requests. Deine erste selbst gehostete Webseite ist live!",
            },
        ],
    },
    "schluesselschmiede": {
        "name":        "Schlüsselschmiede",
        "emoji":       "🔑",
        "beschreibung": (
            "Eine geheimnisvolle Werkstatt, in der magische Schluessel geschmiedet werden.\n"
            "Schluesselmeister Klaus lehrt dich SSH-Key-Authentifizierung –\n"
            "das Ende von Passwoertern! Mit einem Schluesselpaar loggst du dich\n"
            "auf jedem Server ein, ohne je ein Passwort tippen zu muessen."
        ),
        "ausgaenge": {"fernwelt": "Fernwelt-Portal"},
        "npc": {
            "name": "Klaus",
            "bild": "🔑",
            "dialoge": [
                "Willkommen in meiner Schmiede! Ich bin Schluesselmeister Klaus.\n"
                "Passwoerter sind gefaehrlich – ein Schluessel ist viel sicherer!\n"
                "Starte mit: ssh-keygen -t ed25519\n"
                "Das erstellt ein Schluesselpaar: privat (geheim) + oeffentlich (teilbar).",
                "Gut! Dein Schluessel liegt in ~/.ssh/\n"
                "Sieh dir den oeffentlichen Schluessel an:\n"
                "cat ~/.ssh/id_ed25519.pub\n"
                "Dieser kann bedenkenlos weitergegeben werden!",
                "Jetzt kopieren wir den Schluessel auf den Server.\n"
                "Das Spiel erledigt ssh-copy-id automatisch fuer dich.\n"
                "Tippe einfach: ssh-copy-id mia@152.53.225.236",
                "Fantastisch! Ab jetzt kein Passwort mehr!\n"
                "Teste es: ssh mia@152.53.225.236\n"
                "Du wirst direkt eingeloggt – ohne Passwort!",
                "Meisterhaft! Du kennst jetzt Public-Key-Authentifizierung.\n"
                "So funktioniert GitHub, jeder Cloud-Server, alles!\n"
                "Der private Schluessel bleibt NUR bei dir. Nie weitergeben!",
            ],
        },
        "quests": [
            {
                "id":       "keygen",
                "modus":    "lokal",
                "ziel":     "ssh-keygen -t ed25519",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "ssh-keygen" and "ed25519" in cmd,
                "belohnung":"🔑 Schriftrolle des Schluessels",
                "lernziel": "ssh-keygen erstellt privaten + oeffentlichen Schluessel. -t ed25519 = moderner Algorithmus.",
            },
            {
                "id":       "cat_pubkey",
                "modus":    "lokal",
                "ziel":     "cat ~/.ssh/id_ed25519.pub",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "cat" and "id_ed25519.pub" in cmd,
                "belohnung":"🔑 Schriftrolle des Oeffentlichen",
                "lernziel": "Der oeffentliche Schluessel (.pub) darf auf Server kopiert werden. Der private bleibt geheim!",
            },
            {
                "id":       "ssh_copy_id",
                "modus":    "lokal",
                "ziel":     "ssh-copy-id mia@152.53.225.236",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "ssh-copy-id",
                "belohnung":"🔑 Schriftrolle der Installation",
                "lernziel": "ssh-copy-id schreibt deinen Schluessel in ~/.ssh/authorized_keys auf dem Server.",
            },
            {
                "id":       "ssh_nopasswd",
                "modus":    "lokal",
                "ziel":     "ssh mia@152.53.225.236",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "ssh" and "@" in cmd,
                "belohnung":"🔑 Schriftrolle der Freiheit",
                "lernziel": "Public-Key-Auth: Server prueft ob dein privater Schluessel zum installierten passt. Kein Passwort!",
            },
            {
                "id":       "ls_ssh_dir",
                "modus":    "lokal",
                "ziel":     "ls -la ~/.ssh/",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "ls" and ".ssh" in cmd,
                "belohnung":"🔑 Schriftrolle des Gewölbes",
                "lernziel": "~/.ssh/ enthaelt: id_ed25519 (privat!), id_ed25519.pub, known_hosts, authorized_keys.",
            },
        ],
    },
    "zeituhr": {
        "name":        "Zeituhr der Automatik",
        "emoji":       "⏰",
        "beschreibung": (
            "Eine riesige magische Uhr, deren Zahnraeder niemals stillstehen.\n"
            "Chronistin Hora lehrt dich crontab – das Planen automatischer Aufgaben.\n"
            "Befehle, die jede Minute, Stunde oder Nacht automatisch ausgefuehrt werden.\n"
            "Das Herzstuck jeder Server-Automatisierung!"
        ),
        "ausgaenge": {"fernwelt": "Fernwelt-Portal"},
        "npc": {
            "name": "Hora",
            "bild": "⏰",
            "dialoge": [
                "Willkommen an der Zeituhr! Ich bin Chronistin Hora.\n"
                "Crontab plant Befehle die automatisch laufen – ohne dass du dabei sein musst!\n"
                "Verbinde dich zuerst per SSH, dann schau was geplant ist:\n"
                "Tippe im SSH-Modus: crontab -l",
                "Das Crontab-Format ist: Minute Stunde Tag Monat Wochentag Befehl\n"
                "* * * * *  = jede Minute. 0 * * * * = jede volle Stunde.\n"
                "Erstelle deinen ersten Job (in SSH-Modus):\n"
                "echo '* * * * * date >> ~/zeitlog.txt' | crontab -",
                "Hervorragend! Jetzt liste deine geplanten Jobs auf:\n"
                "crontab -l\n"
                "Du siehst deinen neuen Eintrag. Der laeuft jetzt jede Minute!",
                "Lies die automatisch erstellten Logs:\n"
                "sleep 65 && cat ~/zeitlog.txt\n"
                "Oder pruefe direkt: ls -la ~/zeitlog.txt",
                "Du hast crontab gemeistert! Das nutzen Admins fuer:\n"
                "Backups, Log-Rotation, Monitoring, automatische Updates.\n"
                "Entferne alle Jobs wieder mit: crontab -r",
            ],
        },
        "quests": [
            {
                "id":       "crontab_list",
                "modus":    "ssh",
                "ziel":     "crontab -l",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "crontab" and "-l" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"⏰ Schriftrolle der Zeit",
                "lernziel": "crontab -l = list. Zeigt alle geplanten automatischen Aufgaben des aktuellen Benutzers.",
            },
            {
                "id":       "crontab_add",
                "modus":    "ssh",
                "ziel":     "echo '* * * * * date >> ~/zeitlog.txt' | crontab -",
                "check":    lambda cmd, out, p: "crontab" in cmd and "|" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"⏰ Schriftrolle der Planung",
                "lernziel": "Format: MIN STD TAG MON WTAG BEFEHL. * = jeder Wert. | crontab - = direkt setzen ohne Editor.",
            },
            {
                "id":       "crontab_verify",
                "modus":    "ssh",
                "ziel":     "crontab -l",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "crontab" and "-l" in cmd and getattr(p, "in_ssh", False) and "crontab_add" in p.abschluss,
                "belohnung":"⏰ Schriftrolle der Bestaetigung",
                "lernziel": "Immer nach Aenderungen crontab -l zur Kontrolle! Syntaxfehler verhindern die Ausfuehrung.",
            },
            {
                "id":       "crontab_log",
                "modus":    "ssh",
                "ziel":     "cat ~/zeitlog.txt",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "cat" and "zeitlog" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"⏰ Schriftrolle des Beweises",
                "lernziel": ">> leitet Ausgabe an eine Datei an. So sammeln Cronjobs ihre Ergebnisse in Log-Dateien.",
            },
            {
                "id":       "crontab_remove",
                "modus":    "ssh",
                "ziel":     "crontab -r",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "crontab" and "-r" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"⏰ Schriftrolle der Ordnung",
                "lernziel": "crontab -r entfernt ALLE Jobs! crontab -e oeffnet den Editor zum gezielten Bearbeiten.",
            },
        ],
    },
    "webwerkstatt": {
        "name":        "Web-Werkstatt",
        "emoji":       "💻",
        "beschreibung": (
            "Eine leuchtende Werkstatt voller schwebender HTML-Tags und bunter CSS-Farben.\n"
            "Web-Zauberin Lyra lehrt dich, eine echte Website auf dem Server aufzubauen.\n"
            "Du schreibst jedes Element mit echo direkt auf den Server –\n"
            "und siehst das Ergebnis live im Browser!"
        ),
        "ausgaenge": {"fernwelt": "Fernwelt-Portal", "deploymeisterei": "Deploymeisterei"},
        "npc": {
            "name": "Lyra",
            "bild": "💻",
            "dialoge": [
                "Willkommen in der Web-Werkstatt! Ich bin Lyra, Web-Zauberin.\n"
                "Wir bauen eine echte HTML-Seite auf deinem Server – Element fuer Element!\n"
                "Verbinde dich zuerst per SSH, dann:\n"
                "echo '<!DOCTYPE html>' > ~/website/index.html",
                "Gut! Jetzt der HTML-Rahmen:\n"
                "echo '<html><head><title>Mia Linux</title></head><body>' >> ~/website/index.html\n"
                "Das >> haengt an ohne zu loeschen – das kennst du schon!",
                "Eine Ueberschrift macht jede Seite lebendig:\n"
                "echo '<h1>Willkommen auf Mias Linux-Server!</h1>' >> ~/website/index.html\n"
                "h1 = groesste Ueberschrift. h2 bis h6 werden kleiner.",
                "Jetzt ein Absatz und eine Liste:\n"
                "echo '<p>Gelernte Befehle:</p>' >> ~/website/index.html\n"
                "echo '<ul><li>SSH</li><li>SCP</li><li>crontab</li></ul>' >> ~/website/index.html",
                "Ein Link zur naechsten Seite:\n"
                "echo '<a href=\"about.html\">Ueber mich</a>' >> ~/website/index.html\n"
                "echo '</body></html>' >> ~/website/index.html",
                "Jetzt etwas Farbe mit CSS! Erstelle eine Stylesheet-Datei:\n"
                "echo 'body{font-family:sans-serif;background:#1a1a2e;color:white;}' > ~/website/style.css\n"
                "echo 'h1{color:#53c8ff;}a{color:#ff9f43;}' >> ~/website/style.css",
                "Verknuepfe CSS mit HTML – fuege den link-Tag in den head ein:\n"
                "Das machst du mit sed direkt auf dem Server:\n"
                "sed -i 's|</head>|<link rel=\"stylesheet\" href=\"style.css\"></head>|' ~/website/index.html",
                "Sieh dir das fertige Ergebnis an:\n"
                "curl http://152.53.225.236:8080\n"
                "Du siehst den rohen HTML-Code – im Browser sieht es noch viel besser aus!",
                "Fantastisch! Du hast eine vollstaendige Website gebaut!\n"
                "HTML fuer Struktur, CSS fuer Aussehen – das sind die Grundlagen des Webs.\n"
                "Oeffne http://152.53.225.236:8080 im Browser um sie live zu sehen!",
            ],
        },
        "quests": [
            {
                "id":       "html_doctype",
                "modus":    "ssh",
                "ziel":     "echo '<!DOCTYPE html>' > ~/website/index.html",
                "check":    lambda cmd, out, p: "DOCTYPE" in cmd and "index.html" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"💻 Schriftrolle des Dokumenttyps",
                "lernziel": "<!DOCTYPE html> sagt dem Browser: das ist HTML5. Muss die ERSTE Zeile jeder HTML-Datei sein.",
            },
            {
                "id":       "html_frame",
                "modus":    "ssh",
                "ziel":     "echo '<html><head><title>Mia Linux</title></head><body>' >> ~/website/index.html",
                "check":    lambda cmd, out, p: "<html>" in cmd and "<title>" in cmd and ">>" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"💻 Schriftrolle der Struktur",
                "lernziel": "html umschliesst alles. head = unsichtbare Infos (Titel, CSS). body = sichtbarer Inhalt.",
            },
            {
                "id":       "html_h1",
                "modus":    "ssh",
                "ziel":     "echo '<h1>Willkommen!</h1>' >> ~/website/index.html",
                "check":    lambda cmd, out, p: "<h1>" in cmd and ">>" in cmd and "index.html" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"💻 Schriftrolle der Ueberschrift",
                "lernziel": "h1 = groesste Ueberschrift. h2-h6 werden kleiner. Jede Seite sollte genau ein h1 haben.",
            },
            {
                "id":       "html_paragraph",
                "modus":    "ssh",
                "ziel":     "echo '<p>Gelernte Befehle:</p>' >> ~/website/index.html",
                "check":    lambda cmd, out, p: "<p>" in cmd and ">>" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"💻 Schriftrolle des Absatzes",
                "lernziel": "p = paragraph = Absatz. Block-Element mit Abstand oben und unten.",
            },
            {
                "id":       "html_list",
                "modus":    "ssh",
                "ziel":     "echo '<ul><li>SSH</li><li>SCP</li></ul>' >> ~/website/index.html",
                "check":    lambda cmd, out, p: "<ul>" in cmd and "<li>" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"💻 Schriftrolle der Liste",
                "lernziel": "ul = unordered list (Punkte). ol = ordered list (Zahlen). li = list item.",
            },
            {
                "id":       "html_link",
                "modus":    "ssh",
                "ziel":     "echo '<a href=\"about.html\">Ueber mich</a>' >> ~/website/index.html",
                "check":    lambda cmd, out, p: "<a " in cmd and "href" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"💻 Schriftrolle der Verbindung",
                "lernziel": "a = anchor = Link. href = hypertext reference. Das Grundprinzip des Internets!",
            },
            {
                "id":       "html_close",
                "modus":    "ssh",
                "ziel":     "echo '</body></html>' >> ~/website/index.html",
                "check":    lambda cmd, out, p: "</body>" in cmd and "</html>" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"💻 Schriftrolle des Abschlusses",
                "lernziel": "Jedes oefffnende Tag braucht ein schliessendes. </body> und </html> beenden das Dokument.",
            },
            {
                "id":       "css_create",
                "modus":    "ssh",
                "ziel":     "echo 'body{background:#1a1a2e;color:white;}' > ~/website/style.css",
                "check":    lambda cmd, out, p: "style.css" in cmd and "background" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"💻 Schriftrolle des Stils",
                "lernziel": "CSS = Cascading Style Sheets. Selektor{Eigenschaft:Wert;} gibt Elementen Farbe und Form.",
            },
            {
                "id":       "css_link",
                "modus":    "ssh",
                "ziel":     "sed -i 's|</head>|<link rel=\"stylesheet\" href=\"style.css\"></head>|' ~/website/index.html",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "sed" and "style.css" in cmd and getattr(p, "in_ssh", False),
                "belohnung":"💻 Schriftrolle der Verknuepfung",
                "lernziel": "sed -i ersetzt Text direkt in der Datei. Der link-Tag laedt das CSS in den Browser.",
            },
            {
                "id":       "curl_html",
                "modus":    "lokal",
                "ziel":     "curl http://152.53.225.236:8080",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "curl" and "8080" in cmd,
                "belohnung":"💻 Schriftrolle der Meisterin",
                "lernziel": "curl zeigt den HTML-Quellcode. Im Browser sieht es mit CSS visuell aus. Oeffne die URL!",
            },
        ],
    },
    "deploymeisterei": {
        "name":        "Deploymeisterei",
        "emoji":       "🚀",
        "beschreibung": (
            "Die Deploymeisterei ist das Ziel jeder Web-Entwicklerin!\n"
            "Hier lernst du den echten Workflow: design → edit → deploy → check → repeat.\n"
            "Du designst deine eigene Seite mit nano, schreibst ein Deploy-Skript\n"
            "und kannst deine Website mit einem einzigen Befehl live schalten!"
        ),
        "ausgaenge": {"webwerkstatt": "Webwerkstatt"},
        "npc": {
            "name": "Aria",
            "bild": "🚀",
            "dialoge": [
                "Willkommen in der Deploymeisterei! Ich bin Aria, Deploy-Meisterin.\n"
                "Du hast HTML und CSS gelernt – jetzt lernst du den echten Workflow!\n"
                "Starte mit deiner eigenen Seite: nano index.html\n"
                "Schreib was du willst – Titel, Texte, Links. Deine Kreativitaet!",
                "Gut! Jetzt deploy sie auf den Server:\n"
                "scp index.html mia@152.53.225.236:~/website/\n"
                "Und check das Ergebnis: curl http://152.53.225.236:8080",
                "Echter Workflow: aendere jetzt etwas an deiner Seite!\n"
                "Nutze sed um einen Text zu ersetzen:\n"
                "sed -i 's/Willkommen/Hallo Welt/g' index.html\n"
                "Dann nochmal deployen und pruefen!",
                "Jetzt automatisieren wir das Deploy!\n"
                "Erstelle ein Skript: nano deploy.sh\n"
                "Inhalt: #!/bin/bash\\nscp index.html mia@152.53.225.236:~/website/\\necho 'Deployed!'",
                "Mache es ausfuehrbar und starte es:\n"
                "chmod +x deploy.sh\n"
                "./deploy.sh\n"
                "Ab jetzt: eine Aenderung, ein Befehl – fertig deployed!",
                "Du bist eine echte Web-Entwicklerin!\n"
                "Genau so arbeiten echte Teams: edit → git push → deploy script.\n"
                "Deine Website ist live auf einem echten Server. Das ist REAL!",
            ],
        },
        "quests": [
            {
                "id":       "nano_eigene_seite",
                "modus":    "lokal",
                "ziel":     "nano index.html",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "nano" and "index.html" in cmd,
                "belohnung":"🚀 Schriftrolle des Designs",
                "lernziel": "nano oeffnet den Editor. Schreib eigenes HTML! Strg+O speichert, Strg+X beendet.",
            },
            {
                "id":       "deploy_v1",
                "modus":    "lokal",
                "ziel":     "scp index.html mia@152.53.225.236:~/website/",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "scp" and "index.html" in cmd,
                "belohnung":"🚀 Schriftrolle des ersten Deploys",
                "lernziel": "scp = Secure Copy. Jedes Mal wenn du deployst, ersetzt du die alte Version auf dem Server.",
            },
            {
                "id":       "check_v1",
                "modus":    "lokal",
                "ziel":     "curl http://152.53.225.236:8080",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "curl" and "8080" in cmd and "deploy_v1" in p.abschluss,
                "belohnung":"🚀 Schriftrolle der Kontrolle",
                "lernziel": "Nach jedem Deploy pruefen! curl ist schnell. Oder oeffne http://152.53.225.236:8080 im Browser.",
            },
            {
                "id":       "aendern_v2",
                "modus":    "lokal",
                "ziel":     "sed -i 's/ALTESTEXT/NEUESTEXT/g' index.html",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "sed" and "-i" in cmd and "index.html" in cmd,
                "belohnung":"🚀 Schriftrolle der Version 2",
                "lernziel": "sed -i aendert Dateien ohne Editor. Perfekt fuer schnelle Anpassungen im Deploy-Workflow.",
            },
            {
                "id":       "deploy_v2",
                "modus":    "lokal",
                "ziel":     "scp index.html mia@152.53.225.236:~/website/",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "scp" and "index.html" in cmd and "aendern_v2" in p.abschluss,
                "belohnung":"🚀 Schriftrolle des zweiten Deploys",
                "lernziel": "Edit → Deploy → Check → repeat. Das ist der Kern jeder Web-Entwicklung!",
            },
            {
                "id":       "deploy_script",
                "modus":    "lokal",
                "ziel":     "nano deploy.sh",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "nano" and "deploy.sh" in cmd,
                "belohnung":"🚀 Schriftrolle der Automatisierung",
                "lernziel": "Skripte automatisieren wiederkehrende Aufgaben. Inhalt: #!/bin/bash + scp-Befehl.",
            },
            {
                "id":       "chmod_deploy",
                "modus":    "lokal",
                "ziel":     "chmod +x deploy.sh",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "chmod" and "+x" in cmd and "deploy.sh" in cmd,
                "belohnung":"🚀 Schriftrolle der Ausfuehrung",
                "lernziel": "chmod +x macht Skripte ausfuehrbar. Ohne +x: Permission denied!",
            },
            {
                "id":       "run_deploy",
                "modus":    "lokal",
                "ziel":     "./deploy.sh",
                "check":    lambda cmd, out, p: bool(cmd.split()) and cmd.split()[0] == "./deploy.sh",
                "belohnung":"🚀 Schriftrolle der Meisterin",
                "lernziel": "Ein Befehl, alles deployed. So arbeiten echte DevOps-Teams – nur mit mehr Schritten!",
            },
        ],
    },
}
GESAMT_QUESTS = sum(len(r.get('quests', [])) for r in RAEUME.values())


# ── Spielzustand ───────────────────────────────────────────────────────────────
class Spiel:
    def __init__(self, basis: Path, spielerin: str):
        self.basis      = basis
        self.spielerin  = spielerin
        self.aktuell    = basis / "dorf"
        self.scrolls    = []
        self.abschluss  = set()
        self.terminal   = []
        self.dialog_idx = {}
        self.in_ssh     = False  # True waehrend SSH-Modus aktiv
        self.ort_verlauf = []   # Raum-History fuer zurueck-Befehl

    def raum_id(self):
        name = self.aktuell.name
        return name if name in RAEUME else "dorf"

    def raum(self):
        return RAEUME[self.raum_id()]

    def speichern(self):
        try:
            save = {
                "scrolls":    self.scrolls,
                "abschluss":  list(self.abschluss),
                "dialog_idx": self.dialog_idx,
                "aktuell":    str(self.aktuell.relative_to(self.basis)),
            }
            (self.basis / ".save.json").write_text(json.dumps(save, indent=2))
        except Exception:
            pass

    def laden(self):
        savefile = self.basis / ".save.json"
        if savefile.exists():
            try:
                data = json.loads(savefile.read_text())
                self.scrolls    = data.get("scrolls", [])
                self.abschluss  = set(data.get("abschluss", []))
                self.dialog_idx = data.get("dialog_idx", {})
                rel = data.get("aktuell", "dorf")
                p   = (self.basis / rel).resolve()
                if p.exists():
                    self.aktuell = p
            except Exception:
                pass


# ── Bildschirm zeichnen ────────────────────────────────────────────────────────

def _aktive_quest(spiel: Spiel):
    for q in spiel.raum().get("quests", []):
        if q["id"] not in spiel.abschluss:
            return q
    return None

def zeige_bildschirm(spiel: Spiel, nachricht: str = '', zeige_dialog: bool = False):
    clr()
    raum   = spiel.raum()
    npc    = raum["npc"]
    kunst  = KUNST.get(spiel.raum_id(), KUNST["dorf"])

    total_quests = sum(len(r.get("quests", [])) for r in RAEUME.values())
    scrolls_str = f"📜 {len(spiel.scrolls)}/{total_quests}"
    pos_str     = raum["name"]

    # ── Kopfleiste ─────────────────────────────────────────────────────────────
    kopf   = c(f"  ⚔️  MIA'S LINUX-ABENTEUER  ", F.PINK + F.FETT)
    kopf_r = c(f"  {scrolls_str}   📍 {pos_str}  ", F.GELB)
    leer   = max(0, W - vis_len(kopf) - vis_len(kopf_r) - 2)
    print(c('╔' + '═' * (W - 2) + '╗', F.PINK))
    print(c('║', F.PINK) + kopf + ' ' * leer + kopf_r + c('║', F.PINK))
    print(c('╠' + '═' * (W - 2) + '╣', F.PINK))

    # ── Raum-Kunst (links) + Beschreibung (rechts) ─────────────────────────────
    kunst_b = 30
    info_b  = W - kunst_b - 3
    beschr  = textwrap.wrap(raum["beschreibung"], width=info_b - 2)
    max_z   = max(len(kunst), len(beschr) + 1)

    print(c('║', F.PINK) + c('─' * (W - 2), F.GRAU) + c('║', F.PINK))
    for i in range(max_z):
        k_z = kunst[i] if i < len(kunst) else ''
        if i == 0:
            d_z = c(f"  {raum['emoji']} {raum['name']}", F.FETT + F.GELB)
        elif i - 1 < len(beschr):
            d_z = c(f"  {beschr[i-1]}", F.WEISS)
        else:
            d_z = ''
        k_vis = vis_len(k_z)
        d_vis = vis_len(d_z)
        k_pad = k_z + ' ' * max(0, kunst_b - k_vis)
        d_pad = d_z + ' ' * max(0, info_b - d_vis)
        print(c('║', F.PINK) + ' ' + k_pad + c('│', F.GRAU) + d_pad + c('║', F.PINK))

    print(c('╠' + '═' * (W - 2) + '╣', F.PINK))

    # ── NPC-Dialog ─────────────────────────────────────────────────────────────
    if zeige_dialog:
        rid     = spiel.raum_id()
        d_idx   = spiel.dialog_idx.get(rid, 0)
        dialoge = npc["dialoge"]
        aktuell = dialoge[min(d_idx, len(dialoge) - 1)]
        d_text  = f"{npc['bild']} {npc['name']}: {aktuell}"
        for z in textwrap.wrap(d_text, width=W - 6):
            z_c = c(f"  {z}", F.CYAN)
            print(c('║', F.PINK) + z_c + ' ' * max(0, W - 2 - vis_len(z_c)) + c('║', F.PINK))
    else:
        # Zeige kompakten NPC-Hinweis
        npc_hint = c(f"  {npc['bild']} {npc['name']} ist hier. 'schau' um zu sprechen.", F.GRAU)
        print(c('║', F.PINK) + npc_hint + ' ' * max(0, W - 2 - vis_len(npc_hint)) + c('║', F.PINK))

    # ── Aktive Quest ───────────────────────────────────────────────────────────
    aktive = _aktive_quest(spiel)
    if aktive:
        modus = aktive.get("modus", "")
        if modus == "ssh":
            badge = c("  🖥️  IM SSH-MODUS TIPPEN  (ssh mia@server → mia@server:~$ → Befehl)", F.CYAN + F.FETT)
        elif modus == "lokal":
            badge = c("  💻  LOKAL TIPPEN  (KEIN SSH – normaler Prompt)", F.GRUEN + F.FETT)
        else:
            badge = None
        if badge:
            print(c('║', F.PINK) + badge + ' ' * max(0, W - 2 - vis_len(badge)) + c('║', F.PINK))
        q_c = c(f"  🎯 {aktive['ziel']}", F.GELB + F.FETT)
        print(c('║', F.PINK) + q_c + ' ' * max(0, W - 2 - vis_len(q_c)) + c('║', F.PINK))
    else:
        alle_done = all(q["id"] in spiel.abschluss for q in spiel.raum().get("quests", []))
        if alle_done and spiel.raum().get("quests"):
            d_c = c(f"  ✅ Alle Quests hier abgeschlossen! Erkunde andere Orte.", F.GRUEN)
            print(c('║', F.PINK) + d_c + ' ' * max(0, W - 2 - vis_len(d_c)) + c('║', F.PINK))
        else:
            print(c('║', F.PINK) + ' ' * (W - 2) + c('║', F.PINK))

    # ── Ausgänge ────────────────────────────────────────────────────────────────
    aug      = spiel.raum().get("ausgaenge", {})
    aug_str  = "  Ausgaenge: " + "   ".join(f"cd {k}" for k in aug)
    aug_c    = c(aug_str, F.GRAU)
    print(c('║', F.PINK) + aug_c + ' ' * max(0, W - 2 - vis_len(aug_c)) + c('║', F.PINK))

    # ── Terminal-Verlauf ────────────────────────────────────────────────────────
    print(c('╠' + '─' * (W - 2) + '╣', F.PINK))
    for cmd, out in spiel.terminal[-3:]:
        z = c(f"  $ {cmd}", F.GRUEN)
        print(c('║', F.PINK) + z + ' ' * max(0, W - 2 - vis_len(z)) + c('║', F.PINK))
        if out:
            for oz in out.splitlines()[:2]:
                oz_c = c(f"    {oz[:W-8]}", F.WEISS)
                print(c('║', F.PINK) + oz_c + ' ' * max(0, W - 2 - vis_len(oz_c)) + c('║', F.PINK))

    # ── Nachricht ───────────────────────────────────────────────────────────────
    if nachricht:
        print(c('╠' + '─' * (W - 2) + '╣', F.PINK))
        for z in textwrap.wrap(nachricht, width=W - 4):
            z_c = f"  {z}"
            print(c('║', F.PINK) + z_c + ' ' * max(0, W - 2 - len(z_c)) + c('║', F.PINK))

    # ── Prompt ─────────────────────────────────────────────────────────────────
    print(c('╠' + '═' * (W - 2) + '╣', F.PINK))
    try:
        rel = str(spiel.aktuell.relative_to(spiel.basis.parent))
    except ValueError:
        rel = spiel.aktuell.name
    print(c('║', F.PINK) + c(f"  ⚔️  {rel} $ ", F.GRUEN + F.FETT), end='', flush=True)


# ── Animationen ────────────────────────────────────────────────────────────────

def anim_reise(von: str, nach: str):
    schritte = ['·', '·>', '─>', '──>', '───>', '────▶']
    for i, pfeil in enumerate(schritte):
        clr()
        print()
        print(c(f"  🧙‍♀️  Mia reist ...", F.PINK + F.FETT))
        print()
        print(c(f"   {von:<15} {pfeil:<10} {nach}", F.GELB))
        time.sleep(0.18)
    clr()
    print()
    print(c(f"  ✨ Du betrittst: {nach}", F.GELB + F.FETT))
    time.sleep(0.5)

def anim_scroll(scroll_name: str):
    frames = [
        [],
        [c("      ╔═══════╗", F.GELB)],
        [c("      ╔═══════╗", F.GELB), c("      ║  📜   ║", F.GELB)],
        [c("      ╔═══════╗", F.GELB), c("      ║  📜   ║", F.GELB), c("      ╚═══════╝", F.GELB)],
        [c("  ✨✨✨✨✨✨✨✨✨✨  ", F.GELB + F.FETT),
         c(f"  SCHRIFTROLLE ERHALTEN!   ", F.GELB + F.FETT),
         c(f"  {scroll_name}", F.WEISS)],
    ]
    for frame in frames:
        clr()
        print()
        for z in frame:
            print(f"  {z}")
        time.sleep(0.4)
    time.sleep(0.8)

def anim_sieg():
    clr()
    print()
    sterne = ['·', '✦', '✦✦', '✦✦✦', '✦✦✦✦', '✦✦✦✦✦']
    for s in sterne:
        clr()
        print()
        print(c(f"  {s.center(W-4)}", F.GELB + F.FETT))
        time.sleep(0.2)

def anim_drachen_sieg(spiel: Spiel):
    """Epischer Boss-Sieg-Bildschirm fuer den Drachen."""
    clr()
    print()
    # Dramatische Drachen-Niederlage Animation
    frames = [
        c("  🐉 REMIRF greift an! ⚡", F.ROT + F.FETT),
        c("  ⚡ BLITZ trifft den Drachen! 🐉", F.GELB + F.FETT),
        c("  🐲 REMIRF brüllt vor Schmerz!", F.ROT + F.FETT),
        c("  ✨ Der Zauberbann wirkt...!", F.CYAN + F.FETT),
        c("  💥 DER DRACHE IST BESIEGT! 💥", F.GELB + F.FETT),
    ]
    for frame in frames:
        clr()
        print()
        print(f"  {frame}")
        time.sleep(0.6)

    time.sleep(0.5)
    clr()
    print()
    print(c('╔' + '═' * (W - 2) + '╗', F.ROT + F.FETT))
    print(c(f"║{'🐉  REMIRF IST BESIEGT!  🐉'.center(W-2)}║", F.ROT + F.FETT))
    print(c(f"║{'SIEG FUER BINARIA!'.center(W-2)}║", F.GELB + F.FETT))
    print(c('╠' + '═' * (W - 2) + '╣', F.ROT + F.FETT))
    print()
    langsam(f"{spiel.spielerin}! Du hast alle {GESAMT_QUESTS} Schriftrollen gesammelt!", F.PINK, 0.04)
    langsam("Den maechtigen Drachen Remirf besiegt!", F.ROT, 0.04)
    langsam("Das Koenigreich Binaria ist fuer immer gerettet!", F.WEISS, 0.03)
    print()

    print(c("  Deine Faehigkeiten als Linux-Herrscherin:", F.GELB + F.FETT))
    print()

    kategorien = [
        ("NAVIGATION",        ["ls", "pwd", "cd", "mkdir", "touch"]),
        ("DATEIEN",           ["cat", "echo", "cp", "mv", "rm"]),
        ("SUCHEN & PIPES",    ["grep", "find", "|", "wc"]),
        ("BERECHTIGUNGEN",    ["ls -l", "chmod", "chmod +x"]),
        ("PROZESSE",          ["ps", "ps aux", "sleep &", "jobs"]),
        ("PAKETE",            ["apt-cache search", "apt-cache show", "apt list"]),
        ("NETZWERK",          ["ping", "wget", "curl"]),
        ("EDITOR & SKRIPTE",  ["nano", "#!/bin/bash", "chmod +x", "./skript.sh"]),
    ]

    for kat, befehle in kategorien:
        print(c(f"  {kat}:", F.CYAN + F.FETT))
        print(c(f"    {', '.join(befehle)}", F.GRUEN))
        time.sleep(0.15)

    print()
    print(c('╠' + '═' * (W - 2) + '╣', F.GELB + F.FETT))
    print(c(f"║{'✨  DU BIST DIE WAHRE HERRSCHERIN VON BINARIA!  ✨'.center(W-2)}║", F.GELB + F.FETT))
    print(c('╚' + '═' * (W - 2) + '╝', F.GELB + F.FETT))
    print()
    print(c("  Spickzettel:  python3 mia_lernt_linux.py --spickzettel", F.GRAU))
    print(c("  Konzepte:     python3 mia_lernt_linux.py --konzept", F.GRAU))
    print()


# ── Dateisystem-Konzepterklärung ──────────────────────────────────────────────

def konzept_erklarung(spiel: 'Spiel | None' = None) -> str:
    """Gibt eine Erklärung des Dateisystems als String zurück."""
    b = spiel.basis if spiel else Path.home() / "linux_abenteuer"

    zeilen = [
        c("📚 DAS DATEISYSTEM – So funktioniert es:", F.GELB + F.FETT),
        "",
        c("  Denk dir den Computer wie ein riesiges Gebaeude vor:", F.WEISS),
        c("  Jeder Ordner ist ein Zimmer, jede Datei ist ein Dokument.", F.WEISS),
        "",
        c("  Dein Abenteuer-Ordner sieht so aus:", F.CYAN),
        "",
        c(f"  📦 {b.parent.name}/", F.GRAU) + c("                    <- Home-Verzeichnis", F.GRAU),
        c(f"  └── 📦 {b.name}/", F.WEISS) + c("             <- Unser Spielbereich", F.WEISS),
        c("       ├── 🏠 dorf/", F.GELB) + c("            <- Ordner (= Zimmer)", F.GRAU),
        c("       │   └── 📄 aushang.txt", F.WEISS) + c("  <- Datei (= Dokument)", F.GRAU),
        c("       ├── 🌲 wald/", F.GRUEN) + c("            <- noch ein Ordner", F.GRAU),
        c("       │   └── 📦 hoehle/", F.CYAN) + c("       <- Ordner im Ordner!", F.GRAU),
        c("       ├── 🌊 see/", F.BLAU),
        c("       ├── 🏪 markt/", F.GELB),
        c("       ├── 📚 bibliothek/", F.BRAUN),
        c("       ├── ⚗️  labor/", F.CYAN),
        c("       ├── 🏰 festung/", F.GRAU),
        c("       ├── ⛰️  bergpass/", F.BLAU),
        c("       ├── ⚓ hafen/", F.BLAU),
        c("       ├── 🗼 turm/", F.PINK),
        c("       └── 🐉 drachenfestung/", F.ROT),
        "",
        c("  ┌─────────────────────────────────────────────┐", F.CYAN),
        c("  │  WICHTIGE BEGRIFFE:                         │", F.CYAN + F.FETT),
        c("  │                                             │", F.CYAN),
        c("  │  Ordner / Verzeichnis  = Container fuer     │", F.WEISS),
        c("  │                          Dateien & Ordner   │", F.WEISS),
        c("  │  Datei                 = Inhalt             │", F.WEISS),
        c("  │                          (Text, Bilder...)  │", F.WEISS),
        c("  │  Pfad    = Adresse:  wald/hoehle/datei.txt  │", F.WEISS),
        c("  │  /       = Trenner zwischen Ordnern         │", F.WEISS),
        c("  │  ~       = Dein Home-Verzeichnis            │", F.WEISS),
        c("  │  .       = Aktueller Ordner                 │", F.WEISS),
        c("  │  ..      = Uebergeordneter Ordner (zurueck) │", F.WEISS),
        c("  └─────────────────────────────────────────────┘", F.CYAN),
        "",
        c("  💡 pwd zeigt deinen genauen Pfad, ls zeigt den Inhalt.", F.GELB),
    ]
    return "\n".join(zeilen)


def zeige_konzept_screen():
    """Zeigt die Konzepterklärung als eigenständigen Bildschirm."""
    clr()
    print(konzept_erklarung(None))
    print()


# ── Welt aufbauen ──────────────────────────────────────────────────────────────

def welt_aufbauen(basis: Path):
    basis.mkdir(exist_ok=True)
    # Explizite Verzeichnisstruktur (hoehle liegt innerhalb von wald)
    for raum_id in ("dorf", "wald", "see", "markt",
                    "bibliothek", "labor", "festung",
                    "bergpass", "hafen", "turm", "drachenfestung",
                    "bibliothekskeller", "schmiede", "sternwarte",
                    "akademie", "taverne", "magierschule", "palast", "garten",
                    "fernwelt", "schluesselschmiede", "zeituhr", "webwerkstatt", "deploymeisterei"):
        (basis / raum_id).mkdir(exist_ok=True)
    (basis / "wald" / "hoehle").mkdir(exist_ok=True)

    def schreibe(pfad: Path, inhalt: str):
        if not pfad.exists():
            pfad.write_text(inhalt)

    # Bestehende Dateien
    schreibe(basis / "dorf" / "aushang.txt",
        "GESUCHT: Tapfere Abenteurerin!\n"
        "Dreissig Schriftrollen muessen gerettet werden!\n"
        "Melde dich beim Aeltesten Finn.\n"
    )
    schreibe(basis / "schmiede" / "lagerliste.txt",
        "Vorraete in der Schmiede:\n"
        "- Eisen x 50\n"
        "- Kohle x 30\n"
        "- Kupfer x 20\n"
    )
    schreibe(basis / "sternwarte" / "sternenkarte.txt",
        "=== Systembeobachtung ===\n"
        "uname, df, free, du, date, cal\n"
    )
    schreibe(basis / "akademie" / "variablen.txt",
        "Wichtige Umgebungsvariablen:\n"
        "$HOME - Home-Verzeichnis\n"
        "$USER - Benutzername\n"
        "$PATH - Suchpfad\n"
        "$SHELL - Shell-Pfad\n"
    )
    schreibe(basis / "taverne" / "trickliste.txt",
        "Shell-Tricks:\n"
        "Strg+C - Abbrechen\n"
        "Strg+L - Leeren\n"
        "Strg+A - Zeilenanfang\n"
        "Tab - Autovervollstaendigung\n"
        "Pfeil-Oben - Vorheriger Befehl\n"
    )
    schreibe(basis / "magierschule" / "zauber_vorlage.sh",
        "#!/bin/bash\n"
        "NAME='Mia'\n"
        "echo Hallo $NAME\n"
        "for i in 1 2 3; do echo $i; done\n"
    )
    schreibe(basis / "palast" / "benutzerhandbuch.txt",
        "Benutzerverwaltung:\n"
        "whoami - Aktueller Benutzer\n"
        "id - User-ID und Gruppen\n"
        "sudo BEFEHL - Als Root ausfuehren\n"
        "useradd NAME - Neuen Benutzer (root)\n"
    )
    schreibe(basis / "bibliothekskeller" / "namen.txt",
        "Anna\nBernd\nClara\nAnna\n"
        "Dieter\nBernd\nEva\nAnna\n"
    )
    schreibe(basis / "bibliothekskeller" / "daten.csv",
        "Anna,25,Berlin\n"
        "Bernd,30,Hamburg\n"
        "Clara,28,Berlin\n"
        "Dieter,35,Muenchen\n"
    )
    schreibe(basis / "garten" / "gartenbuch.txt",
        "Erweiterte Dateioperationen:\n"
        "ln -s = Symlink\n"
        "find -type f = nur Dateien\n"
        "find -size +1k = nach Groesse\n"
        "du -sh = Ordnergroesse\n"
    )
    schreibe(basis / "see" / "fels.txt",
        "=== Alte Inschrift ===\n"
        "Das Wasser kennt alle Geheimnisse.\n"
        "Wer liest, der weiss. Wer weiss, der handelt.\n"
        "--- Marina, Hueterin des Sees ---\n"
    )
    schreibe(basis / "markt" / "preisliste.txt",
        "=== Preisliste ===\n"
        "Apfel       : 1 Muenze\n"
        "Zaubertrank : 5 Muenzen\n"
        "Karte       : 3 Muenzen\n"
    )

    # Bibliothek
    schreibe(basis / "bibliothek" / "buecher.txt",
        "Kapitel 1: Das Geheimnis des Terminals\n"
        "Kapitel 2: Verzeichnisse und Pfade\n"
        "Kapitel 3: Suchen und Finden\n"
        "Kapitel 4: Berechtigungen und Sicherheit\n"
        "Kapitel 5: Prozesse und Dienste\n"
        "Kapitel 6: Netzwerk und Verbindungen\n"
        "\n"
        "Wissen ist Macht. Lernen ist Abenteuer.\n"
        "Das Terminal ist dein Freund.\n"
    )

    # Labor
    schreibe(basis / "labor" / "experiment.sh",
        "#!/bin/bash\n"
        "echo 'Das Experiment ist gelueckt!'\n"
        "echo 'Du hast die Ausfuehrungsrechte gemeistert!'\n"
    )

    # Bergpass
    schreibe(basis / "bergpass" / "einkaufsliste.txt",
        "Benoetigte Software:\n"
        "- nano (Texteditor)\n"
        "- htop (Prozess-Monitor)\n"
        "- git (Versionsverwaltung)\n"
        "- curl (Datei-Download)\n"
        "- wget (Datei-Download)\n"
        "\n"
        "Installieren mit: sudo apt install paketname\n"
    )

    # Hafen
    schreibe(basis / "hafen" / "logbuch.txt",
        "Hafenlogbuch\n"
        "============\n"
        "Eingehende Verbindungen:\n"
        "- Schiff 1: google.com (Port 443)\n"
        "- Schiff 2: github.com (Port 22)\n"
        "- Schiff 3: ubuntu.com (Port 80)\n"
        "\n"
        "Alle Verbindungen sicher!\n"
    )

    # Turm
    schreibe(basis / "turm" / "zauberbuch.txt",
        "Zauberbuch des Xan\n"
        "==================\n"
        "Geheime Befehle:\n"
        "\n"
        "1. history    - Zeigt alle getippten Befehle\n"
        "2. !!         - Wiederholt letzten Befehl\n"
        "3. !befehl    - Wiederholt letzten Befehl mit diesem Namen\n"
        "4. Strg+C     - Bricht laufenden Befehl ab\n"
        "5. Strg+Z     - Pausiert Prozess (fg zum Fortsetzen)\n"
        "6. tab        - Vervollstaendigt Befehle automatisch!\n"
        "\n"
        "Das Geheimnis: Tab-Taste fuer Auto-Vervollstaendigung!\n"
    )

    # Drachenfestung
    schreibe(basis / "drachenfestung" / "drachen_geheimnis.txt",
        "=== GEHEIMES ARCHIV ===\n"
        "Von den alten Weisen niedergeschrieben:\n"
        "\n"
        "Des Drachen SCHWAECHE liegt im Wissen!\n"
        "\n"
        "Wer alle Linux-Befehle beherrscht,\n"
        "kann den Zauberbann sprechen.\n"
        "\n"
        "Die Schriftrolle zeigt: chmod +x drachenbann.sh\n"
        "Dann: ./drachenbann.sh\n"
        "\n"
        "Der Sieg ist nah!\n"
    )
    schreibe(basis / "drachenfestung" / "drachenbann.sh",
        "#!/bin/bash\n"
        "echo ''\n"
        "echo '  Blitz trifft den Drachen!'\n"
        "echo '  REMIRF bruellt vor Schmerz!'\n"
        "echo '  Der Zauberbann wirkt...'\n"
        "echo ''\n"
        "echo '  *** DER DRACHE IST BESIEGT! ***'\n"
        "echo ''\n"
        "echo '  Du hast alle Linux-Geheimnisse gemeistert!'\n"
        "echo '  SIEG FUER BINARIA!'\n"
    )


# ── Befehl ausführen ──────────────────────────────────────────────────────────

def fuehre_aus(cmd: str, cwd: Path) -> tuple[int, str, str]:
    if not cwd.exists():
        return 1, '', f'Ordner nicht gefunden: {cwd.name}'
    try:
        erg = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                             cwd=str(cwd), timeout=8)
        return erg.returncode, erg.stdout.strip(), erg.stderr.strip()
    except subprocess.TimeoutExpired:
        return 1, '', 'Zeitüberschreitung'


# ── Quest prüfen ───────────────────────────────────────────────────────────────

def pruefe_quest(spiel: Spiel, cmd: str, out: str) -> str:
    aktive = _aktive_quest(spiel)
    if not aktive:
        return ''
    try:
        ok = aktive["check"](cmd, out, spiel)
    except Exception:
        ok = False
    if ok:
        qid    = aktive["id"]
        scroll = aktive["belohnung"]
        lernz  = aktive["lernziel"]
        spiel.abschluss.add(qid)
        spiel.scrolls.append(scroll)
        rid = spiel.raum_id()
        spiel.dialog_idx[rid] = spiel.dialog_idx.get(rid, 0) + 1
        anim_scroll(scroll)
        return f"🎉 Quest erfüllt! {scroll}\n💡 {lernz}"
    return ''


# ── SSH-Mini-Shell ─────────────────────────────────────────────────────────────

def ssh_modus(spiel: Spiel) -> list:
    """Interaktive SSH-Session zum VPS. Gibt Liste von (cmd, out) zurueck."""
    if not PARAMIKO_OK:
        print(c("❌  paramiko nicht installiert! Tippe: pip3 install paramiko", F.ROT))
        return []
    if not VPS_CONFIG:
        print(c("❌  ~/.mia_vps.ini nicht gefunden! Erstelle sie zuerst.", F.ROT))
        return []

    host = VPS_CONFIG.get("host", "")
    user = VPS_CONFIG.get("user", "")
    pw   = VPS_CONFIG.get("password", "")

    clr()
    print(c('╔' + '═' * (W - 2) + '╗', F.CYAN + F.FETT))
    print(c(f"║  🌐  SSH-Verbindung zu {user}@{host}  ".ljust(W - 1) + "║", F.CYAN + F.FETT))
    print(c('╠' + '═' * (W - 2) + '╣', F.CYAN))
    print(c(f"║  Verbinde ...".ljust(W - 1) + "║", F.GRAU))

    client = _paramiko.SSHClient()
    client.set_missing_host_key_policy(_paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=pw, timeout=15)
    except Exception as e:
        print(c(f"║  ❌ Verbindungsfehler: {e}".ljust(W - 1) + "║", F.ROT))
        print(c('╚' + '═' * (W - 2) + '╝', F.CYAN))
        return []

    print(c(f"║  ✅ Verbunden!".ljust(W - 1) + "║", F.GRUEN))
    print(c('╠' + '═' * (W - 2) + '╣', F.CYAN))
    print(c(f"║  Du bist jetzt auf dem Server! Alles was du tippst laeuft DORT.".ljust(W - 1) + "║", F.GELB))
    print(c(f"║  Nuetzliche Befehle: ls · pwd · mkdir · cd · cat · nano".ljust(W - 1) + "║", F.GRAU))
    print(c(f"║  Zum Beenden tippe:  exit   (kehrt ins Koenigreich zurueck)".ljust(W - 1) + "║", F.GRAU))
    print(c('╚' + '═' * (W - 2) + '╝', F.CYAN))
    print()

    verlauf = []
    spiel.in_ssh = True

    while True:
        try:
            remote_cmd = input(c(f"{user}@{host}:~$ ", F.GRUEN + F.FETT)).strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not remote_cmd:
            continue
        if remote_cmd in ("exit", "quit", "logout"):
            print(c("Verbindung getrennt. Willkommen zurueck im Koenigreich!", F.GELB))
            break

        # http.server & blockiert exec_command → nohup+redirect, kein stdout.read()
        if "http.server" in remote_cmd:
            port = "8080"
            for tok in remote_cmd.split():
                if tok.isdigit() and 1024 < int(tok) < 65536:
                    port = tok
            default_html = (
                "<!DOCTYPE html><html><head><title>Mia Linux</title></head>"
                "<body><h1>Willkommen auf meinem Server!</h1>"
                "<p>Erstellt mit Linux-Befehlen im Mia-Abenteuer.</p>"
                "</body></html>"
            )
            safe = (
                f"mkdir -p ~/website; "
                f"[ -s ~/website/index.html ] || echo '{default_html}' > ~/website/index.html; "
                f"pkill -f 'python3 -m http.server' 2>/dev/null; "
                f"cd ~/website && nohup python3 -m http.server {port} > ~/webserver.log 2>&1 &"
            )
            client.exec_command(safe, timeout=5)
            msg = f"🌐  HTTP-Server laeuft auf Port {port}! Lass ihn laufen und tippe: exit"
            print(c(msg, F.GRUEN))
            verlauf.append((remote_cmd, f"Server gestartet auf Port {port}"))
            continue

        _, stdout, stderr = client.exec_command(remote_cmd, timeout=15)
        out = stdout.read().decode()
        err = stderr.read().decode()
        ausgabe = out or err or ""
        if ausgabe:
            print(ausgabe.rstrip())

        verlauf.append((remote_cmd, out.strip()))

    client.close()
    spiel.in_ssh = False
    return verlauf


# ── SSH-Key auf Server installieren ────────────────────────────────────────────

def install_ssh_key() -> str:
    """Kopiert den lokalen oeffentlichen SSH-Schluessel in authorized_keys auf dem VPS."""
    if not PARAMIKO_OK:
        return "❌  paramiko nicht installiert!"
    if not VPS_CONFIG:
        return "❌  ~/.mia_vps.ini nicht gefunden!"

    pub_key_path = Path.home() / ".ssh" / "id_ed25519.pub"
    if not pub_key_path.exists():
        pub_key_path = Path.home() / ".ssh" / "id_rsa.pub"
    if not pub_key_path.exists():
        return "❌  Kein SSH-Schluessel gefunden. Erstelle erst einen mit: ssh-keygen -t ed25519"

    pub_key = pub_key_path.read_text().strip()
    host = VPS_CONFIG.get("host", "")
    user = VPS_CONFIG.get("user", "")
    pw   = VPS_CONFIG.get("password", "")

    client = _paramiko.SSHClient()
    client.set_missing_host_key_policy(_paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=pw, timeout=15)
        client.exec_command("mkdir -p ~/.ssh && chmod 700 ~/.ssh")[1].read()
        client.exec_command(
            f"grep -qF '{pub_key}' ~/.ssh/authorized_keys 2>/dev/null || "
            f"echo '{pub_key}' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
        )[1].read()
        client.close()
        return f"✅  Schluessel installiert auf {user}@{host}:~/.ssh/authorized_keys"
    except Exception as e:
        return f"❌  Fehler: {e}"


# ── SCP via paramiko ───────────────────────────────────────────────────────────

def scp_upload(local_datei: Path, remote_pfad: str) -> str:
    """Uebertraegt eine lokale Datei per SFTP auf den VPS."""
    if not PARAMIKO_OK:
        return "❌  paramiko nicht installiert!"
    if not VPS_CONFIG:
        return "❌  ~/.mia_vps.ini nicht gefunden!"
    if not local_datei.exists():
        return f"❌  Datei nicht gefunden: {local_datei.name}"

    host = VPS_CONFIG.get("host", "")
    user = VPS_CONFIG.get("user", "")
    pw   = VPS_CONFIG.get("password", "")

    client = _paramiko.SSHClient()
    client.set_missing_host_key_policy(_paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=pw, timeout=15)
        sftp = client.open_sftp()
        # Zielpfad aufloesen
        ziel = remote_pfad.replace("~", f"/home/{user}")
        # Wenn Ziel ein Verzeichnis (endet mit /), Dateiname anhaengen
        if ziel.endswith("/"):
            ziel += local_datei.name
        # Zielordner anlegen falls noetig
        ziel_dir = ziel.rsplit("/", 1)[0] if "/" in ziel else f"/home/{user}"
        client.exec_command(f"mkdir -p {ziel_dir}")[1].read()
        sftp.put(str(local_datei), ziel)
        sftp.close()
        client.close()
        return f"✅  {local_datei.name} → {user}@{host}:{ziel}"
    except Exception as e:
        return f"❌  SCP-Fehler: {e}"


# ── VPS Vorbereitung (laeuft beim Start im Hintergrund) ───────────────────────

_vps_vorbereit_status = {"ok": False, "fehler": ""}

def vps_vorbereiten():
    """Bereinigt und bereitet den VPS fuer das Spiel vor. Laeuft in einem Thread."""
    if not PARAMIKO_OK or not VPS_CONFIG:
        return
    host = VPS_CONFIG.get("host", "")
    user = VPS_CONFIG.get("user", "")
    pw   = VPS_CONFIG.get("password", "")
    try:
        client = _paramiko.SSHClient()
        client.set_missing_host_key_policy(_paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=pw, timeout=15)

        default_html = (
            "<!DOCTYPE html><html><head><title>Mia Linux</title></head>"
            "<body><h1>Willkommen auf meinem Server!</h1>"
            "<p>Erstellt mit Linux-Befehlen im Mia-Abenteuer.</p>"
            "</body></html>"
        )
        befehle = [
            "pkill -f 'python3 -m http.server' 2>/dev/null; true",
            "rm -rf ~/website && mkdir -p ~/website",
            f"echo '{default_html}' > ~/website/index.html",
            "crontab -r 2>/dev/null; true",
            "rm -f ~/zeitlog.txt",
            f"nohup python3 -m http.server 8080 --directory ~/website > ~/webserver.log 2>&1 &",
        ]
        for b in befehle:
            _, stdout, stderr = client.exec_command(b, timeout=10)
            stdout.read(); stderr.read()

        client.close()
        _vps_vorbereit_status["ok"] = True
    except Exception as e:
        _vps_vorbereit_status["fehler"] = str(e)


# ── Hauptspielschleife ─────────────────────────────────────────────────────────

def spielschleife(spiel: Spiel):
    nachricht    = ''
    zeige_dialog = True

    while True:
        zeige_bildschirm(spiel, nachricht, zeige_dialog)
        zeige_dialog = False
        nachricht    = ''

        try:
            cmd = input().strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not cmd:
            continue

        teile     = cmd.split()
        basis_cmd = teile[0].lower()

        # ── Interne Spielbefehle ───────────────────────────────────────────────
        if basis_cmd in ("hilfe", "help", "?", "h"):
            nachricht = (
                "LINUX-BEFEHLE:\n"
                "  ls          – Ordnerinhalt anzeigen\n"
                "  pwd         – Aktuellen Pfad anzeigen\n"
                "  cd [ort]    – Woanders hingehen (z.B. cd wald)\n"
                "  mkdir name  – Neuen Ordner erstellen\n"
                "  touch x.txt – Neue Datei erstellen\n"
                "  cat x.txt   – Dateiinhalt lesen\n"
                "  echo 't' >f – Text in Datei schreiben\n"
                "  cp von nach – Datei kopieren\n"
                "  mv von nach – Datei verschieben/umbenennen\n"
                "  rm x.txt    – Datei loeschen\n"
                "  grep 'x' f  – In Datei suchen\n"
                "  find . -name – Dateien finden\n"
                "  cat f | wc -l – Pipe: Ausgabe weiterleiten\n"
                "  ls -l       – Berechtigungen anzeigen\n"
                "  chmod 755 f – Berechtigungen setzen\n"
                "  chmod +x f  – Datei ausfuehrbar machen\n"
                "  ps / ps aux – Prozesse anzeigen\n"
                "  sleep 10 &  – Prozess im Hintergrund\n"
                "  apt-cache search – Software suchen\n"
                "  ping IP     – Netzwerkverbindung testen\n"
                "  wget URL    – Datei herunterladen\n"
                "  curl URL    – HTTP-Anfrage senden\n"
                "  ssh user@IP – Auf Remote-Server einloggen\n"
                "  scp datei user@IP:~/pfad/ – Datei uebertragen\n"
                "  nano datei  – Texteditor oeffnen\n"
                "SPIELBEFEHLE:\n"
                "  schau  – Mit NPC sprechen (Quest holen)\n"
                "  karte  – Weltkarte anzeigen\n"
                "  inventar / status – Fortschritt anzeigen\n"
                "  konzept – Dateisystem-Erklaerung\n"
                "  spickzettel – Linux-Spickzettel\n"
                "  beenden – Spiel beenden (Fortschritt gespeichert)\n"
                "  sshhilfe – SSH-Anleitung anzeigen\n"
                "  warp <raum> – Direkt zu einem Raum springen (auch: warp 5)\n"
                "  zurueck – Einen Raum zurueck"
            )
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "sshhilfe":
            host_anzeige = VPS_CONFIG.get('host', 'SERVER_IP')
            user_anzeige = VPS_CONFIG.get('user', 'mia')
            nachricht = (
                "╔══ SSH-ANLEITUNG ══════════════════════════════╗\n"
                "║                                               ║\n"
                f"║  1. Verbinden:                                ║\n"
                f"║     ssh {user_anzeige}@{host_anzeige}         ║\n"
                "║     → Du siehst: mia@server:~$  (SSH-Modus!) ║\n"
                "║                                               ║\n"
                "║  2. Im SSH-Modus (auf dem Server):            ║\n"
                "║     ls          Dateien anzeigen              ║\n"
                "║     pwd         Aktuellen Pfad                ║\n"
                "║     mkdir name  Ordner erstellen              ║\n"
                "║     cd ordner   In Ordner wechseln            ║\n"
                "║     cat datei   Datei lesen                   ║\n"
                "║     exit        Verbindung trennen            ║\n"
                "║                                               ║\n"
                "║  3. Datei uebertragen (LOKAL, kein SSH):      ║\n"
                f"║     scp datei.html {user_anzeige}@{host_anzeige}:~/website/ ║\n"
                "║                                               ║\n"
                "║  WICHTIG: ls/mkdir etc. im SSH-Modus          ║\n"
                "║  laufen auf dem SERVER, nicht lokal!          ║\n"
                "╚═══════════════════════════════════════════════╝"
            )
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "karte":
            nachricht = (
                "     🗺️  WELTKARTE:\n"
                "            [🏠 Dorf]\n"
                "           /   |   \\\n"
                " [🌲 Wald] [🌊 See] [🏪 Markt]──[📚 Bib.]──[⚗️ Labor]\n"
                "     |                                           |\n"
                " [⛏️ Hoehle]                             [🏰 Festung]\n"
                "                                                |\n"
                "                                        [⛰️ Bergpass]\n"
                "                                                |\n"
                "                                          [⚓ Hafen]\n"
                "                                                |\n"
                "                                         [🗼 Turm]\n"
                "                                                |\n"
                "                                    [🐉 Drachenfestung]\n"
                "\n"
                "Reisen mit: cd wald   cd see   cd markt   cd bibliothek   usw."
            )
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "inventar":
            if spiel.scrolls:
                zeilen = "\n".join(f"  {s}" for s in spiel.scrolls)
                nachricht = f"📚 Deine Schriftrollen ({len(spiel.scrolls)}/{GESAMT_QUESTS}):\n{zeilen}"
            else:
                nachricht = "Du hast noch keine Schriftrollen.\nSpreche mit einem NPC (schau) um eine Quest zu bekommen!"
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "status":
            total = sum(len(r.get("quests", [])) for r in RAEUME.values())
            getan = len(spiel.abschluss)
            nachricht = f"Quests: {getan}/{total}   Schriftrollen: {len(spiel.scrolls)}/{GESAMT_QUESTS}\nBesuche alle Orte um alle Schriftrollen zu finden!"
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "konzept":
            nachricht = konzept_erklarung(spiel)
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "spickzettel":
            spickzettel()
            input(c("  ↵ Zurueck zum Spiel", F.CYAN) + "  ")
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "schau":
            zeige_dialog = True
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd in ("beenden", "exit", "quit"):
            spiel.speichern()
            print(c("\n  Bis zum naechsten Abenteuer! 👋\n", F.GELB))
            return

        # ── cd: Raum wechseln ─────────────────────────────────────────────────
        if basis_cmd == "cd":
            spiel.ort_verlauf.append(spiel.aktuell)  # History merken
            if len(spiel.ort_verlauf) > 20:
                spiel.ort_verlauf.pop(0)
            ziel = teile[1] if len(teile) > 1 else '..'
            if ziel == '..':
                neues = spiel.aktuell.parent
                # Wenn parent == basis oder außerhalb → automatisch nach dorf
                if neues == spiel.basis or not str(neues).startswith(str(spiel.basis)):
                    neues = spiel.basis / "dorf"
                    anim_reise(spiel.aktuell.name, "dorf")
                    spiel.aktuell = neues
                    zeige_dialog  = True
                    nachricht     = "Du gehst zurueck zum Dorfplatz 🏠"
                else:
                    anim_reise(spiel.aktuell.name, neues.name)
                    spiel.aktuell = neues
                    zeige_dialog  = True
                    nachricht     = f"Willkommen zurueck in: {spiel.raum()['name']}"
            else:
                # Zuerst relativ zum aktuellen Verzeichnis suchen,
                # dann als Top-Level-Raum (z.B. "cd dorf" von überall)
                neues = (spiel.aktuell / ziel).resolve()
                if not neues.exists():
                    neues = (spiel.basis / ziel).resolve()
                if not str(neues).startswith(str(spiel.basis)):
                    nachricht = "⚠️  Das liegt ausserhalb des Abenteuerlandes!"
                elif not neues.exists():
                    verfuegbar = list(spiel.raum().get("ausgaenge", {}).keys())
                    nachricht = (
                        f"'{ziel}' gibt es hier nicht.\n"
                        f"Ausgaenge: {', '.join(verfuegbar)}"
                    )
                else:
                    anim_reise(spiel.aktuell.name, neues.name)
                    spiel.aktuell = neues
                    zeige_dialog  = True
                    nachricht     = f"Du betrittst: {spiel.raum()['name']} {spiel.raum()['emoji']}"

            q_erg = pruefe_quest(spiel, cmd, '')
            if q_erg:
                nachricht = q_erg
                zeige_dialog = True
            spiel.terminal.append((cmd, ''))
            spiel.speichern()
            continue

        # ── zurueck: einen Raum zurueck ────────────────────────────────────────
        if basis_cmd in ("zurueck", "back", "zurück"):
            if spiel.ort_verlauf:
                vorher = spiel.ort_verlauf.pop()
                if vorher.exists():
                    spiel.aktuell = vorher
                    nachricht = f"↩  Zurueck nach: {spiel.raum()['name']} {spiel.raum()['emoji']}"
                    zeige_dialog = True
                else:
                    nachricht = "⚠️  Vorheriger Raum existiert nicht mehr."
            else:
                nachricht = "Du bist schon am Anfang – kein Verlauf vorhanden."
            spiel.terminal.append((cmd, ''))
            spiel.speichern()
            continue

        # ── warp: direkt zu einem Raum springen ────────────────────────────────
        if basis_cmd == "warp":
            alle_raeume = list(RAEUME.keys())
            if len(teile) < 2:
                raum_liste = "\n".join(
                    f"  {i+1:2}. {rid:25} {RAEUME[rid]['emoji']} {RAEUME[rid]['name']}"
                    for i, rid in enumerate(alle_raeume)
                )
                nachricht = f"Tippe:  warp <raumname>  oder  warp <nummer>\n\n{raum_liste}"
            else:
                ziel_raw = teile[1].lower()
                # Nummer oder Name
                ziel_rid = None
                if ziel_raw.isdigit():
                    idx = int(ziel_raw) - 1
                    if 0 <= idx < len(alle_raeume):
                        ziel_rid = alle_raeume[idx]
                else:
                    if ziel_raw in RAEUME:
                        ziel_rid = ziel_raw
                    else:
                        # Fuzzy: erste Übereinstimmung im Namen
                        for rid in alle_raeume:
                            if ziel_raw in rid or ziel_raw in RAEUME[rid]['name'].lower():
                                ziel_rid = rid
                                break
                if ziel_rid:
                    spiel.ort_verlauf.append(spiel.aktuell)
                    ziel_pfad = spiel.basis / ziel_rid
                    if not ziel_pfad.exists():
                        ziel_pfad.mkdir(parents=True, exist_ok=True)
                    spiel.aktuell = ziel_pfad
                    raum_info = RAEUME[ziel_rid]
                    nachricht = f"🌀 Warp nach: {raum_info['emoji']} {raum_info['name']}"
                    zeige_dialog = True
                else:
                    nachricht = f"Raum '{teile[1]}' nicht gefunden.\nTippe  warp  fuer die Liste."
            spiel.terminal.append((cmd, ''))
            spiel.speichern()
            continue

        # ── nano: Texteditor interaktiv ────────────────────────────────────────
        if basis_cmd == "nano":
            ziel_datei = teile[1] if len(teile) > 1 else "temp.txt"
            datei_pfad = spiel.aktuell / ziel_datei
            vorher_exists = datei_pfad.exists()
            vorher_mtime = datei_pfad.stat().st_mtime if vorher_exists else 0
            subprocess.run(["nano", ziel_datei], cwd=str(spiel.aktuell))
            nachher_exists = datei_pfad.exists()
            nachher_mtime = datei_pfad.stat().st_mtime if nachher_exists else 0
            if nachher_exists and (not vorher_exists or nachher_mtime > vorher_mtime):
                out_nano = f"Datei '{ziel_datei}' gespeichert!"
            else:
                out_nano = "nano beendet (ohne Aenderungen)"
            spiel.terminal.append((cmd, out_nano))
            q_erg = pruefe_quest(spiel, cmd, out_nano)
            if q_erg:
                nachricht = q_erg
                zeige_dialog = True
            else:
                nachricht = out_nano
            spiel.speichern()
            continue

        # ── ssh-keygen: Schluesselpaar erstellen (lokal, non-interaktiv) ─────────
        if basis_cmd == "ssh-keygen":
            key_path = Path.home() / ".ssh" / "id_ed25519"
            if key_path.exists():
                ausgabe = f"✅ Schluessel bereits vorhanden: {key_path}\n   Nutze: cat {key_path}.pub"
                rc = 0
            else:
                ni_cmd = f"ssh-keygen -t ed25519 -f {key_path} -N ''"
                rc, out, err = fuehre_aus(ni_cmd, spiel.aktuell)
                ausgabe = out or err or "Schluessel erstellt!"
            q_erg = pruefe_quest(spiel, cmd, ausgabe)
            nachricht = q_erg if q_erg else ausgabe[:300]
            if q_erg:
                zeige_dialog = True
            spiel.terminal.append((cmd, ausgabe[:150]))
            spiel.speichern()
            continue

        # ── ssh-copy-id: Key per paramiko auf VPS installieren ─────────────────
        if basis_cmd == "ssh-copy-id":
            print(c("Installiere SSH-Schluessel auf dem Server ...", F.CYAN))
            ergebnis = install_ssh_key()
            q_erg = pruefe_quest(spiel, cmd, ergebnis)
            nachricht = q_erg if q_erg else ergebnis
            if q_erg:
                zeige_dialog = True
            spiel.terminal.append((cmd, ergebnis[:150]))
            spiel.speichern()
            continue

        # ── ssh: interaktive Fernverbindung ────────────────────────────────────
        if basis_cmd == "ssh":
            # Quest fuer das Verbinden selbst pruefen
            q_erg = pruefe_quest(spiel, cmd, "ssh gestartet")
            if q_erg:
                nachricht = q_erg
                zeige_dialog = True
            if not PARAMIKO_OK or not VPS_CONFIG:
                if not PARAMIKO_OK:
                    nachricht = "❌ paramiko fehlt. Tippe: pip3 install paramiko"
                else:
                    nachricht = "❌ ~/.mia_vps.ini nicht gefunden!"
                spiel.terminal.append((cmd, nachricht))
                spiel.speichern()
                continue
            # Starte SSH-Mini-Shell
            verlauf = ssh_modus(spiel)
            # Quest-Checks fuer alle Remote-Befehle
            # in_ssh muss True sein waehrend der Checks (ssh_modus setzt es auf False)
            spiel.in_ssh = True
            for r_cmd, r_out in verlauf:
                rq = pruefe_quest(spiel, r_cmd, r_out)
                if rq and not zeige_dialog:
                    nachricht = rq
                    zeige_dialog = True
            spiel.in_ssh = False
            # SSH-Verlauf im Terminal-Panel sichtbar machen
            for r_cmd, r_out in verlauf[-8:]:
                kurzout = r_out[:80].replace('\n', ' ') if r_out else "✅"
                spiel.terminal.append((f"ssh> {r_cmd}", kurzout))
            if not verlauf:
                spiel.terminal.append((cmd, "SSH-Session beendet (0 Befehle)"))
            spiel.speichern()
            continue

        # ── Shell-Skripte mit scp-Befehlen abfangen ────────────────────────────
        if basis_cmd.startswith("./") and basis_cmd.endswith(".sh") and spiel.raum_id() in {"fernwelt", "deploymeisterei", "webwerkstatt"}:
            skript_name = basis_cmd[2:]
            skript_pfad = spiel.aktuell / skript_name
            if skript_pfad.exists():
                skript_inhalt = skript_pfad.read_text()
                ausgabe_zeilen = []
                for zeile in skript_inhalt.splitlines():
                    z = zeile.strip()
                    if not z or z.startswith("#!"):
                        continue
                    if z.startswith("scp ") and (VPS_CONFIG.get("host", "") in z or "152.53." in z):
                        # scp-Zeile via paramiko simulieren
                        zsh = z.split()
                        if len(zsh) >= 3:
                            lok = spiel.aktuell / zsh[1]
                            ziel_pfad = zsh[-1].split(":", 1)[-1] if ":" in zsh[-1] else "~/website/"
                            ausgabe_zeilen.append(scp_upload(lok, ziel_pfad))
                    elif z.startswith("echo "):
                        _, sh_out, _ = fuehre_aus(z, spiel.aktuell)
                        if sh_out:
                            ausgabe_zeilen.append(sh_out)
                ergebnis = "\n".join(ausgabe_zeilen) if ausgabe_zeilen else f"✅  {skript_name} ausgefuehrt"
                q_erg = pruefe_quest(spiel, cmd, ergebnis)
                nachricht = q_erg if q_erg else ergebnis
                if q_erg:
                    zeige_dialog = True
                spiel.terminal.append((cmd, ergebnis[:150]))
                spiel.speichern()
                continue

        # ── scp: Datei auf VPS uebertragen ─────────────────────────────────────
        if basis_cmd == "scp":
            # Einfache Verarbeitung: scp LOKALDATEI user@host:ZIELPFAD
            scp_teile = teile[1:] if len(teile) > 1 else []
            if len(scp_teile) >= 2:
                lok = spiel.aktuell / scp_teile[0]
                ziel_pfad = scp_teile[-1].split(":", 1)[-1] if ":" in scp_teile[-1] else "~/website/"
                ergebnis = scp_upload(lok, ziel_pfad)
            else:
                ergebnis = "Verwendung: scp DATEINAME mia@IP:~/ziel/"
            q_erg = pruefe_quest(spiel, cmd, ergebnis)
            nachricht = q_erg if q_erg else ergebnis
            if q_erg:
                zeige_dialog = True
            spiel.terminal.append((cmd, ergebnis[:150]))
            spiel.speichern()
            continue

        # ── Alle anderen Befehle: wirklich ausführen ───────────────────────────
        VPS_RAEUME = {"fernwelt", "schluesselschmiede", "zeituhr", "webwerkstatt", "deploymeisterei"}
        if spiel.raum_id() in VPS_RAEUME and basis_cmd in ("ls", "mkdir", "cd", "cat", "rm", "touch", "pwd", "crontab", "echo", "sed"):
            aktive_q = _aktive_quest(spiel)
            q_modus  = aktive_q.get("modus", "") if aktive_q else ""
            # Lokal-Quests: Befehl normal ausfuehren, KEIN Intercept
            if q_modus != "lokal":
                vps_user = VPS_CONFIG.get('user', 'mia')
                vps_host = VPS_CONFIG.get('host', 'SERVER_IP')
                if q_modus == "ssh":
                    nachricht = (
                        f"🖥️  Dieser Befehl muss AUF DEM SERVER laufen!\n\n"
                        f"  1. Tippe:  ssh {vps_user}@{vps_host}\n"
                        f"  2. Du siehst:  {vps_user}@{vps_host}:~$\n"
                        f"  3. Dann tippe:  {aktive_q['ziel']}\n\n"
                        f"  Tipp:  sshhilfe  fuer mehr Hilfe"
                    )
                else:
                    nachricht = (
                        f"🖥️  Verbinde dich zuerst per SSH:\n"
                        f"     ssh {vps_user}@{vps_host}"
                    )
                spiel.terminal.append((cmd, "[Server-Befehl lokal getippt]"))
                spiel.speichern()
                continue

        rc, out, err = fuehre_aus(cmd, spiel.aktuell)
        ausgabe = out or err or ''

        # Curl in VPS-Raum: Server nicht erreichbar → automatisch starten und nochmal versuchen
        VPS_RAEUME_SET = {"fernwelt", "webwerkstatt", "deploymeisterei"}
        if basis_cmd == "curl" and spiel.raum_id() in VPS_RAEUME_SET and rc != 0 and PARAMIKO_OK and VPS_CONFIG:
            vps_host = VPS_CONFIG.get("host", "")
            if vps_host and vps_host in cmd:
                try:
                    _c2 = _paramiko.SSHClient()
                    _c2.set_missing_host_key_policy(_paramiko.AutoAddPolicy())
                    _c2.connect(vps_host, username=VPS_CONFIG.get("user",""), password=VPS_CONFIG.get("password",""), timeout=10)
                    default_html = (
                        "<!DOCTYPE html><html><head><title>Mia Linux</title></head>"
                        "<body><h1>Willkommen auf meinem Server!</h1>"
                        "<p>Erstellt mit Linux-Befehlen im Mia-Abenteuer.</p>"
                        "</body></html>"
                    )
                    chan = _c2.get_transport().open_session()
                    chan.exec_command(
                        f"mkdir -p ~/website; "
                        f"[ -s ~/website/index.html ] || echo '{default_html}' > ~/website/index.html; "
                        f"pkill -f 'python3 -m http.server' 2>/dev/null; "
                        f"nohup python3 -m http.server 8080 --directory ~/website > ~/webserver.log 2>&1 &"
                    )
                    import time as _t; _t.sleep(0.5)
                    chan.close()
                    _c2.close()
                    print(c("  ⏳  Server wird gestartet, warte 4 Sekunden ...", F.GRAU))
                    _t.sleep(4)
                    rc, out, err = fuehre_aus(cmd, spiel.aktuell)
                    ausgabe = out or err or ''
                    if out:
                        ausgabe = "🌐 Server gestartet! " + out
                except Exception:
                    pass  # Fehler ignorieren, curl-Ausgabe bleibt

        spiel.terminal.append((cmd, ausgabe[:150]))

        q_erg = pruefe_quest(spiel, cmd, out)
        if q_erg:
            nachricht    = q_erg
            zeige_dialog = True
        elif ausgabe:
            nachricht = ausgabe[:300]
        elif rc == 0:
            nachricht = "✅ Ausgefuehrt!"
        else:
            nachricht = f"❌ Fehler (Code {rc})"

        spiel.speichern()

        # Sieg-Check: alle 30 Schriftrollen gesammelt
        if len(spiel.scrolls) >= GESAMT_QUESTS:
            time.sleep(0.8)
            # Prüfe ob letzter Scroll aus der Drachenfestung kommt (epischer Sieg)
            letzter_qid = list(spiel.abschluss)[-1] if spiel.abschluss else ""
            if "drache" in letzter_qid:
                anim_drachen_sieg(spiel)
            else:
                anim_sieg()
                clr()
                print()
                print(c('╔' + '═' * (W - 2) + '╗', F.GELB + F.FETT))
                print(c(f"║{'🎉  DER FLUCH IST GEBROCHEN!  🎉'.center(W-2)}║", F.GELB + F.FETT))
                print(c('╚' + '═' * (W - 2) + '╝', F.GELB + F.FETT))
                print()
                langsam(f"{spiel.spielerin}! Du hast alle {GESAMT_QUESTS} Schriftrollen gesammelt!", F.PINK, 0.04)
                langsam("Das Koenigreich Binaria ist gerettet! Die Bewohner jubeln!", F.WEISS, 0.03)
                print()
                print(c("  Was du gelernt hast:", F.GELB + F.FETT))
                for s in spiel.scrolls:
                    print(c(f"    {s}", F.GRUEN))
                    time.sleep(0.1)
                print()
                print(c("  Spickzettel:  python3 mia_lernt_linux.py --spickzettel", F.GRAU))
                print(c("  Konzepte:     python3 mia_lernt_linux.py --konzept", F.GRAU))
                print()
            break


# ── Startbildschirm ────────────────────────────────────────────────────────────

def startbildschirm() -> str:
    clr()
    print(c('╔' + '═' * (W - 2) + '╗', F.PINK + F.FETT))
    for z in [
        "     ⚔️   Mia's Linux-Abenteuer   ⚔️     ",
        "  Lerne Linux-Befehle in einer Fantasywelt!  ",
    ]:
        print(c(f"║{z.center(W-2)}║", F.PINK + F.FETT))
    print(c('╠' + '═' * (W - 2) + '╣', F.PINK))

    geschichte = [
        "Das Koenigreich Binaria wurde vom boesen Zauberer 'rm -rf'",
        "verflucht! Alle Magie ist verschwunden.",
        "",
        "Nur du, Mia – mutige Abenteurerin – kannst helfen!",
        "Sammle alle 30 magischen Schriftrollen, die ueber die",
        "Lande verstreut sind, um den Fluch zu brechen!",
        "",
        "12 Orte warten auf dich – von der Bibliothek bis zur",
        "Drachenfestung des maechtigen Remirf!",
        "",
        "Jede Schriftrolle lehrt dir einen echten Linux-Befehl.",
        "Tippe 'hilfe' wenn du nicht weiterkommst.",
        "Tippe 'karte' fuer die Weltkarte.",
        "Tippe 'schau' um mit dem NPC zu sprechen.",
    ]
    for z in geschichte:
        row = f"  {z}"
        print(c('║', F.PINK) + c(row, F.WEISS) + ' ' * max(0, W - 2 - len(row)) + c('║', F.PINK))

    print(c('╠' + '─' * (W - 2) + '╣', F.PINK))
    eingabe_zeile = c("  Wie heisst du, Abenteurerin? ", F.GELB)
    print(c('║', F.PINK) + eingabe_zeile, end='')
    name = input().strip() or "Mia"
    print(c('╚' + '═' * (W - 2) + '╝', F.PINK))
    return name


# ── Spickzettel ────────────────────────────────────────────────────────────────

def spickzettel():
    clr()
    S = min(W, 68)
    def row(befehl, beschreibung):
        eintrag = f"    {befehl:<22} {beschreibung}"
        print(c(f"║{c(eintrag, F.WEISS):<{S + 8}}║", F.CYAN))

    print(c('╔' + '═' * (S - 2) + '╗', F.CYAN + F.FETT))
    print(c(f"║{'  ⚔️  Linux-Spickzettel fuer Mia  ⚔️  '.center(S-2)}║", F.CYAN + F.FETT))
    print(c('╠' + '═' * (S - 2) + '╣', F.CYAN + F.FETT))

    print(c(f"║  {c('NAVIGATION', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("pwd",             "Aktuellen Pfad anzeigen")
    row("ls",              "Ordnerinhalt anzeigen")
    row("ls -l",           "Mit Details (Datum, Groesse)")
    row("cd ordner",       "In Ordner wechseln")
    row("cd ..",           "Eine Ebene zurueck")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))

    print(c(f"║  {c('ERSTELLEN', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("mkdir name",      "Neuen Ordner erstellen")
    row("touch datei.txt", "Neue leere Datei erstellen")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))

    print(c(f"║  {c('LESEN & SCHREIBEN', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("cat datei.txt",   "Dateiinhalt anzeigen")
    row('echo "text"',     "Text ausgeben")
    row('echo "t" > datei',"In Datei schreiben")
    row('echo "t" >>datei',"An Datei anhaengen")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))

    print(c(f"║  {c('KOPIEREN / VERSCHIEBEN / LOESCHEN', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("cp quelle ziel",  "Datei kopieren")
    row("mv alt neu",      "Verschieben/umbenennen")
    row("rm datei.txt",    "Loeschen (ACHTUNG: endgueltig!)")
    row("rmdir ordner",    "Leeren Ordner loeschen")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))

    print(c(f"║  {c('SUCHEN & PIPES', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("grep 'x' datei",  "In Datei nach Text suchen")
    row("find . -name '*.txt'", "Dateien finden")
    row("cmd1 | cmd2",     "Ausgabe weiterleiten (Pipe)")
    row("wc -l datei",     "Zeilen zaehlen")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))

    print(c(f"║  {c('BERECHTIGUNGEN', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("ls -l",           "Berechtigungen anzeigen")
    row("chmod 755 datei", "Berechtigungen setzen (rwxr-xr-x)")
    row("chmod +x datei",  "Datei ausfuehrbar machen")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))

    print(c(f"║  {c('PROZESSE', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("ps",              "Eigene Prozesse anzeigen")
    row("ps aux",          "Alle Prozesse mit Details")
    row("kill PID",        "Prozess beenden")
    row("sleep 10 &",      "Prozess im Hintergrund")
    row("jobs",            "Hintergrundprozesse anzeigen")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))

    print(c(f"║  {c('PAKETE (APT)', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("apt-cache search x", "Software suchen")
    row("apt-cache show x",   "Paketdetails anzeigen")
    row("apt list --installed","Installierte Pakete")
    row("sudo apt install x",  "Software installieren")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))

    print(c(f"║  {c('NETZWERK', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("ping -c 3 IP",       "Netzwerkverbindung testen")
    row("wget URL",           "Datei herunterladen")
    row("curl URL",           "HTTP-Anfrage senden")
    row("ssh user@host",      "Auf Remote-Server einloggen")
    row("scp datei user@h:~", "Datei per SSH uebertragen")
    row("python3 -m http.server 8080", "Webserver starten")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))

    print(c(f"║  {c('EDITOR & SKRIPTE', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("nano datei.txt",  "Texteditor oeffnen")
    row("  Strg+O",        "Speichern in nano")
    row("  Strg+X",        "nano beenden")
    row("#!/bin/bash",     "Shebang-Zeile fuer Skripte")
    row("./skript.sh",     "Skript im aktuellen Ordner ausfuehren")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))

    print(c(f"║  {c('HILFE', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("befehl --help",   "Kurze Hilfe")
    row("man befehl",      "Ausfuehrliches Handbuch")
    print(c('╚' + '═' * (S - 2) + '╝', F.CYAN + F.FETT))
    print()


# ── Einstieg ──────────────────────────────────────────────────────────────────

def main():
    if '--spickzettel' in sys.argv or '-s' in sys.argv:
        spickzettel()
        return

    if '--konzept' in sys.argv or '-k' in sys.argv:
        zeige_konzept_screen()
        return

    if '--neustart' in sys.argv:
        savefile = Path.home() / "linux_abenteuer" / ".save.json"
        if savefile.exists():
            savefile.unlink()
        print(c("  Spielstand geloescht. Viel Spass beim neuen Abenteuer!\n", F.GELB))

    basis = Path.home() / "linux_abenteuer"
    welt_aufbauen(basis)

    # VPS im Hintergrund vorbereiten (bereinigt + richtet ein)
    if PARAMIKO_OK and VPS_CONFIG:
        import threading
        print(c(f"  🌐  Verbinde mit VPS ({VPS_CONFIG.get('host','?')}) und bereite Server vor ...", F.GRAU))
        _t = threading.Thread(target=vps_vorbereiten, daemon=True)
        _t.start()
        _t.join(timeout=20)
        if _vps_vorbereit_status["ok"]:
            print(c("  ✅  Server bereit! (website/ geleert, Webserver gestoppt)\n", F.GRUEN))
        elif _vps_vorbereit_status["fehler"]:
            print(c(f"  ⚠️   VPS nicht erreichbar: {_vps_vorbereit_status['fehler'][:80]}", F.GELB))
            print(c("       VPS-Raeume sind gesperrt bis die Verbindung klappt.\n", F.GRAU))
        else:
            print(c("  ⚠️   VPS-Vorbereitung Timeout (>20s) – VPS-Raeume eventuell nicht bereit.\n", F.GELB))

    name  = startbildschirm()
    spiel = Spiel(basis, name)
    spiel.laden()

    if not spiel.scrolls:
        clr()
        # Kurze Dateisystem-Einführung für Erstbenutzer
        print(c('╔' + '═' * (W - 2) + '╗', F.CYAN))
        print(c(f"║{'  📚 Kurze Erklaerung – was ist ein Dateisystem?  '.center(W-2)}║", F.CYAN + F.FETT))
        print(c('╠' + '═' * (W - 2) + '╣', F.CYAN))
        erklaerung = [
            "Ein Computer speichert alles in Dateien und Ordnern –",
            "genau wie ein echter Aktenschrank:",
            "",
            "  📦 Ordner  = Ein Fach im Aktenschrank",
            "               Kann andere Ordner oder Dateien enthalten",
            "  📄 Datei   = Ein Dokument im Fach",
            "               Enthaelt Text, Bilder, Programme ...",
            "",
            "  Ordner koennen ineinander geschachtelt sein:",
            "  musik/ -> rock/ -> song.mp3",
            "",
            "  pwd zeigt dir wo du gerade bist.",
            "  ls  zeigt dir was in deinem Ordner liegt.",
            "  cd  bringt dich in einen anderen Ordner.",
            "",
            "  Im Spiel = jeder Raum ist ein echter Ordner auf deinem PC!",
            "  Tippe 'konzept' um diese Erklaerung nochmal zu sehen.",
        ]
        for z in erklaerung:
            row = f"  {z}"
            print(c('║', F.CYAN) + c(row, F.WEISS) + ' ' * max(0, W - 2 - len(row)) + c('║', F.CYAN))
        print(c('╚' + '═' * (W - 2) + '╝', F.CYAN))
        print()
        langsam(f"Willkommen, {name}! Dein Abenteuer beginnt!", F.PINK, 0.05)
        print()
        print(c("  💡 Tipps:", F.GELB + F.FETT))
        print(c("     schau    -> NPC ansprechen (Quest bekommen)", F.GELB))
        print(c("     hilfe    -> alle Befehle anzeigen", F.GELB))
        print(c("     karte    -> Weltkarte anzeigen", F.GELB))
        print(c("     konzept  -> Dateisystem-Erklaerung", F.GELB))
        print()
        input(c("  ↵ Los geht's!", F.CYAN) + "  ")

    try:
        spielschleife(spiel)
    except KeyboardInterrupt:
        print(c("\n\n  Gespeichert! Bis zum naechsten Abenteuer! 👋\n", F.GELB))
        spiel.speichern()


if __name__ == "__main__":
    main()
