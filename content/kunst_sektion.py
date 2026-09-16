# Inhalt: Komplette KUNST-Dict fuer alle 20 Raeume
# Diese Datei wird vom Build-System eingelesen

import os
import re

class F:
    PINK  = '\033[95m'; BLAU  = '\033[94m'; GRUEN = '\033[92m'
    GELB  = '\033[93m'; ROT   = '\033[91m'; CYAN  = '\033[96m'
    WEISS = '\033[97m'; GRAU  = '\033[90m'; BRAUN = '\033[33m'
    FETT  = '\033[1m';  RESET = '\033[0m'

def c(t, *fs): return ''.join(fs) + str(t) + F.RESET

KUNST_KOMPLETT = {
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
}
