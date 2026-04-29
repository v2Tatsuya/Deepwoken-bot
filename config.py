#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Konfiguration - Zentrale Einstellungen für den Bot
Ändere hier die Grundeinstellungen
"""

import os
import pytz
from dotenv import load_dotenv

# Lade .env Datei
load_dotenv()

# ====== DISCORD EINSTELLUNGEN ======
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
NOTIFICATION_CHANNEL_ID = int(os.getenv("NOTIFICATION_CHANNEL_ID", 0))
NOTIFICATION_ROLE_ID = os.getenv("NOTIFICATION_ROLE_ID")
COMMAND_PREFIX = "!"  # Discord Befehl Präfix (!status, !start, etc)

# ====== ZEITZONE ======
BERLIN_TZ = pytz.timezone('Europe/Berlin')

# ====== EVENT EINSTELLUNGEN ======
# Wann sind Boss Events? (Berlin Zeit)
EVENT_INTERVALS = [0, 30]  # Jede Stunde XX:00 und XX:30
BOSS_TYPES = ["Parasol", "Carnival of Heart", "Battle Royale"]  # Mögliche Bosses

# ====== PATTERN LEARNING ======
MIN_EVENTS_FOR_PREDICTION = 3  # Min. 3 Events bevor Vorhersage möglich
PATTERN_HISTORY_LENGTH = 50  # Speichere letzte 50 Events
RECENT_PATTERN_LENGTH = 5  # Nutze letzte 5 Events für Analyse

# ====== CHECK INTERVAL ======
CHECK_INTERVAL_MINUTES = 1  # Prüfe alle X Minuten nach Events

# ====== DATA PERSISTANCE ======
DATA_FILE = "event_data.json"  # Speichern von Events lokal
LOG_FILE = "bot_activity.log"  # Bot Activity Log

print("✅ Konfiguration geladen")
