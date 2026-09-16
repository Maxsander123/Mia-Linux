#!/usr/bin/env python3
"""
Mia lernt Linux! 🐧
Ein spielerisches Linux-Terminal-Abenteuer für Anfänger
mit visueller Darstellung des Dateisystems
"""

import os
import sys
import subprocess
import shutil
import time
import random
from pathlib import Path


# ── Terminal-Breite ───────────────────────────────────────────────────────────

try:
    BREITE = min(os.get_terminal_size().columns, 90)
except OSError:
    BREITE = 80

BREITE = max(BREITE, 72)


# ── ANSI-Farben ───────────────────────────────────────────────────────────────

class F:
    PINK   = '\033[95m'
    BLAU   = '\033[94m'
    GRUEN  = '\033[92m'
    GELB   = '\033[93m'
    ROT    = '\033[91m'
    CYAN   = '\033[96m'
    WEISS  = '\033[97m'
    GRAU   = '\033[90m'
    FETT   = '\033[1m'
    KURSIV = '\033[3m'
    RESET  = '\033[0m'

def c(text, *farben):
    return ''.join(farben) + str(text) + F.RESET


def clr():
    os.system('clear' if os.name != 'nt' else 'cls')


def langsam(text, farbe=F.WEISS, delay=0.025, indent=2):
    print(' ' * indent, end='')
    for zeichen in text:
        print(f"{farbe}{zeichen}{F.RESET}", end='', flush=True)
        time.sleep(delay)
    print()


def warte(prompt="Drücke ENTER um weiterzumachen …"):
    print()
    input(f"  {F.GELB}↵  {prompt}{F.RESET}  ")
    print()


# ── Box-Zeichnen ──────────────────────────────────────────────────────────────

def box_linie(breite, links='┌', mitte='─', rechts='┐'):
    return links + mitte * (breite - 2) + rechts

def box_mitte(inhalt, breite, links='│', rechts='│', farbe=''):
    sichtbar = len(inhalt) - sum(
        len(seq) for seq in __import__('re').findall(r'\033\[[0-9;]*m', inhalt)
    )
    leer = breite - 2 - sichtbar
    return f"{links}{farbe}{inhalt}{F.RESET}{' ' * max(0, leer)}{rechts}"

def box_trenn(breite, links='├', mitte='─', rechts='┤'):
    return links + mitte * (breite - 2) + rechts


# ── Dateisystem-Visualisierung ────────────────────────────────────────────────

def fs_baum(basis: Path, highlight=None, aktuell=None, max_tiefe=4) -> list[str]:
    """Gibt ASCII-Baum-Zeilen zurück."""
    zeilen = []

    def symbol(p: Path) -> str:
        if p.is_dir():
            return '📁'
        ext = p.suffix.lower()
        if ext in ('.txt', '.md'): return '📄'
        if ext in ('.py',):        return '🐍'
        if ext in ('.sh',):        return '⚙️ '
        return '📄'

    def rekursiv(pfad: Path, prefix: str, tiefe: int):
        if tiefe > max_tiefe:
            return
        try:
            eintraege = sorted(pfad.iterdir(), key=lambda x: (x.is_file(), x.name))
        except PermissionError:
            return
        for i, eintrag in enumerate(eintraege):
            ist_letzter = (i == len(eintraege) - 1)
            conn  = '└── ' if ist_letzter else '├── '
            naech = '    ' if ist_letzter else '│   '
            sym   = symbol(eintrag)
            name  = eintrag.name + ('/' if eintrag.is_dir() else '')

            # Farbe
            if eintrag == aktuell:
                name_col = c(name, F.CYAN, F.FETT) + c(' ◀ du', F.CYAN)
            elif highlight and eintrag.name == highlight:
                name_col = c(name, F.GELB, F.FETT) + c(' ✨neu', F.GELB)
            elif eintrag.is_dir():
                name_col = c(name, F.BLAU, F.FETT)
            else:
                name_col = c(name, F.WEISS)

            zeilen.append(f"{prefix}{conn}{sym} {name_col}")

            if eintrag.is_dir():
                rekursiv(eintrag, prefix + naech, tiefe + 1)

    # Wurzel
    wurzel_name = basis.name + '/'
    if aktuell == basis:
        zeilen.append(c('📂 ' + wurzel_name, F.CYAN, F.FETT) + c(' ◀ du', F.CYAN))
    else:
        zeilen.append(c('📂 ' + wurzel_name, F.BLAU, F.FETT))
    rekursiv(basis, '', 0)

    if not zeilen[1:]:
        zeilen.append(c('   (leer)', F.GRAU))
    return zeilen


# ── Split-Screen Anzeige ──────────────────────────────────────────────────────

class Bildschirm:
    """Zeigt Dateisystem und Terminal nebeneinander."""

    def __init__(self, basis: Path):
        self.basis = basis
        self.terminal_verlauf: list[tuple[str, str]] = []  # [(befehl, ausgabe)]
        self.aktuell: Path = basis
        self.hervorheben: str | None = None

    def zeichne(self, titel: str, nachricht: str = '', lektion_nr: int = 0):
        clr()
        fs_zeilen = fs_baum(self.basis, self.hervorheben, self.aktuell)

        # ── Kopfzeile ──
        kopf = f" 🐧 Mia lernt Linux"
        if lektion_nr:
            kopf += f"  │  Lektion {lektion_nr}"
        if titel:
            kopf += f"  │  {titel}"
        print(c('═' * BREITE, F.PINK))
        kopf_sicht = len(kopf) - sum(
            len(s) for s in __import__('re').findall(r'\033\[[0-9;]*m', kopf)
        )
        rand = (BREITE - kopf_sicht) // 2
        print(' ' * rand + kopf)
        print(c('═' * BREITE, F.PINK))
        print()

        # ── Split-Berechnung ──
        FS_BREITE = min(34, BREITE // 3)
        TERM_BREITE = BREITE - FS_BREITE - 3

        # ── Dateisystem-Panel ──
        fs_header = c(' 📂 Dein Übungsbereich', F.FETT + F.BLAU)
        term_header = c(' 💻 Terminal-Verlauf', F.FETT + F.GRUEN)

        print(
            box_linie(FS_BREITE, '┌', '─', '┬') +
            box_linie(TERM_BREITE + 1, '─', '─', '┐')
        )
        print(
            box_mitte(fs_header,   FS_BREITE,   '│', '│') +
            box_mitte(term_header, TERM_BREITE, '│', '│')
        )
        print(
            box_trenn(FS_BREITE, '├', '─', '┼') +
            box_trenn(TERM_BREITE + 1, '─', '─', '┤')
        )

        # Letzte Terminal-Einträge sammeln
        term_zeilen: list[str] = []
        for befehl, ausgabe in self.terminal_verlauf[-8:]:
            prompt_str = str(self.aktuell.relative_to(self.basis.parent))
            term_zeilen.append(c(f"$ {befehl}", F.GRUEN))
            if ausgabe:
                for zeile in ausgabe.splitlines()[:4]:
                    if len(zeile) > TERM_BREITE - 4:
                        zeile = zeile[:TERM_BREITE - 7] + '...'
                    term_zeilen.append(c(f"  {zeile}", F.WEISS))

        max_zeilen = max(len(fs_zeilen), len(term_zeilen), 6)

        for i in range(max_zeilen):
            fs_z = fs_zeilen[i] if i < len(fs_zeilen) else ''
            term_z = term_zeilen[i] if i < len(term_zeilen) else ''

            # sichtbare Länge für Auffüllung
            def sicht(s):
                return len(s) - sum(len(x) for x in __import__('re').findall(r'\033\[[0-9;]*m', s))

            fs_leer = FS_BREITE - 2 - min(sicht(fs_z), FS_BREITE - 4)
            term_leer = TERM_BREITE - 2 - min(sicht(term_z), TERM_BREITE - 4)

            fs_cell = f"│ {fs_z}{' ' * max(0, fs_leer - 1)}│"
            term_cell = f" {term_z}{' ' * max(0, term_leer)}│"
            print(fs_cell + term_cell)

        print(
            '└' + '─' * (FS_BREITE - 2) + '┴' +
            '─' * TERM_BREITE + '┘'
        )

        # ── Nachricht / Erklärung ──
        if nachricht:
            print()
            for zeile in nachricht.split('\n'):
                print(f"  {zeile}")

    def befehl_ausfuehren(self, befehl: str) -> tuple[int, str, str]:
        try:
            erg = subprocess.run(
                befehl, shell=True, capture_output=True, text=True,
                cwd=str(self.aktuell), timeout=10
            )
            # cd separat
            teile = befehl.strip().split()
            if teile and teile[0] == 'cd':
                ziel = teile[1] if len(teile) > 1 else str(Path.home())
                if ziel == '..':
                    neues = self.aktuell.parent
                elif ziel == '~':
                    neues = Path.home()
                else:
                    neues = (self.aktuell / ziel).resolve()
                if neues.exists() and str(neues).startswith(str(self.basis)):
                    self.aktuell = neues
                    return 0, '', ''
            return erg.returncode, erg.stdout.strip(), erg.stderr.strip()
        except subprocess.TimeoutExpired:
            return 1, '', 'Zeitüberschreitung'

    def eingabe(self, aufgabe: str, titel: str, lektion_nr: int,
                pruefen, max_versuche=6) -> bool:
        versuche = 0
        nachricht = c(f"  📝 Aufgabe: {aufgabe}", F.GELB + F.FETT)
        while True:
            self.zeichne(titel, nachricht, lektion_nr)
            prompt = c(
                f"\n  {str(self.aktuell.relative_to(self.basis.parent))}$ ",
                F.GRUEN
            )
            print(prompt, end='')
            try:
                befehl = input().strip()
            except EOFError:
                break
            if not befehl:
                continue
            versuche += 1
            rc, out, err = self.befehl_ausfuehren(befehl)
            ausgabe = out or err or ''
            self.terminal_verlauf.append((befehl, ausgabe))

            ok, meldung = pruefen(self, out, err, befehl)
            if ok:
                self.hervorheben = None
                self.zeichne(titel, '', lektion_nr)
                print()
                print(c(f"  ✅  {meldung}", F.GRUEN + F.FETT))
                warte("Weiter zur nächsten Aufgabe …")
                return True
            else:
                if versuche >= max_versuche:
                    self.zeichne(titel, '', lektion_nr)
                    print(c(f"\n  ℹ️  Kein Problem! Wir üben das nochmal später.", F.CYAN))
                    warte()
                    return False
                nachricht = (
                    c(f"  📝 Aufgabe: {aufgabe}\n", F.GELB + F.FETT) +
                    c(f"\n  ❌  {meldung}", F.ROT) +
                    c(f"\n  💡 Versuch {versuche}/{max_versuche}", F.GRAU)
                )


# ── ASCII-Animationen ─────────────────────────────────────────────────────────

def anim_datei_erstellen(name: str):
    clr()
    frames = [
        ["         ", "  ┌────┐  ", "  │    │  ", "  │    │  ", "  └────┘  "],
        ["         ", "  ┌────┐  ", "  │ ✏️ │  ", "  │    │  ", "  └────┘  "],
        ["         ", "  ┌────┐  ", "  │ ✏️ │  ", f"  │{name[:4]:^4}│  ", "  └────┘  "],
        [c("  ✨ NEUE DATEI ERSTELLT ✨", F.GELB + F.FETT),
         c("  ┌────────┐", F.GRUEN),
         c(f"  │  📄    │", F.GRUEN),
         c(f"  │ {name[:6]:<6} │", F.GRUEN),
         c("  └────────┘", F.GRUEN)],
    ]
    for frame in frames:
        clr()
        print()
        print(c(f"  ⚙️  Führe aus: touch {name}", F.CYAN))
        print()
        for zeile in frame:
            print(f"     {zeile}")
        time.sleep(0.4)


def anim_ordner_erstellen(name: str):
    frames = [
        ["       ", "  ╔══╗ ", "  ║  ║ ", "  ╚══╝ "],
        ["       ", "  ╔═══╗", "  ║   ║", "  ╚═══╝"],
        [c(f"  ✨ ORDNER '{name}' ERSTELLT ✨", F.GELB + F.FETT),
         c("  ╔══════════╗", F.BLAU + F.FETT),
         c(f"  ║  📁 {name[:8]:<8}║", F.BLAU + F.FETT),
         c("  ╚══════════╝", F.BLAU + F.FETT)],
    ]
    for frame in frames:
        clr()
        print()
        print(c(f"  ⚙️  Führe aus: mkdir {name}", F.CYAN))
        print()
        for zeile in frame:
            print(f"     {zeile}")
        time.sleep(0.45)


def anim_loeschen(name: str):
    frames = [
        [c(f"  📄 {name}", F.WEISS)],
        [c(f"  📄 {name}", F.GELB)],
        [c(f"  📃 {name}  ← wird gelöscht…", F.ROT)],
        [c(f"  ✂️  {name}", F.ROT)],
        [c(f"  🗑️  … weg!", F.GRAU)],
    ]
    for frame in frames:
        clr()
        print()
        print(c(f"  ⚙️  Führe aus: rm {name}", F.CYAN))
        print()
        for zeile in frame:
            print(f"     {zeile}")
        time.sleep(0.35)


def anim_kopieren(von: str, nach: str):
    frames = [
        [f"  📄 {von}             "],
        [f"  📄 {von}  ──┐        "],
        [f"  📄 {von}  ──┤ kopiert"],
        [f"  📄 {von}  ──┘  📄 {nach}"],
    ]
    for frame in frames:
        clr()
        print()
        print(c(f"  ⚙️  Führe aus: cp {von} {nach}", F.CYAN))
        print()
        for zeile in frame:
            print(c(f"     {zeile}", F.GRUEN))
        time.sleep(0.4)


def anim_verschieben(von: str, nach: str):
    frames = [
        [c(f"  📄 {von}              ─┐", F.WEISS)],
        [c(f"  📄 {von}  ──────────── │", F.GELB)],
        [c(f"     {' ' * len(von)}  ──────────── │", F.GRAU)],
        [c(f"     {' ' * len(von)}               └─▶ 📄 {nach}", F.GRUEN + F.FETT)],
    ]
    for frame in frames:
        clr()
        print()
        print(c(f"  ⚙️  Führe aus: mv {von} {nach}", F.CYAN))
        print()
        for zeile in frame:
            print(f"     {zeile}")
        time.sleep(0.4)


def anim_cd(ziel: str, aktuell: str):
    arrows = ['·', '>', '>>', '>>>']
    for arrow in arrows:
        clr()
        print()
        print(c(f"  ⚙️  Führe aus: cd {ziel}", F.CYAN))
        print()
        print(c(f"     📍 {aktuell} {arrow} 📁 {ziel}", F.CYAN))
        time.sleep(0.3)


def anim_cat(inhalt: str, datei: str):
    clr()
    print()
    print(c(f"  ⚙️  Führe aus: cat {datei}", F.CYAN))
    print()
    print(c("  ┌─── Inhalt der Datei ───────────────────┐", F.CYAN))
    for zeile in inhalt.splitlines()[:8]:
        zeile = zeile[:42]
        print(c(f"  │  {zeile:<42}│", F.CYAN))
    print(c("  └──────────────────────────────────────┘", F.CYAN))
    time.sleep(1.2)


# ── Lektionen ─────────────────────────────────────────────────────────────────

def lektion_0_intro(screen: Bildschirm):
    clr()
    print(c('═' * BREITE, F.PINK))
    titel = "  🐧  Willkommen bei Mia lernt Linux!  🐧  "
    print(c(titel.center(BREITE), F.PINK + F.FETT))
    print(c('═' * BREITE, F.PINK))
    print()
    time.sleep(0.3)
    langsam("Hallo! Schön, dass du da bist! 🎉", F.PINK, 0.04)
    print()
    langsam("Du bist kurz davor, eine ganz neue Welt zu entdecken –", F.WEISS, 0.03)
    langsam("die Welt der Linux-Kommandozeile! 🌍", F.WEISS, 0.03)
    print()
    print(c("  Wie das funktioniert:", F.GELB + F.FETT))
    print()
    items = [
        ("📂", "Links siehst du immer deinen Übungsbereich (Dateisystem)"),
        ("💻", "Rechts siehst du die Befehle, die du schon eingegeben hast"),
        ("🎯", "Unten kannst du Befehle eintippen – ganz ohne Angst!"),
        ("✨", "Animationen zeigen dir, was bei jedem Befehl passiert"),
        ("💡", "Tipps helfen dir weiter wenn du nicht weiterkommst"),
    ]
    for emoji, text in items:
        print(f"    {emoji}  {c(text, F.WEISS)}")
        time.sleep(0.15)
    print()
    print(c("  Hier kann nichts kaputt gehen – alles passiert in", F.GRUEN))
    print(c("  einem sicheren Übungsordner auf deinem Computer.", F.GRUEN))
    print()
    warte("Los geht's! Drücke ENTER …")


def lektion_1_pwd(screen: Bildschirm):
    NR = 1
    TITEL = "pwd – Wo bin ich?"

    clr()
    screen.zeichne(TITEL, '', NR)
    print()
    print(c("  Stell dir vor, du bist in einem riesigen Gebäude.", F.WEISS))
    print(c("  Du möchtest wissen: 'In welchem Raum bin ich gerade?'", F.WEISS))
    print()
    print(c("  In Linux fragst du das mit:", F.WEISS))
    print()
    print(c("      pwd", F.GRUEN + F.FETT))
    print()
    print(c("  pwd = print working directory", F.KURSIV + F.CYAN))
    print(c("  Zu Deutsch: 'Zeig mir meinen aktuellen Ordner'", F.KURSIV + F.CYAN))
    print()
    print(c("  💡 Tipp: Einfach 'pwd' eintippen und ENTER drücken", F.GELB))
    warte()

    def check(sh, out, err, cmd):
        if 'pwd' in cmd.lower():
            if out:
                return True, f"Super! Du bist hier: {out}"
            return True, "pwd hat funktioniert!"
        return False, "Tippe einfach: pwd"

    screen.eingabe(
        "Finde heraus, in welchem Ordner du gerade bist",
        TITEL, NR, check
    )


def lektion_2_ls(screen: Bildschirm):
    NR = 2
    TITEL = "ls – Was ist hier?"

    # Beispieldateien anlegen
    (screen.basis / "notizen.txt").write_text("Meine erste Datei!\n")
    (screen.basis / "bilder").mkdir(exist_ok=True)
    (screen.basis / "musik").mkdir(exist_ok=True)

    clr()
    screen.zeichne(TITEL, '', NR)
    print()
    print(c("  Du kennst jetzt deinen Standort.", F.WEISS))
    print(c("  Aber was liegt in diesem Ordner?", F.WEISS))
    print()
    print(c("  Den Inhalt siehst du mit:", F.WEISS))
    print()
    print(c("      ls", F.GRUEN + F.FETT))
    print()
    print(c("  ls = list   →   Zeig mir alles, was hier ist", F.KURSIV + F.CYAN))
    print()
    print(c("  Noch mehr Details mit:", F.WEISS))
    print(c("      ls -l        (Größe, Datum, Rechte)", F.GRUEN))
    print(c("      ls -lh       (Größe in KB/MB lesbar)", F.GRUEN))
    print()
    print(c("  💡 Tipp: Das '-l' ist ein Schalter – wie ein Lichtschalter", F.GELB))
    warte()

    def check(sh, out, err, cmd):
        if 'ls' in cmd.lower():
            if out or err == '':
                return True, "Wunderbar! Du siehst den Ordnerinhalt!"
        return False, "Tippe 'ls' um den Ordnerinhalt zu sehen"

    screen.eingabe(
        "Zeige den Inhalt des aktuellen Ordners an",
        TITEL, NR, check
    )


def lektion_3_cd(screen: Bildschirm):
    NR = 3
    TITEL = "cd – Woanders hingehen"

    screen.basis.joinpath("bilder").mkdir(exist_ok=True)
    screen.basis.joinpath("musik").mkdir(exist_ok=True)

    clr()
    screen.zeichne(TITEL, '', NR)
    print()
    print(c("  Jetzt weißt du, wo du bist und was hier ist.", F.WEISS))
    print(c("  Wie kommst du in einen anderen Ordner?", F.WEISS))
    print()
    print(c("      cd ordnername    →  wechsle in diesen Ordner", F.GRUEN + F.FETT))
    print(c("      cd ..            →  eine Ebene zurück", F.GRUEN + F.FETT))
    print(c("      cd ~             →  direkt nach Hause (Home)", F.GRUEN + F.FETT))
    print()
    print(c("  cd = change directory", F.KURSIV + F.CYAN))
    print()
    print(c("  💡 Tipp: Erst 'ls' tippen um Ordner zu sehen, dann 'cd ordner'", F.GELB))
    warte()

    # Schritt 1: rein
    alter_pfad = str(screen.aktuell.name)

    def check_rein(sh, out, err, cmd):
        if sh.aktuell != sh.basis:
            anim_cd(sh.aktuell.name, alter_pfad)
            return True, f"Super! Du bist jetzt in '{sh.aktuell.name}'! 🎉"
        if 'cd' in cmd.lower():
            return False, "Versuch: cd bilder   oder: cd musik"
        return False, "Benutze: cd ordnername    Beispiel: cd bilder"

    screen.eingabe(
        "Wechsle in den Ordner 'bilder' (oder 'musik')",
        TITEL, NR, check_rein
    )

    # Schritt 2: raus
    def check_raus(sh, out, err, cmd):
        if sh.aktuell == sh.basis:
            return True, "Perfekt! Du bist wieder zurück! cd .. funktioniert!"
        if 'cd' in cmd:
            return False, "Nochmal versuchen: cd .."
        return False, "Benutze: cd ..   (zwei Punkte = eine Ebene zurück)"

    screen.eingabe(
        "Gehe mit 'cd ..' wieder zurück",
        TITEL + " (zurück)", NR, check_raus
    )


def lektion_4_mkdir(screen: Bildschirm):
    NR = 4
    TITEL = "mkdir – Neuen Ordner erstellen"

    clr()
    screen.zeichne(TITEL, '', NR)
    print()
    print(c("  Neue Ordner erstellen – kein Problem!", F.WEISS))
    print()
    print(c("      mkdir ordnername", F.GRUEN + F.FETT))
    print()
    print(c("  mkdir = make directory   →   Erstelle einen Ordner", F.KURSIV + F.CYAN))
    print()
    print(c("  Beispiele:", F.WEISS))
    print(c("      mkdir meine_fotos", F.GRUEN))
    print(c("      mkdir urlaub_2025", F.GRUEN))
    print(c("      mkdir rezepte", F.GRUEN))
    print()
    print(c("  💡 Tipp: Keine Leerzeichen! Nutze _ statt Leerzeichen", F.GELB))
    warte()

    def check(sh, out, err, cmd):
        name = ''
        if 'mkdir' in cmd.lower():
            teile = cmd.split()
            if len(teile) > 1:
                name = teile[1]
                neuer = sh.basis / name
                if neuer.exists():
                    anim_ordner_erstellen(name)
                    sh.hervorheben = name
                    return True, f"🎊 Dein Ordner '{name}' wurde erstellt!"
            return False, "Gib auch einen Namen an: mkdir mein_ordner"
        return False, "Benutze: mkdir ordnername"

    screen.eingabe(
        "Erstelle einen Ordner mit einem Namen deiner Wahl",
        TITEL, NR, check
    )
    screen.hervorheben = None


def lektion_5_touch(screen: Bildschirm):
    NR = 5
    TITEL = "touch – Neue Datei erstellen"

    clr()
    screen.zeichne(TITEL, '', NR)
    print()
    print(c("  Ordner für Kategorien – Dateien für Inhalte.", F.WEISS))
    print(c("  Eine leere Datei erstellst du so:", F.WEISS))
    print()
    print(c("      touch dateiname.txt", F.GRUEN + F.FETT))
    print()
    print(c("  touch = berühren / erstellen", F.KURSIV + F.CYAN))
    print(c("  '.txt' = Textdatei (wie ein Word-Dokument, nur einfacher)", F.KURSIV + F.CYAN))
    print()
    print(c("  Mehrere Dateien auf einmal:", F.WEISS))
    print(c("      touch datei1.txt datei2.txt datei3.txt", F.GRUEN))
    print()
    print(c("  💡 Tipp: Gib deiner Datei einen Namen, der dir gefällt!", F.GELB))
    warte()

    def check(sh, out, err, cmd):
        if 'touch' in cmd.lower():
            teile = cmd.split()
            if len(teile) > 1:
                name = teile[1]
                datei = sh.basis / name
                if datei.exists():
                    anim_datei_erstellen(name)
                    sh.hervorheben = name
                    return True, f"📄 '{name}' wurde erstellt!"
            return False, "Schreibe nach touch noch einen Namen: touch meine_datei.txt"
        return False, "Benutze: touch dateiname.txt"

    screen.eingabe(
        "Erstelle eine neue Textdatei – gib ihr deinen eigenen Namen",
        TITEL, NR, check
    )
    screen.hervorheben = None


def lektion_6_cat(screen: Bildschirm):
    NR = 6
    TITEL = "cat – Datei lesen"

    inhalt = (
        "Liebe Mia,\n\n"
        "Du lernst so schnell! Linux macht Spaß, oder?\n\n"
        "Liebe Grüße,\ndein Linux-Freund 🐧\n"
    )
    brief = screen.basis / "brief.txt"
    brief.write_text(inhalt)

    clr()
    screen.zeichne(TITEL, '', NR)
    print()
    print(c("  Was steht in einer Datei? Das zeigst du mit:", F.WEISS))
    print()
    print(c("      cat dateiname.txt", F.GRUEN + F.FETT))
    print()
    print(c("  cat = concatenate   →   eigentlich 'verketten',", F.KURSIV + F.CYAN))
    print(c("       aber wir benutzen es einfach zum Lesen von Dateien", F.KURSIV + F.CYAN))
    print()
    print(c("  Es gibt eine Datei 'brief.txt' hier – lies sie!", F.WEISS))
    print()
    print(c("  💡 Tipp: Erst 'ls' um alle Dateien zu sehen,", F.GELB))
    print(c("       dann: cat brief.txt", F.GELB))
    warte()

    def check(sh, out, err, cmd):
        if 'cat' in cmd.lower():
            if out:
                anim_cat(out, cmd.replace('cat', '').strip())
                return True, "Du hast die Datei gelesen! 💌 Hast du den Brief gesehen?"
            return True, "cat hat funktioniert!"
        return False, "Benutze: cat brief.txt"

    screen.eingabe(
        "Lies den Inhalt der Datei 'brief.txt'",
        TITEL, NR, check
    )


def lektion_7_echo(screen: Bildschirm):
    NR = 7
    TITEL = "echo – Text ausgeben und speichern"

    clr()
    screen.zeichne(TITEL, '', NR)
    print()
    print(c("  Mit 'echo' kannst du Text anzeigen und in Dateien schreiben.", F.WEISS))
    print()
    print(c('      echo "Hallo Welt!"         → Text anzeigen', F.GRUEN + F.FETT))
    print(c('      echo "Text" > datei.txt    → In Datei schreiben', F.GRUEN + F.FETT))
    print(c('      echo "Text" >> datei.txt   → An Datei anhängen', F.GRUEN + F.FETT))
    print()
    print(c("  >  = Datei neu erstellen (Vorsicht: überschreibt!)", F.KURSIV + F.CYAN))
    print(c("  >> = Text hinzufügen ohne zu überschreiben", F.KURSIV + F.CYAN))
    print()
    print(c('  💡 Tipp: Probiere: echo "Ich lerne Linux!" > mein_text.txt', F.GELB))
    warte()

    def check(sh, out, err, cmd):
        if 'echo' in cmd.lower():
            if '>' in cmd:
                return True, "Klasse! Du hast Text in eine Datei geschrieben! 🎯"
            if out:
                return True, f"Super! echo hat ausgegeben: {out[:50]}"
            return True, "echo hat geklappt!"
        return False, 'Benutze: echo "dein text"'

    screen.eingabe(
        'Schreibe etwas mit echo, z.B.: echo "Hallo Linux!"',
        TITEL, NR, check
    )


def lektion_8_cp(screen: Bildschirm):
    NR = 8
    TITEL = "cp – Dateien kopieren"

    (screen.basis / "original.txt").write_text("Ich bin das Original! Kopiere mich!\n")

    clr()
    screen.zeichne(TITEL, '', NR)
    print()
    print(c("  Dateien kopieren – wie Strg+C, Strg+V, aber im Terminal:", F.WEISS))
    print()
    print(c("      cp quelle.txt ziel.txt", F.GRUEN + F.FETT))
    print()
    print(c("  cp = copy   →   kopieren", F.KURSIV + F.CYAN))
    print()
    print(c("  Beispiel:", F.WEISS))
    print(c("      cp original.txt meine_kopie.txt", F.GRUEN))
    print()
    print(c("  Ordner kopieren:", F.WEISS))
    print(c("      cp -r ordner/ kopie/     (-r = mit Inhalt)", F.GRUEN))
    print()
    print(c("  💡 Tipp: Es gibt eine 'original.txt' hier – kopiere sie!", F.GELB))
    warte()

    def check(sh, out, err, cmd):
        if 'cp' in cmd.lower():
            teile = cmd.split()
            if len(teile) >= 3:
                ziel_name = teile[-1]
                ziel = sh.basis / ziel_name
                von_name = teile[1] if teile[1] != '-r' else teile[2]
                if ziel.exists() and ziel != sh.basis / 'original.txt':
                    anim_kopieren(von_name, ziel_name)
                    sh.hervorheben = ziel_name
                    return True, f"Kopie erstellt: '{ziel_name}' ✨"
            return True, "cp wurde ausgeführt!"
        return False, "Benutze: cp original.txt meine_kopie.txt"

    screen.eingabe(
        "Kopiere 'original.txt' und gib der Kopie einen neuen Namen",
        TITEL, NR, check
    )
    screen.hervorheben = None


def lektion_9_mv(screen: Bildschirm):
    NR = 9
    TITEL = "mv – Verschieben & Umbenennen"

    (screen.basis / "alt_name.txt").write_text("Ich heiße bald anders!\n")

    clr()
    screen.zeichne(TITEL, '', NR)
    print()
    print(c("  mv macht zwei Dinge in einem:", F.WEISS))
    print()
    print(c("  Datei umbenennen:", F.WEISS))
    print(c("      mv alter_name.txt neuer_name.txt", F.GRUEN + F.FETT))
    print()
    print(c("  Datei verschieben:", F.WEISS))
    print(c("      mv datei.txt ordner/datei.txt", F.GRUEN + F.FETT))
    print()
    print(c("  mv = move   →   bewegen / verschieben", F.KURSIV + F.CYAN))
    print(c("  (Die Originaldatei verschwindet, es gibt nur noch die neue!)", F.KURSIV + F.CYAN))
    print()
    print(c("  💡 Tipp: Benenne 'alt_name.txt' in etwas Schönes um!", F.GELB))
    warte()

    def check(sh, out, err, cmd):
        if 'mv' in cmd.lower():
            teile = cmd.split()
            if len(teile) >= 3:
                von = teile[1]
                nach = teile[-1]
                anim_verschieben(von, nach)
                return True, f"'{von}' wurde zu '{nach}' umbenannt/verschoben! 🚀"
            return True, "mv wurde ausgeführt!"
        return False, "Benutze: mv alt_name.txt mein_neuer_name.txt"

    screen.eingabe(
        "Benenne 'alt_name.txt' in einen anderen Namen um",
        TITEL, NR, check
    )


def lektion_10_rm(screen: Bildschirm):
    NR = 10
    TITEL = "rm – Löschen (mit Vorsicht!)"

    (screen.basis / "kann_weg.txt").write_text("Diese Datei darf weg!\n")

    clr()
    screen.zeichne(TITEL, '', NR)
    print()
    print(c("  ⚠️  ACHTUNG: rm löscht Dateien DAUERHAFT!", F.ROT + F.FETT))
    print(c("  Es gibt keinen Papierkorb in der Kommandozeile!", F.ROT))
    print()
    print(c("  Datei löschen:", F.WEISS))
    print(c("      rm dateiname.txt", F.GRUEN + F.FETT))
    print()
    print(c("  Leeren Ordner löschen:", F.WEISS))
    print(c("      rmdir ordnername", F.GRUEN + F.FETT))
    print()
    print(c("  Ordner MIT Inhalt löschen:", F.WEISS))
    print(c("      rm -r ordnername    (-r = alles darin auch löschen)", F.GRUEN + F.FETT))
    print()
    print(c("  💡 Tipp: Immer zweimal nachdenken bevor du löschst!", F.GELB))
    warte()

    def check(sh, out, err, cmd):
        datei = sh.basis / "kann_weg.txt"
        if 'rm' in cmd.lower() and 'kann_weg' in cmd:
            if not datei.exists():
                anim_loeschen("kann_weg.txt")
                return True, "Gelöscht! 🗑️ Für immer weg – daher: immer zweimal überlegen!"
            return False, "Versuche: rm kann_weg.txt"
        if 'rm' in cmd.lower():
            return False, "Lösche speziell 'kann_weg.txt': rm kann_weg.txt"
        return False, "Benutze: rm kann_weg.txt"

    screen.eingabe(
        "Lösche die Datei 'kann_weg.txt'",
        TITEL, NR, check
    )


def lektion_11_hilfe(screen: Bildschirm):
    NR = 11
    TITEL = "Hilfe holen – --help & man"

    clr()
    screen.zeichne(TITEL, '', NR)
    print()
    print(c("  Niemand kennt alle Befehle auswendig!", F.WEISS))
    print(c("  Das Wichtigste: wissen, wie man Hilfe bekommt.", F.WEISS))
    print()
    print(c("  Kurze Hilfe:", F.WEISS))
    print(c("      befehl --help    Beispiel: ls --help", F.GRUEN + F.FETT))
    print()
    print(c("  Ausführliches Handbuch:", F.WEISS))
    print(c("      man befehl       Beispiel: man ls", F.GRUEN + F.FETT))
    print(c("  (Im Handbuch: Scrollen mit ↑↓, beenden mit 'q')", F.KURSIV + F.CYAN))
    print()
    print(c("  Noch nützlicher im Internet:", F.WEISS))
    print(c("      → explainshell.com  (erklärt Befehle auf Englisch)", F.CYAN))
    print(c("      → tldr.sh           (kurze Beispiele)", F.CYAN))
    print()
    print(c("  💡 Tipp: 'ls --help' zeigt alle Optionen von ls", F.GELB))
    warte()

    def check(sh, out, err, cmd):
        if '--help' in cmd or ('man ' in cmd and len(cmd) > 4):
            return True, "Du weißt wie man Hilfe bekommt – das ist das Allerwichtigste! 📚"
        return False, "Versuche: ls --help"

    screen.eingabe(
        "Ruf die Hilfe für 'ls' auf:  ls --help",
        TITEL, NR, check
    )


def abschluss(screen: Bildschirm):
    clr()
    print(c('╔' + '═' * (BREITE - 2) + '╗', F.PINK + F.FETT))
    zeile = "  🎉  Herzlichen Glückwunsch! Du hast es geschafft!  🎉  "
    print(c(f"║{zeile.center(BREITE - 2)}║", F.PINK + F.FETT))
    print(c('╚' + '═' * (BREITE - 2) + '╝', F.PINK + F.FETT))
    print()
    langsam("WOW! Du hast alle Lektionen gemeistert!", F.PINK, 0.04)
    print()
    print(c("  Das weißt du jetzt:", F.GELB + F.FETT))
    lernziele = [
        ("pwd",    "Aktuellen Ordner anzeigen"),
        ("ls",     "Ordnerinhalt auflisten"),
        ("cd",     "In andere Ordner wechseln"),
        ("mkdir",  "Neue Ordner erstellen"),
        ("touch",  "Neue Dateien erstellen"),
        ("cat",    "Dateiinhalt lesen"),
        ("echo",   "Text ausgeben und speichern"),
        ("cp",     "Dateien kopieren"),
        ("mv",     "Dateien verschieben / umbenennen"),
        ("rm",     "Dateien löschen"),
        ("--help", "Hilfe holen"),
    ]
    for befehl, beschreibung in lernziele:
        print(f"    {c('✅', F.GRUEN)}  {c(befehl, F.GRUEN + F.FETT):<20} {c(beschreibung, F.WEISS)}")
        time.sleep(0.12)
    print()
    print(c("  " + "─" * (BREITE - 4), F.PINK))
    print()
    print(c("  Wenn du mehr lernen möchtest:", F.GELB + F.FETT))
    print(c("      nano datei.txt      – Text im Terminal bearbeiten", F.CYAN))
    print(c("      grep 'suche' datei  – Text in Dateien suchen", F.CYAN))
    print(c("      chmod +x script.sh  – Ausführungsrechte vergeben", F.CYAN))
    print(c("      apt install paket   – Programme installieren", F.CYAN))
    print()
    print(c("  Spickzettel anzeigen:", F.WEISS))
    print(c("      python3 mia_lernt_linux.py --spickzettel", F.GRUEN))
    print()
    print(c('  ' + '═' * (BREITE - 4), F.PINK))
    print(c("  Du rockst! 🌟💜🐧", F.PINK + F.FETT))
    print(c('  ' + '═' * (BREITE - 4), F.PINK))
    print()


def spickzettel():
    clr()
    SCHMAL = min(BREITE, 70)
    print(c('╔' + '═' * (SCHMAL - 2) + '╗', F.CYAN + F.FETT))
    titel = "  🐧  Linux-Spickzettel für Mia  🐧  "
    print(c(f"║{titel.center(SCHMAL - 2)}║", F.CYAN + F.FETT))
    print(c('╠' + '═' * (SCHMAL - 2) + '╣', F.CYAN + F.FETT))

    def abschnitt(titel):
        print(c(f"║ {c(titel, F.GELB + F.FETT):<{SCHMAL + 11}}║", F.CYAN))

    def zeile(befehl, beschreibung):
        eintrag = f"  {befehl:<22} {beschreibung}"
        print(c(f"║{c(eintrag, F.WEISS):<{SCHMAL + 8}}║", F.CYAN))

    def trenn():
        print(c('╠' + '─' * (SCHMAL - 2) + '╣', F.CYAN))

    abschnitt("NAVIGATION")
    zeile("pwd",             "Aktuellen Ordner anzeigen")
    zeile("ls",              "Ordnerinhalt anzeigen")
    zeile("ls -l",           "Mit Details (Größe, Datum)")
    zeile("ls -lh",          "Größe in KB/MB leserlich")
    zeile("cd ordner",       "In Ordner wechseln")
    zeile("cd ..",           "Eine Ebene zurück")
    zeile("cd ~",            "Zum Home-Ordner")
    trenn()
    abschnitt("ORDNER & DATEIEN")
    zeile("mkdir name",      "Neuen Ordner erstellen")
    zeile("touch datei.txt", "Leere Datei erstellen")
    zeile("cat datei.txt",   "Dateiinhalt anzeigen")
    zeile('echo "text"',     "Text ausgeben")
    zeile('echo "t" > datei',"Text in Datei schreiben")
    zeile('echo "t" >>datei',"Text anhängen")
    trenn()
    abschnitt("KOPIEREN / VERSCHIEBEN / LÖSCHEN")
    zeile("cp quelle ziel",  "Datei kopieren")
    zeile("cp -r ord/ kop/", "Ordner kopieren")
    zeile("mv quelle ziel",  "Verschieben / umbenennen")
    zeile("rm datei.txt",    "Datei löschen (ACHTUNG!)")
    zeile("rmdir ordner",    "Leeren Ordner löschen")
    zeile("rm -r ordner",    "Ordner + Inhalt löschen")
    trenn()
    abschnitt("HILFE")
    zeile("befehl --help",   "Kurze Hilfe zum Befehl")
    zeile("man befehl",      "Ausführliches Handbuch")
    print(c('╚' + '═' * (SCHMAL - 2) + '╝', F.CYAN + F.FETT))
    print()


# ── Hauptprogramm ─────────────────────────────────────────────────────────────

def main():
    if '--spickzettel' in sys.argv or '-s' in sys.argv:
        spickzettel()
        return

    # Übungsverzeichnis
    basis = Path.home() / "linux_uebungen"
    basis.mkdir(exist_ok=True)

    screen = Bildschirm(basis)

    try:
        lektion_0_intro(screen)
        lektion_1_pwd(screen)
        lektion_2_ls(screen)
        lektion_3_cd(screen)
        lektion_4_mkdir(screen)
        lektion_5_touch(screen)
        lektion_6_cat(screen)
        lektion_7_echo(screen)
        lektion_8_cp(screen)
        lektion_9_mv(screen)
        lektion_10_rm(screen)
        lektion_11_hilfe(screen)
        abschluss(screen)

    except KeyboardInterrupt:
        print()
        print()
        print(c("  Pause gemacht! Kein Problem. 👋", F.GELB))
        print(c("  Starte einfach neu: python3 mia_lernt_linux.py", F.WEISS))
        print(c("  Dein Übungsordner bleibt: ~/linux_uebungen", F.CYAN))
        print()


if __name__ == "__main__":
    main()
