# Sektion: Raeume 1-6 (dorf/wald/hoehle/see/markt/bibliothek) mit allen Quests
RAEUME_1_6 = {
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
}
