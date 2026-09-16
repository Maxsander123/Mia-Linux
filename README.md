# Mia lernt Linux!

Ein spielerisches, interaktives Linux-Terminal-Tutorial auf Deutsch – fuer alle, die
noch nie mit der Kommandozeile gearbeitet haben. Lerne echte Linux-Befehle in einer
Fantasywelt mit Quests, Raeumen und einem epischen Bosskampf gegen den boesen
Zauberer `rm -rf`.

## Eckdaten

- **20 Raeume** mit insgesamt **123 Quests** – ca. **3 Stunden Spielzeit**
- **Split-Screen**: Links das virtuelle Dateisystem, rechts der Terminal-Verlauf
- **Echte Befehle**: Du tippst echte Linux-Befehle – nichts ist simuliert
- **Sicher**: Alle Uebungen laufen in `~/linux_uebungen` – nichts am System kann kaputtgehen
- **Bosskampf**: Am Ende wartet die Drachenfestung

## Starten

```bash
python3 mia_lernt_linux.py
```

## Optionen

```bash
python3 mia_lernt_linux.py --spickzettel    # Alle Befehle auf einen Blick
python3 mia_lernt_linux.py --konzept        # Spielkonzept und Story anzeigen
python3 mia_lernt_linux.py --neustart       # Spielstand zuruecksetzen und neu beginnen
```

## Voraussetzungen

- Linux oder macOS
- Python 3.10+
- Ein Terminal-Fenster (mind. 80 Zeichen breit empfohlen)

## Die 20 Raeume

| # | Raum | Thema | Befehle (Auswahl) | Quests |
|---|------|-------|-------------------|--------|
| 1 | Dorfplatz | Einstieg & Orientierung | `ls`, `pwd`, `ls -la`, `ls -lh`, `--help` | 6 |
| 2 | Mystischer Wald | Navigation & erste Schritte | `mkdir`, `touch`, `rm`, `ls -R` | 5 |
| 3 | Dunkle Hoehle | Dateien lesen & bearbeiten | `cat`, `echo >>`, `wc -l`, `rmdir` | 6 |
| 4 | Stiller See | Textausgabe & Dateien | `echo >`, `head`, `wc -w`, `cat` | 6 |
| 5 | Marktplatz | Dateiverwaltung | `cp`, `mv`, `rm`, `find -name` | 6 |
| 6 | Bibliothek des Wissens | Suchen & Filtern | `grep`, `find`, Pipes (`\|`) | 3 |
| 7 | Geheimes Labor | Berechtigungen | `chmod`, `ls -l`, `whoami`, `id`, `stat` | 7 |
| 8 | Festung der Waechter | Prozesse | `ps`, `ps aux`, `jobs`, `kill`, `top`, `uptime` | 7 |
| 9 | Bergpass der Haendler | Paketverwaltung | `apt`, `apt-cache`, `dpkg`, `which` | 7 |
| 10 | Hafen der Verbindungen | Netzwerk | `ping`, `wget`, `curl`, `hostname`, `ss`, `nslookup` | 7 |
| 11 | Turm der Schreibkunst | Texteditor & Shell | `nano`, `chmod +x`, `uname`, `history` | 7 |
| 12 | Drachenfestung | Bosskampf | Alles zusammen, `grep`, `chmod`, Skript-Ausfuehrung | 5 |
| 13 | Schmiede der Archive | Archive & Komprimierung | `tar`, `gzip`, `gunzip`, `zip` | 6 |
| 14 | Sternwarte des Systems | Systeminfo | `uname -a`, `df -h`, `free -h`, `du`, `date`, `cal` | 7 |
| 15 | Akademie der Variablen | Umgebungsvariablen | `echo $HOME`, `export`, `env`, `printenv` | 6 |
| 16 | Taverne der Tricks | Shell-Tricks | `history`, `alias`, `type`, `which`, `echo $?`, `tee` | 6 |
| 17 | Magierschule der Skripte | Bash-Skripting | Variablen, Schleifen, `if`-Bedingungen, Skripte | 7 |
| 18 | Palast der Benutzer | Benutzer & Rechte | `whoami`, `id`, `groups`, `/etc/passwd`, `sudo -l` | 6 |
| 19 | Keller der Textzauberer | Textverarbeitung | `sort`, `uniq`, `cut`, `awk`, `sed`, `tr` | 7 |
| 20 | Garten der Verknuepfungen | Links & Suche | `ln -s`, `find -type`, `find -size`, `du -sh` | 6 |

## Alle gelehrten Befehle

### Navigation & Dateisystem
`pwd`, `ls`, `ls -la`, `ls -lh`, `ls -lt`, `ls -R`, `cd`, `mkdir`, `rmdir`

### Dateien erstellen & lesen
`touch`, `cat`, `echo`, `head`, `tail`, `wc`

### Dateiverwaltung
`cp`, `mv`, `rm`, `find`

### Suchen & Filtern
`grep`, `find`, `sort`, `uniq`, `cut`, `awk`, `sed`, `tr`

### Berechtigungen
`chmod`, `ls -l`, `stat`, `whoami`, `id`, `groups`

### Prozesse
`ps`, `ps aux`, `jobs`, `kill`, `top`, `uptime`, `sleep`

### Paketverwaltung
`apt`, `apt-cache show`, `apt list`, `dpkg -l`, `which`

### Netzwerk
`ping`, `wget`, `curl`, `hostname`, `ss`, `nslookup`

### Texteditor
`nano`

### Umgebungsvariablen & Shell
`echo $HOME`, `echo $USER`, `echo $PATH`, `export`, `env`, `printenv`, `history`, `alias`, `type`, `echo $?`, `tee`

### Bash-Skripting
Variablen, `for`-Schleifen, `if`/`test`, Shebang (`#!/bin/bash`), Skript ausfuehren

### Archive & Komprimierung
`tar -czvf`, `tar -tzvf`, `tar -xzvf`, `gzip`, `gunzip`, `zip`

### Systeminfo
`uname -a`, `df -h`, `free -h`, `du -sh`, `date`, `cal`, `uptime`

### Verknuepfungen
`ln -s`, `find -type f`, `find -size`, `find -mtime`

### Benutzer & Rechte
`whoami`, `id`, `groups`, `/etc/passwd`, `/etc/group`, `sudo -l`

## Build-System

Das Spiel kann auch modular gebaut werden. Die Sektionsdateien liegen unter `content/`,
das Build-Skript kombiniert sie:

```bash
python3 build_game.py
```

## Spielprinzip

1. Du startest im **Dorfplatz** des Koenigreichs Binaria.
2. Jeder Raum hat mehrere **Quests** mit Lernzielen.
3. Tippe den gezeigten Linux-Befehl – das Spiel prueft ihn direkt in deiner Shell.
4. Korrekte Befehle bringen dir **magische Schriftrollen**.
5. Mit allen Schriftrollen kannst du den Bosskampf in der **Drachenfestung** gewinnen.
6. Du kannst Raeume in beliebiger Reihenfolge erkunden – nutze `gehe <raum>` um zu reisen.

## In-Game-Befehle

| Befehl | Funktion |
|--------|----------|
| `hilfe` | Zeigt alle Spielbefehle an |
| `karte` | Zeigt die Weltkarte mit Raeumen |
| `gehe <raum>` | Reise in einen anderen Raum |
| `status` | Zeigt Fortschritt und gesammelte Schriftrollen |
| `spickzettel` | Alle bisher erlernten Befehle |
| `beenden` | Spiel beenden (Fortschritt wird gespeichert) |
