# Sektion: Neue Raeume B (magierschule/palast/bibliothekskeller/garten)
RAEUME_NEU_B = {
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
                "aufgabe": "Setze Variable: NAME='Linux'",
                "pruefe": lambda cmd: (
                    "=" in cmd
                    and bool(cmd.split())
                    and cmd.split()[0] not in [
                        "cd", "ls", "cat", "echo", "grep", "find",
                        "chmod", "cp", "mv", "rm", "mkdir", "touch", "pwd",
                    ]
                ),
                "belohnung": "📜 Schriftrolle der Beschwörung",
                "lerninhalt": "Variablen in Bash: NAME='Wert'. Kein Leerzeichen um =! Zugriff mit $NAME.",
            },
            {
                "id": "echo_var_mag",
                "aufgabe": "Nutze Variable: echo $NAME",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "echo"
                    and "$" in cmd
                ),
                "belohnung": "📜 Schriftrolle des Rufens",
                "lerninhalt": (
                    "In doppelten Anführungszeichen werden Variablen expandiert. "
                    "In einfachen nicht!"
                ),
            },
            {
                "id": "forloop_mag",
                "aufgabe": "Erstelle Schleife: for i in 1 2 3; do echo $i; done",
                "pruefe": lambda cmd: (
                    "for" in cmd
                    and "do" in cmd
                    and "done" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Wiederholung",
                "lerninhalt": (
                    "for i in LISTE; do BEFEHL; done. "
                    "Auch: for f in *.txt; do cat $f; done"
                ),
            },
            {
                "id": "if_mag",
                "aufgabe": "Schreibe Bedingung: if [ -f zauber.sh ]; then echo 'Vorhanden'; fi",
                "pruefe": lambda cmd: (
                    "if" in cmd
                    and "fi" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Entscheidung",
                "lerninhalt": (
                    "if [ BEDINGUNG ]; then...; fi. "
                    "-f=Datei, -d=Ordner. [ ] braucht Leerzeichen!"
                ),
            },
            {
                "id": "test_mag",
                "aufgabe": "Teste Datei: test -f zauber.sh && echo 'Ja'",
                "pruefe": lambda cmd: (
                    "&&" in cmd
                    and ("test" in cmd or "[" in cmd)
                ),
                "belohnung": "📜 Schriftrolle des Tests",
                "lerninhalt": (
                    "test -f = Datei vorhanden? "
                    "&& = nur wenn Erfolg. || = nur wenn Fehler."
                ),
            },
            {
                "id": "script_mag",
                "aufgabe": "Schreibe Skript: echo -e '#!/bin/bash\\necho Hallo' > mein.sh",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "echo"
                    and ".sh" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Schöpfung",
                "lerninhalt": (
                    "#!/bin/bash muss erste Zeile sein (Shebang). "
                    "echo -e erlaubt \\n als Zeilenumbruch."
                ),
            },
            {
                "id": "exec_mag",
                "aufgabe": "Fuehre Skript aus: chmod +x mein.sh && ./mein.sh",
                "pruefe": lambda cmd: (
                    "chmod" in cmd
                    and "+x" in cmd
                ),
                "belohnung": "📜 Schriftrolle des Lebens",
                "lerninhalt": (
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
                "aufgabe": "Wer regiert? whoami",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "whoami"
                ),
                "belohnung": "📜 Schriftrolle der Herrschaft",
                "lerninhalt": (
                    "whoami zeigt aktuellen Benutzernamen. "
                    "In Skripten: pruefen ob man root ist."
                ),
            },
            {
                "id": "id_pal",
                "aufgabe": "Zeige alle IDs: id",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "id"
                ),
                "belohnung": "📜 Schriftrolle der Identitaet",
                "lerninhalt": (
                    "id zeigt uid=N(name) gid=N(name) groups=... "
                    "Unverzichtbar fuer Berechtigungsprobleme."
                ),
            },
            {
                "id": "groups_pal",
                "aufgabe": "Zeige Gruppen: groups",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "groups"
                ),
                "belohnung": "📜 Schriftrolle der Zungen",
                "lerninhalt": (
                    "groups zeigt Mitgliedschaften. "
                    "sudo-Gruppe = Admin. docker-Gruppe = Docker nutzen."
                ),
            },
            {
                "id": "passwd_pal",
                "aufgabe": "Zeige Benutzer: cat /etc/passwd | head -5",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "cat"
                    and "passwd" in cmd
                ),
                "belohnung": "📜 Schriftrolle des Volkes",
                "lerninhalt": (
                    "/etc/passwd: name:x:uid:gid:info:home:shell. "
                    "Passwort-Hashes in /etc/shadow."
                ),
            },
            {
                "id": "group_pal",
                "aufgabe": "Zeige Gruppen-Datei: cat /etc/group | head -10",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "cat"
                    and "group" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Gemeinden",
                "lerninhalt": (
                    "/etc/group: gruppenname:x:gid:mitglieder. "
                    "sudo-Gruppe = Administrator."
                ),
            },
            {
                "id": "sudol_pal",
                "aufgabe": "Pruefe sudo-Rechte: sudo -l",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "sudo"
                    and len(cmd.split()) >= 2
                ),
                "belohnung": "📜 Schriftrolle der Macht",
                "lerninhalt": (
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
                "aufgabe": "Sortiere Namen: sort namen.txt",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "sort"
                    and len(cmd.split()) >= 2
                ),
                "belohnung": "📜 Schriftrolle der Ordnung",
                "lerninhalt": (
                    "sort sortiert alphabetisch. "
                    "-r=umgekehrt, -n=numerisch, -k 2=nach Spalte 2."
                ),
            },
            {
                "id": "uniq_kell",
                "aufgabe": "Entferne Duplikate: sort namen.txt | uniq",
                "pruefe": lambda cmd: "uniq" in cmd,
                "belohnung": "📜 Schriftrolle der Einzigartigkeit",
                "lerninhalt": (
                    "uniq entfernt BENACHBARTE Duplikate. "
                    "Immer: sort | uniq. uniq -c zaehlt Vorkommnisse."
                ),
            },
            {
                "id": "cut_kell",
                "aufgabe": "Schneide Spalte: cut -d',' -f1 daten.csv",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "cut"
                    and "-d" in cmd
                ),
                "belohnung": "📜 Schriftrolle des Schnitts",
                "lerninhalt": (
                    "cut -d',' -f1 = Trennzeichen Komma, Feld 1. "
                    "Perfekt fuer CSV-Dateien."
                ),
            },
            {
                "id": "awk_kell",
                "aufgabe": "Drucke Spalte: awk '{print $1}' namen.txt",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "awk"
                ),
                "belohnung": "📜 Schriftrolle der Felder",
                "lerninhalt": (
                    "awk verarbeitet strukturierten Text. "
                    "$1=Feld1, $NF=letztes Feld. Sehr maechtig!"
                ),
            },
            {
                "id": "sed_kell",
                "aufgabe": "Ersetze Text: sed 's/Anna/Mia/g' namen.txt",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "sed"
                ),
                "belohnung": "📜 Schriftrolle des Wandels",
                "lerninhalt": (
                    "sed 's/SUCHE/ERSATZ/g' ersetzt alle Vorkommen. "
                    "sed -i fuer direkte Dateibearbeitung."
                ),
            },
            {
                "id": "tr_kell",
                "aufgabe": "Grossbuchstaben: cat namen.txt | tr 'a-z' 'A-Z'",
                "pruefe": lambda cmd: (
                    "tr" in cmd
                    and ("a-z" in cmd or "A-Z" in cmd)
                ),
                "belohnung": "📜 Schriftrolle der Verwandlung",
                "lerninhalt": (
                    "tr = translate characters. "
                    "tr -d loescht Zeichen. tr -s quetscht Wiederholungen."
                ),
            },
            {
                "id": "pipeline_kell",
                "aufgabe": (
                    "Meister-Pipeline: "
                    "cat daten.csv | cut -d',' -f1 | sort | uniq -c | sort -rn"
                ),
                "pruefe": lambda cmd: (
                    "|" in cmd
                    and len([c for c in cmd.split("|") if c.strip()]) >= 3
                ),
                "belohnung": "📜 Schriftrolle der Meisterschaft",
                "lerninhalt": (
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
                "aufgabe": "Erstelle Symlink: ln -s preisliste.txt preis_link.txt",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "ln"
                    and "-s" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Verbindung",
                "lerninhalt": (
                    "ln -s = symbolischer Link (Verknuepfung). "
                    "Aenderungen wirken auf beide!"
                ),
            },
            {
                "id": "lsla_gar",
                "aufgabe": "Sieh den Symlink: ls -la",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "ls"
                    and "-la" in cmd
                ),
                "belohnung": "📜 Schriftrolle des Zeigers",
                "lerninhalt": (
                    "ls -la zeigt Symlinks mit -> Ziel. "
                    "l am Anfang der Rechte = Link."
                ),
            },
            {
                "id": "findtype_gar",
                "aufgabe": "Finde Dateien: find . -type f",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "find"
                    and "-type" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Dateien",
                "lerninhalt": (
                    "find -type f = nur Dateien, "
                    "-type d = nur Ordner, -type l = nur Links."
                ),
            },
            {
                "id": "findsize_gar",
                "aufgabe": "Finde grosse Dateien: find . -size +1k",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "find"
                    and "-size" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Masse",
                "lerninhalt": (
                    "find -size +1k = groesser als 1 Kilobyte. "
                    "+1M = groesser 1MB. c=Bytes, k=KB, M=MB."
                ),
            },
            {
                "id": "findmtime_gar",
                "aufgabe": "Finde neue Dateien: find . -mtime -1",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "find"
                    and "-mtime" in cmd
                ),
                "belohnung": "📜 Schriftrolle der Neuheit",
                "lerninhalt": (
                    "find -mtime -1 = letzten 24h geaendert. "
                    "-mtime +7 = aelter als 7 Tage."
                ),
            },
            {
                "id": "du_gar",
                "aufgabe": "Groesse anzeigen: du -sh .",
                "pruefe": lambda cmd: (
                    bool(cmd.split())
                    and cmd.split()[0] == "du"
                ),
                "belohnung": "📜 Schriftrolle der Totalgroesse",
                "lerninhalt": (
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
}
