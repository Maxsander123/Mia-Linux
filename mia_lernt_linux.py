#!/usr/bin/env python3
"""
⚔️  Mia's Linux-Abenteuer ⚔️
RPG-Lernspiel für die Linux-Kommandozeile
Steuere Mia durch eine Fantasiewelt und lerne dabei echte Linux-Befehle!
"""

import os, sys, subprocess, time, json, textwrap
from pathlib import Path

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
        ],
    },
    "markt": {
        "name":   "Marktplatz",
        "emoji":  "🏪",
        "beschreibung": (
            "Bunte Marktstände, Händler rufen ihre Waren.\n"
            "Eine Händlerin mit Zylinder winkt dich heran."
        ),
        "ausgaenge": {"dorf": "Dorf", "bibliothek": "Bibliothek"},
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
        "ausgaenge": {"markt": "Markt", "labor": "Labor"},
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
        "ausgaenge": {"bibliothek": "Bibliothek", "festung": "Festung"},
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
        "ausgaenge": {"labor": "Labor", "bergpass": "Bergpass"},
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
        "ausgaenge": {"festung": "Festung", "hafen": "Hafen"},
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
        "ausgaenge": {"bergpass": "Bergpass", "turm": "Turm"},
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
        "ausgaenge": {"hafen": "Hafen", "drachenfestung": "Drachenfestung"},
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
}

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
        q_c = c(f"  🎯 Quest: {aktive['ziel']}", F.GELB)
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
    langsam(f"{spiel.spielerin}! Du hast alle 30 Schriftrollen gesammelt!", F.PINK, 0.04)
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
                    "bergpass", "hafen", "turm", "drachenfestung"):
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
                "  nano datei  – Texteditor oeffnen\n"
                "SPIELBEFEHLE:\n"
                "  schau  – Mit NPC sprechen (Quest holen)\n"
                "  karte  – Weltkarte anzeigen\n"
                "  inventar / status – Fortschritt anzeigen\n"
                "  konzept – Dateisystem-Erklaerung\n"
                "  spickzettel – Linux-Spickzettel\n"
                "  beenden – Spiel beenden (Fortschritt gespeichert)"
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
                nachricht = f"📚 Deine Schriftrollen ({len(spiel.scrolls)}/30):\n{zeilen}"
            else:
                nachricht = "Du hast noch keine Schriftrollen.\nSpreche mit einem NPC (schau) um eine Quest zu bekommen!"
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "status":
            total = sum(len(r.get("quests", [])) for r in RAEUME.values())
            getan = len(spiel.abschluss)
            nachricht = f"Quests: {getan}/{total}   Schriftrollen: {len(spiel.scrolls)}/30\nBesuche alle Orte um alle Schriftrollen zu finden!"
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

        # ── Alle anderen Befehle: wirklich ausführen ───────────────────────────
        rc, out, err = fuehre_aus(cmd, spiel.aktuell)
        ausgabe = out or err or ''
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
        if len(spiel.scrolls) >= 30:
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
                langsam(f"{spiel.spielerin}! Du hast alle 30 Schriftrollen gesammelt!", F.PINK, 0.04)
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
    row("ping -c 3 IP",    "Netzwerkverbindung testen")
    row("wget URL",        "Datei herunterladen")
    row("curl URL",        "HTTP-Anfrage senden")
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
