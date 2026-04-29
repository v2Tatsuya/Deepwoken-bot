# 🖥️ Detaillierte Setup Anleitung für Windows

## Schritt 1: Python installieren

1. Gehe zu https://www.python.org/downloads/
2. Download "Python 3.11" (oder neuer)
3. **WICHTIG**: Bei Installation → "Add Python to PATH" ankreuzen!
4. "Install Now" klicken
5. Warte bis fertig

### Prüfe Installation:
Öffne Command Prompt (Win + R → `cmd` → Enter):
```bash
python --version
```
Sollte anzeigen: `Python 3.11.x` oder höher

## Schritt 2: Bot-Ordner vorbereiten

```bash
# Erstelle Ordner
mkdir C:\Users\dein_name\Desktop\deepwoken-bot
cd C:\Users\dein_name\Desktop\deepwoken-bot
```

## Schritt 3: Virtual Environment

```bash
# Erstelle venv
python -m venv venv

# Aktiviere venv (Windows)
venv\Scripts\activate
```

Erwartete Ausgabe:
```
(venv) C:\Users\dein_name\Desktop\deepwoken-bot>
```

## Schritt 4: Dependencies

```bash
# Installiere alle benötigten Pakete
pip install -r requirements.txt
```

## Schritt 5: Discord Bot Token

1. Gehe zu https://discord.com/developers/applications
2. Melde dich an (oder erstelle Account wenn nötig)
3. Klick oben rechts "New Application"
4. Gebe einen Namen ein: "Deepwoken Boss Bot"
5. Akzeptiere Terms
6. Klick auf "Bot" im linken Menu
7. Klick "Add Bot"
8. Unter "TOKEN" klick "Copy"
9. Speichere den Token sicher (Passwort Manager o.ä.)

## Schritt 6: Bot Permissions

1. Im Developer Portal: "OAuth2" im linken Menu
2. Unter "SCOPES" wähle:
   - ☑️ bot
3. Unter "PERMISSIONS" wähle:
   - ☑️ Send Messages
   - ☑️ Embed Links
   - ☑️ Mention Everyone
   - ☑️ Read Message History
4. Kopiere die generierte URL
5. Öffne sie im Browser
6. Wähle deinen Server aus
7. Klick "Authorize"

## Schritt 7: .env Datei

1. Im Bot-Ordner eine neue Datei erstellen: `.env`
2. Bearbeite sie mit Editor (Rechtsklick → Edit)
3. Schreibe:

```
DISCORD_TOKEN=dein_token_hier_einfügen
NOTIFICATION_CHANNEL_ID=1234567890
NOTIFICATION_ROLE_ID=9876543210
```

**Channel ID bekommen:**
1. Discord Developer Mode aktivieren:
   - User Settings (Zahnrad unten links)
   - Advanced
   - "Developer Mode" ON
2. Rechtsklick auf Discord Channel → "Copy Channel ID"
3. In .env einfügen

**Role ID bekommen:**
1. Rechtsklick auf Role im Server → "Copy Role ID"
2. In .env einfügen (optional)

## Schritt 8: Bot starten

```bash
# Stelle sicher venv ist noch aktiviert
# (Sollte `(venv)` am Anfang der Zeile zeigen)

python bot.py
```

Erwartete Ausgabe:
```
🚀 Deepwoken Boss Detector startet...
✅ Bot eingeloggt als DeepwokenBossBot#1234
📊 Starte Pattern Tracking...
```

✅ Bot läuft jetzt!

## Schritt 9: Bot testen

Im Discord Channel schreibe:
```
!boss_status
```

Bot sollte antworten mit Status!

## 🎯 Bei Problemen

**Error: "Discord token invalid"**
- ✅ Token in .env ist falsch → Regenerate im Developer Portal
- ✅ .env Datei muss im gleichen Ordner wie bot.py sein

**Error: "Channel not found"**
- ✅ NOTIFICATION_CHANNEL_ID in .env falsch
- ✅ Bot hat keinen Zugriff auf den Channel
- ✅ Prüfe dass Developer Mode aktiviert ist

**Python nicht erkannt**
- ✅ Python neu installieren mit "Add to PATH" Option
- ✅ Command Prompt neustarten nach Python Installation

---

🎉 Geschafft! Bot sollte jetzt funktionieren!
