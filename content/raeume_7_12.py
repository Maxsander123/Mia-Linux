# Sektion: Raeume 7-12 (labor/festung/bergpass/hafen/turm/drachenfestung) mit allen Quests
RAEUME_7_12 = {
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
        "ausgaenge": {"bergpass": "Bergpass", "turm": "Turm", "akademie": "Akademie"},
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
}
