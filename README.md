# 🎪 Deepwoken Boss Pattern Detector Bot

Ein Discord Bot der automatisch Parasol Events im Deepwoken Roblox Game erkennt und prediziert!

## 📋 Features

- ✅ Automatische Erkennung von Boss Events (alle XX:00 und XX:30 Berlin Zeit)
- ✅ Pattern Lernen und Vorhersage für nächste Events
- ✅ Speichert Event Historie lokal (JSON)
- ✅ Discord Befehle zum Starten/Stoppen von Benachrichtigungen
- ✅ Automatische Ping-Benachrichtigungen bei erkanntem Parasol
- ✅ Web Dashboard Status (optional)

## 🚀 Schnellstart

### 1. Repository klonen
```bash
git clone https://github.com/v2Tatsuya/Deepwoken-bot.git
cd Deepwoken-bot
```

### 2. Python Setup
```bash
# Virtual Environment erstellen
python -m venv venv

# Aktivieren (Windows)
venv\Scripts\activate
# Oder (Mac/Linux)
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt
```

### 3. Discord Bot vorbereiten

**Bot auf Discord Developer Portal erstellen:**
1. Gehe zu https://discord.com/developers/applications
2. Klick "New Application"
3. Gebe einen Namen ein (z.B. "Deepwoken Boss Detector")
4. Gehe zum "Bot" Tab
5. Klick "Add Bot"
6. Unter "TOKEN" - klick "Copy" um deinen Bot Token zu kopieren
7. Unter "SCOPES" - wähle: `bot`
8. Unter "PERMISSIONS" - wähle:
   - Send Messages
   - Embed Links
   - Mention Everyone
   - Read Message History

**Bot zum Server einladen:**
- OAuth2 → URL Generator
- Scope: `bot`
- Permissions: Wie oben
- Kopiere die URL und öffne sie im Browser

### 4. .env Datei erstellen

```bash
# Kopiere die Beispiel-Datei
cp .env.example .env
```

Edite `.env` und füge ein:
```
DISCORD_TOKEN=dein_bot_token_hier
NOTIFICATION_CHANNEL_ID=deine_channel_id_hier
NOTIFICATION_ROLE_ID=deine_role_id_hier (optional)
```

**Wie bekomme ich IDs?**
- Discord Developer Mode aktivieren (User Settings → Advanced → Developer Mode)
- Rechtsklick auf Channel/Role → "ID kopieren"

### 5. Bot starten

```bash
python bot.py
```

Erwartete Ausgabe:
```
🚀 Deepwoken Boss Detector startet...
✅ Bot eingeloggt als YourBotName#1234
📊 Starte Pattern Tracking...
```

## 💬 Discord Befehle

### Admin Befehle (nur Bot Owner)

| Befehl | Beschreibung |
|--------|-------------|
| `!start_tracking` | Aktiviert Parasol Benachrichtigungen ✅ |
| `!stop_tracking` | Deaktiviert Parasol Benachrichtigungen ❌ |
| `!show_pattern` | Zeigt erkannte Pattern Statistiken 🔍 |
| `!boss_status` | Zeigt nächste Events und Wahrscheinlichkeiten ⏰ |

## 📊 Wie das Pattern Learning funktioniert

1. **Data Collection**: Bot speichert alle erkannten Boss Events mit Timestamp
2. **Pattern Analysis**: Analysiert die letzten 5-10 Events um Muster zu erkennen
3. **Prediction**: Nutzt Häufigkeitsanalyse um das nächste Event vorherzusagen
4. **Notification**: Sendet Discord Ping wenn Parasol vorhergesagt wird

## 📂 Dateien

- `bot.py` - Hauptdatei, Discord Bot Logic
- `event_tracker.py` - Pattern Recognition und Event Management
- `event_data.json` - Speichert alle Uh-Zeiten und Events (Auto-generiert)
- `.env` - Secrets (NICHT ins GitHub!)
- `requirements.txt` - Python Dependencies

## 🔧 Troubleshooting

### Bot goes offline
- ✅ Prüfe Discord Token in `.env`
- ✅ Prüfe Internet Connection
- ✅ Schau in Terminal nach Fehlern

### Keine Benachrichtigungen
- ✅ Prüfe `NOTIFICATION_CHANNEL_ID` in `.env`
- ✅ Stelle sicher dass Bot im Channel schreiben darf
- ✅ Nutze `!boss_status` um Status zu prüfen

### Bot findet Channel nicht
- ✅ Prüfe dass Channel ID korrekt ist (rechtsklick → ID kopieren)
- ✅ Stelle sicher Bot hat permission im Channel

## 🚀 Nächste Features

- [ ] Web Dashboard
- [ ] Machine Learning für bessere Predictions
- [ ] Statistiken und Histogramme
- [ ] Mobile App Integration
- [ ] Multiplayer Event Syncing

## 📝 License

MIT License - Frei zu verwenden und zu modifizieren

---

**Made with ❤️ for Deepwoken Players**
