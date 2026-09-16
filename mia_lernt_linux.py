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
    "bibliothek": [
        c(" 📚 📚 📚 📚 📚 📚 📚 📚  ", ''),
        c(" |   |   |   |   |   |   |  ", F.BRAUN),
        c("     📖         📜          ", ''),
        c(" |   |   |   |   |   |   |  ", F.BRAUN),
        c(" 📚 📚 📚 📚 📚 📚 📚 📚  ", ''),
        c("       Bibliothek            ", F.BRAUN + F.FETT),
    ],
    "markt": [
        c("  ⛺         ⛺         ⛺  ", F.GELB),
        c(" /  \\       /  \\       /  \\ ", F.GELB),
        c("|    |     |    |     |    | ", F.BRAUN),
        c("════════════════════════════ ", F.GRAU),
        c("  🍎  🧄  🪄   🍞  🔑      ", ''),
        c("         Marktplatz          ", F.GELB + F.FETT),
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
                "check":    lambda cmd, out, p: cmd.split()[0] == "ls" if cmd.split() else False,
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
                "check":    lambda cmd, out, p: cmd.split()[0] == "ls" if cmd.split() else False,
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
                "check": lambda cmd, out, p: cmd.split()[0] == "mkdir" and len(cmd.split()) > 1,
                "belohnung":"📜 Schriftrolle der Erschaffung",
                "lernziel": "mkdir = make directory – erstellt einen neuen Ordner",
            },
            {
                "id":    "touch_hoehle",
                "ziel":  "Lege Vorräte an: touch proviant.txt",
                "check": lambda cmd, out, p: cmd.split()[0] == "touch" and len(cmd.split()) > 1,
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
                "check": lambda cmd, out, p: cmd.split()[0] == "cat" and len(cmd.split()) > 1,
                "belohnung":"📜 Schriftrolle des Lesens",
                "lernziel": "cat datei.txt – zeigt den Inhalt einer Datei an",
            },
            {
                "id":    "echo_see",
                "ziel":  'Schreibe eine Nachricht: echo "Text" > datei.txt',
                "check": lambda cmd, out, p: cmd.split()[0] == "echo" and ">" in cmd,
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
        "ausgaenge": {"dorf": "Dorf"},
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
                "check": lambda cmd, out, p: cmd.split()[0] == "cp" and len(cmd.split()) >= 3,
                "belohnung":"📜 Schriftrolle des Kopierens",
                "lernziel": "cp quelle.txt ziel.txt – kopiert eine Datei (das Original bleibt!)",
            },
            {
                "id":    "mv_markt",
                "ziel":  "Benenne um: mv kopie.txt neues_exemplar.txt",
                "check": lambda cmd, out, p: cmd.split()[0] == "mv" and len(cmd.split()) >= 3,
                "belohnung":"📜 Schriftrolle der Bewegung",
                "lernziel": "mv alt.txt neu.txt – verschiebt oder benennt eine Datei um",
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
    aug_str  = "  Ausgänge: " + "   ".join(f"cd {k}" for k in aug)
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


# ── Dateisystem-Konzepterklärung ──────────────────────────────────────────────

def konzept_erklarung(spiel: 'Spiel | None' = None) -> str:
    """Gibt eine Erklärung des Dateisystems als String zurück."""
    b = spiel.basis if spiel else Path.home() / "linux_abenteuer"

    zeilen = [
        c("📚 DAS DATEISYSTEM – So funktioniert es:", F.GELB + F.FETT),
        "",
        c("  Denk dir den Computer wie ein riesiges Gebäude vor:", F.WEISS),
        c("  Jeder Ordner ist ein Zimmer, jede Datei ist ein Dokument.", F.WEISS),
        "",
        c("  Dein Abenteuer-Ordner sieht so aus:", F.CYAN),
        "",
        c(f"  📦 {b.parent.name}/", F.GRAU) + c("                    ← Home-Verzeichnis", F.GRAU),
        c(f"  └── 📦 {b.name}/", F.WEISS) + c("             ← Unser Spielbereich", F.WEISS),
        c("       ├── 🏠 dorf/", F.GELB) + c("            ← Ordner (= Zimmer)", F.GRAU),
        c("       │   └── 📄 aushang.txt", F.WEISS) + c("  ← Datei (= Dokument)", F.GRAU),
        c("       ├── 🌲 wald/", F.GRUEN) + c("            ← noch ein Ordner", F.GRAU),
        c("       │   └── 📦 hoehle/", F.CYAN) + c("       ← Ordner im Ordner!", F.GRAU),
        c("       ├── 🌊 see/", F.BLAU),
        c("       └── 🏪 markt/", F.GELB),
        "",
        c("  ┌─────────────────────────────────────────────┐", F.CYAN),
        c("  │  WICHTIGE BEGRIFFE:                         │", F.CYAN + F.FETT),
        c("  │                                             │", F.CYAN),
        c("  │  Ordner / Verzeichnis  = Container für      │", F.WEISS),
        c("  │                          Dateien & Ordner   │", F.WEISS),
        c("  │  Datei                 = Inhalt             │", F.WEISS),
        c("  │                          (Text, Bilder...)  │", F.WEISS),
        c("  │  Pfad    = Adresse:  wald/hoehle/datei.txt  │", F.WEISS),
        c("  │  /       = Trenner zwischen Ordnern         │", F.WEISS),
        c("  │  ~       = Dein Home-Verzeichnis            │", F.WEISS),
        c("  │  .       = Aktueller Ordner                 │", F.WEISS),
        c("  │  ..      = Übergeordneter Ordner (zurück)   │", F.WEISS),
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
    for raum_id in ("dorf", "wald", "see", "markt"):
        (basis / raum_id).mkdir(exist_ok=True)
    (basis / "wald" / "hoehle").mkdir(exist_ok=True)

    def schreibe(pfad: Path, inhalt: str):
        if not pfad.exists():
            pfad.write_text(inhalt)

    schreibe(basis / "dorf" / "aushang.txt",
        "GESUCHT: Tapfere Abenteurerin!\n"
        "Sieben Schriftrollen muessen gerettet werden!\n"
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
                "  rm x.txt    – Datei löschen\n"
                "SPIELBEFEHLE:\n"
                "  schau  – Mit NPC sprechen (Quest holen)\n"
                "  karte  – Weltkarte anzeigen\n"
                "  inventar / status – Fortschritt anzeigen\n"
                "  konzept – Dateisystem-Erklärung\n"
                "  beenden – Spiel beenden (Fortschritt gespeichert)"
            )
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "karte":
            nachricht = (
                "     🗺️  WELTKARTE:\n"
                "          [🌲 Wald]\n"
                "             │\n"
                " [🌊 See]──[🏠 Dorf]──[🏪 Markt]\n"
                "             │\n"
                "          [🏰 Burg] (kommt später)\n"
                "\n"
                "Reisen mit: cd wald   cd see   cd markt   cd dorf"
            )
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "inventar":
            if spiel.scrolls:
                zeilen = "\n".join(f"  {s}" for s in spiel.scrolls)
                nachricht = f"📚 Deine Schriftrollen ({len(spiel.scrolls)}/9):\n{zeilen}"
            else:
                nachricht = "Du hast noch keine Schriftrollen.\nSpreche mit einem NPC (schau) um eine Quest zu bekommen!"
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "status":
            total = sum(len(r.get("quests", [])) for r in RAEUME.values())
            getan = len(spiel.abschluss)
            nachricht = f"Quests: {getan}/{total}   Schriftrollen: {len(spiel.scrolls)}/9\nBesuche alle Orte um alle Schriftrollen zu finden!"
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "konzept":
            nachricht = konzept_erklarung(spiel)
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd == "schau":
            zeige_dialog = True
            spiel.terminal.append((cmd, ''))
            continue

        if basis_cmd in ("beenden", "exit", "quit"):
            spiel.speichern()
            print(c("\n  Bis zum nächsten Abenteuer! 👋\n", F.GELB))
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
                    nachricht     = "Du gehst zurück zum Dorfplatz 🏠"
                else:
                    anim_reise(spiel.aktuell.name, neues.name)
                    spiel.aktuell = neues
                    zeige_dialog  = True
                    nachricht     = f"Willkommen zurück in: {spiel.raum()['name']}"
            else:
                # Zuerst relativ zum aktuellen Verzeichnis suchen,
                # dann als Top-Level-Raum (z.B. "cd dorf" von überall)
                neues = (spiel.aktuell / ziel).resolve()
                if not neues.exists():
                    neues = (spiel.basis / ziel).resolve()
                if not str(neues).startswith(str(spiel.basis)):
                    nachricht = "⚠️  Das liegt außerhalb des Abenteuerlandes!"
                elif not neues.exists():
                    verfuegbar = list(spiel.raum().get("ausgaenge", {}).keys())
                    nachricht = (
                        f"'{ziel}' gibt es hier nicht.\n"
                        f"Ausgänge: {', '.join(verfuegbar)}"
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
            nachricht = "✅ Ausgeführt!"
        else:
            nachricht = f"❌ Fehler (Code {rc})"

        spiel.speichern()

        # Sieg-Check: alle 9 Schriftrollen gesammelt
        if len(spiel.scrolls) >= 9:
            time.sleep(0.8)
            anim_sieg()
            clr()
            print()
            print(c('╔' + '═' * (W - 2) + '╗', F.GELB + F.FETT))
            print(c(f"║{'🎉  DER FLUCH IST GEBROCHEN!  🎉'.center(W-2)}║", F.GELB + F.FETT))
            print(c('╚' + '═' * (W - 2) + '╝', F.GELB + F.FETT))
            print()
            langsam(f"{spiel.spielerin}! Du hast alle 9 Schriftrollen gesammelt!", F.PINK, 0.04)
            langsam("Das Dorf Binaria ist gerettet! Die Dorfbewohner jubeln!", F.WEISS, 0.03)
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
        "Das Dorf Binaria wurde vom bösen Zauberer 'rm -rf'",
        "verflucht! Alle Magie ist verschwunden.",
        "",
        "Nur du, Mia – mutige Abenteurerin – kannst helfen!",
        "Sammle alle 7 magischen Schriftrollen, die über die",
        "Lande verstreut sind, um den Fluch zu brechen!",
        "",
        "Jede Schriftrolle lehrt dir einen echten Linux-Befehl.",
        "Tippe 'hilfe' wenn du nicht weiterkommst.",
        "Tippe 'karte' für die Weltkarte.",
        "Tippe 'schau' um mit dem NPC zu sprechen.",
    ]
    for z in geschichte:
        row = f"  {z}"
        print(c('║', F.PINK) + c(row, F.WEISS) + ' ' * max(0, W - 2 - len(row)) + c('║', F.PINK))

    print(c('╠' + '─' * (W - 2) + '╣', F.PINK))
    eingabe_zeile = c("  Wie heißt du, Abenteurerin? ", F.GELB)
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
    print(c(f"║{'  ⚔️  Linux-Spickzettel für Mia  ⚔️  '.center(S-2)}║", F.CYAN + F.FETT))
    print(c('╠' + '═' * (S - 2) + '╣', F.CYAN + F.FETT))

    print(c(f"║  {c('NAVIGATION', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("pwd",             "Aktuellen Pfad anzeigen")
    row("ls",              "Ordnerinhalt anzeigen")
    row("ls -l",           "Mit Details (Datum, Größe)")
    row("cd ordner",       "In Ordner wechseln")
    row("cd ..",           "Eine Ebene zurück")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))
    print(c(f"║  {c('ERSTELLEN', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("mkdir name",      "Neuen Ordner erstellen")
    row("touch datei.txt", "Neue leere Datei erstellen")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))
    print(c(f"║  {c('LESEN & SCHREIBEN', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("cat datei.txt",   "Dateiinhalt anzeigen")
    row('echo "text"',     "Text ausgeben")
    row('echo "t" > datei',"In Datei schreiben")
    row('echo "t" >>datei',"An Datei anhängen")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))
    print(c(f"║  {c('KOPIEREN / VERSCHIEBEN / LÖSCHEN', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("cp quelle ziel",  "Datei kopieren")
    row("mv alt neu",      "Verschieben/umbenennen")
    row("rm datei.txt",    "Löschen (ACHTUNG: endgültig!)")
    row("rmdir ordner",    "Leeren Ordner löschen")
    print(c('║' + ' ' * (S - 2) + '║', F.CYAN))
    print(c(f"║  {c('HILFE', F.GELB + F.FETT):<{S+9}}║", F.CYAN))
    row("befehl --help",   "Kurze Hilfe")
    row("man befehl",      "Ausführliches Handbuch")
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
        print(c("  Spielstand gelöscht. Viel Spaß beim neuen Abenteuer!\n", F.GELB))

    basis = Path.home() / "linux_abenteuer"
    welt_aufbauen(basis)

    name  = startbildschirm()
    spiel = Spiel(basis, name)
    spiel.laden()

    if not spiel.scrolls:
        clr()
        # Kurze Dateisystem-Einführung für Erstbenutzer
        print(c('╔' + '═' * (W - 2) + '╗', F.CYAN))
        print(c(f"║{'  📚 Kurze Erklärung – was ist ein Dateisystem?  '.center(W-2)}║", F.CYAN + F.FETT))
        print(c('╠' + '═' * (W - 2) + '╣', F.CYAN))
        erklaerung = [
            "Ein Computer speichert alles in Dateien und Ordnern –",
            "genau wie ein echter Aktenschrank:",
            "",
            "  📦 Ordner  = Ein Fach im Aktenschrank",
            "               Kann andere Ordner oder Dateien enthalten",
            "  📄 Datei   = Ein Dokument im Fach",
            "               Enthält Text, Bilder, Programme ...",
            "",
            "  Ordner können ineinander geschachtelt sein:",
            "  musik/ → rock/ → song.mp3",
            "",
            "  pwd zeigt dir wo du gerade bist.",
            "  ls  zeigt dir was in deinem Ordner liegt.",
            "  cd  bringt dich in einen anderen Ordner.",
            "",
            "  Im Spiel = jeder Raum ist ein echter Ordner auf deinem PC!",
            "  Tippe 'konzept' um diese Erklärung nochmal zu sehen.",
        ]
        for z in erklaerung:
            row = f"  {z}"
            print(c('║', F.CYAN) + c(row, F.WEISS) + ' ' * max(0, W - 2 - len(row)) + c('║', F.CYAN))
        print(c('╚' + '═' * (W - 2) + '╝', F.CYAN))
        print()
        langsam(f"Willkommen, {name}! Dein Abenteuer beginnt!", F.PINK, 0.05)
        print()
        print(c("  💡 Tipps:", F.GELB + F.FETT))
        print(c("     schau    → NPC ansprechen (Quest bekommen)", F.GELB))
        print(c("     hilfe    → alle Befehle anzeigen", F.GELB))
        print(c("     karte    → Weltkarte anzeigen", F.GELB))
        print(c("     konzept  → Dateisystem-Erklärung", F.GELB))
        print()
        input(c("  ↵ Los geht's!", F.CYAN) + "  ")

    try:
        spielschleife(spiel)
    except KeyboardInterrupt:
        print(c("\n\n  Gespeichert! Bis zum nächsten Abenteuer! 👋\n", F.GELB))
        spiel.speichern()


if __name__ == "__main__":
    main()
