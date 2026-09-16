#!/usr/bin/env python3
"""
build_game.py
Combines all content section files into the final mia_lernt_linux.py.
"""
from pathlib import Path

BASE    = Path("/home/maxsander/.claude/worktrees/mia-rpg")
GAME    = BASE / "mia_lernt_linux.py"
CONTENT = BASE / "content"


# ── Helper: find start/end of a dict in source text ──────────────────────────
def find_dict_bounds(text, start_marker):
    start = text.index(start_marker)
    depth = 0
    i = start
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return start, i + 1
        i += 1
    return start, len(text)


def extract_dict_body(text, start_marker):
    """Return the content *inside* the outermost braces of the named dict."""
    s, e = find_dict_bounds(text, start_marker)
    brace_pos = text.index('{', s)
    return text[brace_pos + 1 : e - 1]


# ── Normalize raeume_neu_b.py field names to match the game engine ────────────
def normalize_neu_b(text):
    text = text.replace('"aufgabe":', '"ziel":')
    text = text.replace('"lerninhalt":', '"lernziel":')
    # pruefe lambda takes 1 arg; engine calls check(cmd, out, spiel) – fix sig
    text = text.replace('"pruefe": lambda cmd:', '"check": lambda cmd, out, p:')
    return text


# ── Read all source files ─────────────────────────────────────────────────────
print("Reading source files …")
game_text    = GAME.read_text()
kunst_text   = (CONTENT / "kunst_sektion.py").read_text()
raeume_16    = (CONTENT / "raeume_1_6.py").read_text()
raeume_712   = (CONTENT / "raeume_7_12.py").read_text()
raeume_neu_a = (CONTENT / "raeume_neu_a.py").read_text()
raeume_neu_b = normalize_neu_b((CONTENT / "raeume_neu_b.py").read_text())
print("  All files read OK")


# ── 1. Build replacement KUNST = {...} ────────────────────────────────────────
kunst_body = extract_dict_body(kunst_text, "KUNST_KOMPLETT = {")
new_kunst  = "KUNST = {" + kunst_body + "}"
print(f"  KUNST body: {len(kunst_body):,} chars")


# ── 2. Build combined RAEUME = {...} ──────────────────────────────────────────
body_16  = extract_dict_body(raeume_16,    "RAEUME_1_6 = {")
body_712 = extract_dict_body(raeume_712,   "RAEUME_7_12 = {")
body_na  = extract_dict_body(raeume_neu_a, "RAEUME_NEU_A = {")
body_nb  = extract_dict_body(raeume_neu_b, "RAEUME_NEU_B = {")

combined   = (body_16.rstrip('\n') + "\n"
              + body_712.rstrip('\n') + "\n"
              + body_na.rstrip('\n') + "\n"
              + body_nb.rstrip('\n') + "\n")
new_raeume = "RAEUME = {" + combined + "}"
print(f"  RAEUME body: {len(combined):,} chars")


# ── 3. Replace KUNST in game file ─────────────────────────────────────────────
ks, ke    = find_dict_bounds(game_text, "KUNST = {")
game_text = game_text[:ks] + new_kunst + game_text[ke:]
print("  KUNST replaced")


# ── 4. Replace RAEUME in game file ────────────────────────────────────────────
rs, re_   = find_dict_bounds(game_text, "RAEUME = {")
game_text = game_text[:rs] + new_raeume + game_text[re_:]
print("  RAEUME replaced")


# ── 5. Insert GESAMT_QUESTS after RAEUME ──────────────────────────────────────
rs2, re2  = find_dict_bounds(game_text, "RAEUME = {")
gesamt_line = "\nGESAMT_QUESTS = sum(len(r.get('quests', [])) for r in RAEUME.values())\n"
game_text = game_text[:re2] + gesamt_line + game_text[re2:]
print("  GESAMT_QUESTS inserted")


# ── 6. Update win condition ────────────────────────────────────────────────────
game_text = game_text.replace(
    'if len(spiel.scrolls) >= 30:',
    'if len(spiel.scrolls) >= GESAMT_QUESTS:'
)

# ── 7. Update scroll-count display (inventar + status) ───────────────────────
game_text = game_text.replace(
    '{len(spiel.scrolls)}/30',
    '{len(spiel.scrolls)}/{GESAMT_QUESTS}'
)

# ── 8. Update win-screen messages that hard-code "30 Schriftrollen" ───────────
game_text = game_text.replace(
    'Du hast alle 30 Schriftrollen gesammelt!',
    'Du hast alle {GESAMT_QUESTS} Schriftrollen gesammelt!'
)

print("  Win condition + UI counts updated")


# ── 9. Update welt_aufbauen – add new room directories ───────────────────────
old_dirs = (
    '    for raum_id in ("dorf", "wald", "see", "markt",\n'
    '                    "bibliothek", "labor", "festung",\n'
    '                    "bergpass", "hafen", "turm", "drachenfestung"):'
)
new_dirs = (
    '    for raum_id in ("dorf", "wald", "see", "markt",\n'
    '                    "bibliothek", "labor", "festung",\n'
    '                    "bergpass", "hafen", "turm", "drachenfestung",\n'
    '                    "bibliothekskeller", "schmiede", "sternwarte",\n'
    '                    "akademie", "taverne", "magierschule", "palast", "garten"):'
)
if old_dirs in game_text:
    game_text = game_text.replace(old_dirs, new_dirs)
    print("  welt_aufbauen directories updated")
else:
    print("  WARNING: directory list not found in welt_aufbauen – skipping")


# ── 10. Add new room data files inside welt_aufbauen ─────────────────────────
#
# We insert the new schreibe() calls right after the last existing one
# (the drachenbann.sh block, identified by its unique "SIEG FUER BINARIA" line).

new_files_block = (
    '    schreibe(basis / "schmiede" / "lagerliste.txt",\n'
    '        "Vorraete in der Schmiede:\\n"\n'
    '        "- Eisen x 50\\n"\n'
    '        "- Kohle x 30\\n"\n'
    '        "- Kupfer x 20\\n"\n'
    '    )\n'
    '    schreibe(basis / "sternwarte" / "sternenkarte.txt",\n'
    '        "=== Systembeobachtung ===\\n"\n'
    '        "uname, df, free, du, date, cal\\n"\n'
    '    )\n'
    '    schreibe(basis / "akademie" / "variablen.txt",\n'
    '        "Wichtige Umgebungsvariablen:\\n"\n'
    '        "$HOME - Home-Verzeichnis\\n"\n'
    '        "$USER - Benutzername\\n"\n'
    '        "$PATH - Suchpfad\\n"\n'
    '        "$SHELL - Shell-Pfad\\n"\n'
    '    )\n'
    '    schreibe(basis / "taverne" / "trickliste.txt",\n'
    '        "Shell-Tricks:\\n"\n'
    '        "Strg+C - Abbrechen\\n"\n'
    '        "Strg+L - Leeren\\n"\n'
    '        "Strg+A - Zeilenanfang\\n"\n'
    '        "Tab - Autovervollstaendigung\\n"\n'
    '        "Pfeil-Oben - Vorheriger Befehl\\n"\n'
    '    )\n'
    '    schreibe(basis / "magierschule" / "zauber_vorlage.sh",\n'
    '        "#!/bin/bash\\n"\n'
    "        \"NAME='Mia'\\n\"\n"
    '        "echo Hallo $NAME\\n"\n'
    '        "for i in 1 2 3; do echo $i; done\\n"\n'
    '    )\n'
    '    schreibe(basis / "palast" / "benutzerhandbuch.txt",\n'
    '        "Benutzerverwaltung:\\n"\n'
    '        "whoami - Aktueller Benutzer\\n"\n'
    '        "id - User-ID und Gruppen\\n"\n'
    '        "sudo BEFEHL - Als Root ausfuehren\\n"\n'
    '        "useradd NAME - Neuen Benutzer (root)\\n"\n'
    '    )\n'
    '    schreibe(basis / "bibliothekskeller" / "namen.txt",\n'
    '        "Anna\\nBernd\\nClara\\nAnna\\n"\n'
    '        "Dieter\\nBernd\\nEva\\nAnna\\n"\n'
    '    )\n'
    '    schreibe(basis / "bibliothekskeller" / "daten.csv",\n'
    '        "Anna,25,Berlin\\n"\n'
    '        "Bernd,30,Hamburg\\n"\n'
    '        "Clara,28,Berlin\\n"\n'
    '        "Dieter,35,Muenchen\\n"\n'
    '    )\n'
    '    schreibe(basis / "garten" / "gartenbuch.txt",\n'
    '        "Erweiterte Dateioperationen:\\n"\n'
    '        "ln -s = Symlink\\n"\n'
    '        "find -type f = nur Dateien\\n"\n'
    '        "find -size +1k = nach Groesse\\n"\n'
    '        "du -sh = Ordnergroesse\\n"\n'
    '    )\n'
)

MARKER = 'SIEG FUER BINARIA'
if MARKER in game_text:
    pos = game_text.index(MARKER)
    # Scan forward to find the closing paren of this schreibe() call
    close = game_text.index('\n    )\n', pos)
    insert_at = close + len('\n    )\n')
    game_text = game_text[:insert_at] + new_files_block + game_text[insert_at:]
    print("  New room data files added to welt_aufbauen")
else:
    print("  WARNING: SIEG FUER BINARIA not found – new room files not inserted")


# ── 11. Write the combined game file ──────────────────────────────────────────
GAME.write_text(game_text)
print(f"\nBuild complete: {GAME}  ({len(game_text):,} chars)")
