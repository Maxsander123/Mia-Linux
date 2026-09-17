# Mia lernt Linux!

Ein spielerisches, interaktives Linux-Terminal-Tutorial auf Deutsch – fuer alle, die
noch nie mit der Kommandozeile gearbeitet haben. Lerne echte Linux-Befehle in einer
Fantasywelt mit Quests, Raeumen und einem epischen Bosskampf gegen den boesen
Zauberer `rm -rf`.

## Eckdaten

- **25 Raeume** mit insgesamt **158 Quests** – ca. **5–6 Stunden Spielzeit**
- **Split-Screen**: Links das virtuelle Dateisystem, rechts der Terminal-Verlauf
- **Echte Befehle**: Du tippst echte Linux-Befehle – nichts ist simuliert
- **Echter VPS**: Die letzten 5 Raeume verbinden dich mit einem echten Linux-Server!
- **Sicher**: Lokale Uebungen laufen in `~/linux_uebungen` – nichts am System kann kaputtgehen

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
- `paramiko` fuer die VPS-Raeume: `pip3 install paramiko`

## VPS-Raeume einrichten (optional)

Die letzten 5 Raeume (Fernwelt-Portal, Schluesselschmiede, Zeituhr, Webwerkstatt,
Deploymeisterei) verbinden sich mit einem echten Linux-Server. Dazu braucht es eine
Konfigurationsdatei **ausserhalb** des Repos:

```bash
cat > ~/.mia_vps.ini << 'EOF'
[vps]
host     = DEINE_SERVER_IP
user     = DEIN_USER
password = DEIN_PASSWORT
port     = 22
EOF
```

Ohne diese Datei sind die VPS-Raeume gesperrt – alle anderen 20 Raeume funktionieren
ohne Konfiguration.

## Die 25 Raeume

### Lokale Raeume (kein Server noetig)

| # | Raum | Thema | Befehle (Auswahl) | Quests |
|---|------|-------|-------------------|--------|
| 1 | 🏠 Dorfplatz | Einstieg & Orientierung | `ls`, `pwd`, `ls -la`, `ls -lh`, `--help` | 6 |
| 2 | 🌲 Mystischer Wald | Navigation & erste Schritte | `mkdir`, `touch`, `rm`, `ls -R` | 5 |
| 3 | ⛏️ Dunkle Hoehle | Dateien lesen & bearbeiten | `cat`, `echo >>`, `wc -l`, `rmdir` | 6 |
| 4 | 🌊 Stiller See | Textausgabe & Dateien | `echo >`, `head`, `wc -w`, `cat` | 6 |
| 5 | 🏪 Marktplatz | Dateiverwaltung | `cp`, `mv`, `rm`, `find -name` | 6 |
| 6 | 📚 Bibliothek | Suchen & Filtern | `grep`, `find`, Pipes (`\|`) | 3 |
| 7 | ⚗️ Geheimes Labor | Berechtigungen | `chmod`, `ls -l`, `whoami`, `id`, `stat` | 7 |
| 8 | 🏰 Festung | Prozesse | `ps`, `jobs`, `kill`, `top`, `uptime` | 7 |
| 9 | ⛰️ Bergpass | Paketverwaltung | `apt`, `apt-cache`, `dpkg`, `which` | 7 |
| 10 | ⚓ Hafen | Netzwerk | `ping`, `wget`, `curl`, `hostname`, `ss` | 7 |
| 11 | 🗼 Turm | Texteditor & Shell | `nano`, `chmod +x`, `uname`, `history` | 7 |
| 12 | 🐉 Drachenfestung | Bosskampf | Alles zusammen | 5 |
| 13 | ⚒️ Schmiede | Archive & Komprimierung | `tar`, `gzip`, `gunzip`, `zip` | 6 |
| 14 | 🔭 Sternwarte | Systeminfo | `uname -a`, `df -h`, `free -h`, `du`, `date` | 7 |
| 15 | 🎓 Akademie | Umgebungsvariablen | `echo $HOME`, `export`, `env`, `printenv` | 6 |
| 16 | 🍺 Taverne | Shell-Tricks | `history`, `alias`, `type`, `tee`, `echo $?` | 6 |
| 17 | 🪄 Magierschule | Bash-Skripting | Variablen, Schleifen, `if`, Skripte | 7 |
| 18 | 🏛️ Palast | Benutzer & Rechte | `whoami`, `id`, `groups`, `/etc/passwd` | 6 |
| 19 | 📜 Buchkeller | Textverarbeitung | `sort`, `uniq`, `cut`, `awk`, `sed`, `tr` | 7 |
| 20 | 🌸 Garten | Links & Suche | `ln -s`, `find -type`, `find -size`, `du` | 6 |

### VPS-Raeume (echter Linux-Server, braucht `~/.mia_vps.ini`)

| # | Raum | Thema | Befehle (Auswahl) | Quests |
|---|------|-------|-------------------|--------|
| 21 | 🌐 Fernwelt-Portal | SSH & SCP | `ssh`, `scp`, `python3 -m http.server` | 7 |
| 22 | 🔑 Schluesselschmiede | SSH-Keys | `ssh-keygen`, `ssh-copy-id`, `cat ~/.ssh/id_ed25519.pub` | 5 |
| 23 | ⏰ Zeituhr | Crontab | `crontab -l`, `crontab -r`, Cron-Jobs anlegen | 5 |
| 24 | 💻 Webwerkstatt | HTML & CSS | `echo` HTML-Tags, `sed` CSS verknuepfen, `curl` | 10 |
| 25 | 🚀 Deploymeisterei | Deploy-Workflow | `nano`, `scp`, `sed -i`, Deploy-Skript | 8 |

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

### Netzwerk (lokal)
`ping`, `wget`, `curl`, `hostname`, `ss`, `nslookup`

### Texteditor
`nano`

### Umgebungsvariablen & Shell
`echo $HOME`, `echo $USER`, `echo $PATH`, `export`, `env`, `printenv`,
`history`, `alias`, `type`, `echo $?`, `tee`

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

### Remote-Server (VPS-Raeume)
`ssh user@host`, `scp datei user@host:~/pfad/`,
`ssh-keygen -t ed25519`, `ssh-copy-id user@host`,
`crontab -l`, `crontab -r`,
HTML mit `echo` und `>>` schreiben,
`sed -i` fuer Datei-Patches,
`python3 -m http.server PORT`,
Deploy-Skript mit `chmod +x` und `./deploy.sh`

## Build-System

Das Spiel kann modular gebaut werden. Die Sektionsdateien liegen unter `content/`,
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
6. Danach warten die VPS-Raeume mit echten Server-Abenteuern!

## In-Game-Befehle

| Befehl | Funktion |
|--------|----------|
| `hilfe` | Zeigt alle Spielbefehle an |
| `karte` | Zeigt die Weltkarte mit Raeumen |
| `gehe <raum>` | Reise in einen anderen Raum |
| `status` | Zeigt Fortschritt und gesammelte Schriftrollen |
| `spickzettel` | Alle bisher erlernten Befehle |
| `beenden` | Spiel beenden (Fortschritt wird gespeichert) |
