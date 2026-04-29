# 🔧 TROUBLESHOOTING - Fehler beheben

## ❌ Error: "TypeError: expected token to be a str, received NoneType"

**URSACHE:** `.env` Datei fehlt oder `DISCORD_TOKEN` ist leer

**LÖSUNG:**
1. Prüfe dass `.env` Datei im Bot-Ordner existiert
2. Kopiere `.env.example` → `.env`
3. Öffne `.env` mit Editor
4. Ersetze `dein_bot_token_hier` mit echtem Token:

```env
DISCORD_TOKEN=MTkyNDEyNzc3MDY2OTU1Nzc2OA.CgdH6Q.XXXXX
NOTIFICATION_CHANNEL_ID=1234567890
```

5. Speichern (Ctrl+S)
6. Bot neu starten

---

## ❌ Error: "No module named 'discord'"

**URSACHE:** dependencies nicht installiert

**LÖSUNG:**
```bash
# Stelle sicher venv aktiv ist
venv\Scripts\activate

# Installiere dependencies
pip install -r requirements.txt
```

---

## ❌ Bot geht sofort offline

**Mögliche Ursachen:**
1. ✅ Token ungültig
2. ✅ Internet Problem
3. ✅ Python Version zu alt

**LÖSUNG:**
```bash
# Prüfe Python Version
python --version  # Muss 3.9+ sein

# Regeneriere Token im Developer Portal
# Settings → Bot → TOKEN → Regenerate
```

---

## ❌ Buttons erscheinen nicht im Discord

**URSACHE:** Slash Commands nicht synced

**LÖSUNG:**
1. Bot neu starten: `python bot_v2.py`
2. Warte 10 Sekunden
3. Im Discord: `/ask_event` eintippen
4. Sollte Buttons zeigen!

---

## ❌ "Channel not found" Error

**URSACHE:** Falsche Channel ID in `.env`

**LÖSUNG:**
1. Discord Developer Mode aktivieren:
   - Settings (⚙️ unten links)
   - Advanced
   - Developer Mode = ON
2. Rechtsklick auf Discord Channel
3. "Copy Channel ID" klicken
4. In `.env` einfügen
5. Bot neu starten

---

## ❌ Bot darf nicht schreiben

**URSACHE:** Bot hat keine Permissions

**LÖSUNG:**
1. Server → Channel
2. Rechtsklick auf Channel → Edit Channel
3. Permissions → Rolle des Bots
4. Stelle sicher aktiviert:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ View Channel

---

## ✅ Alles funktioniert!

Wenn alles lädt, sollte im Terminal stehen:
```
✅ Bot online als BotName#1234
✅ 4 Slash Commands synced
```

Im Discord dann `/ask_event` probieren!
