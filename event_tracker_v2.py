#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Event Tracker v2.0 - Enhanced mit besseren Predictions
Verwaltet alle Boss Events mit Pattern Recognition
"""

from datetime import datetime, timedelta
import pytz
import json
import os
from collections import Counter

# Zeitzone Berlin
BERLIN_TZ = pytz.timezone('Europe/Berlin')

class EventTracker:
    """Event Tracking & Pattern Learning Engine"""
    
    def __init__(self):
        # Speicherdatei
        self.data_file = "event_data.json"
        
        # Lade Events oder starte mit leer
        self.events = self._load_events()
        self.pattern = [e['type'] for e in self.events]  # Extrahiere nur Types
        
        # Mögliche Boss-Types
        self.boss_types = ["Parasol", "Carnival of Heart", "Battle Royale"]
    
    def _load_events(self):
        """Lade Events aus JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_events(self):
        """Speichere Events in JSON"""
        with open(self.data_file, 'w') as f:
            json.dump(self.events, f, indent=2, default=str)
        print(f"📼 {len(self.events)} Events gespeichert")
    
    def add_event(self, event_type, timestamp):
        """Füge ein Event hinzu und lerne Pattern"""
        event = {
            "type": event_type,
            "timestamp": timestamp.isoformat(),
            "time_str": timestamp.strftime("%d.%m.%Y %H:%M")
        }
        
        self.events.append(event)
        self.pattern.append(event_type)
        
        # Limitiere auf letzte 100 Events
        if len(self.events) > 100:
            self.events = self.events[-100:]
            self.pattern = self.pattern[-100:]
        
        self._save_events()
        print(f"✅ Event hinzugefügt: {event_type} um {timestamp.strftime('%H:%M')}")
    
    def check_event_time(self, current_time):
        """Prüfe ob gerade Event-Zeit ansteht (XX:00 oder XX:30)"""
        minute = current_time.minute
        
        if minute == 0:
            return True, "Volle Stunde (XX:00)"
        elif minute == 30:
            return True, "Halbe Stunde (XX:30)"
        else:
            return False, None
    
    def predict_next_event(self):
        """
        Vorhersage welcher Boss kommt
        Nutzt: Häufigkeitsanalyse der letzten 5 Events
        """
        if not self.pattern or len(self.pattern) < 3:
            return "Unbekannt"  # Zu wenig Daten
        
        # Nutze letzte 5 Events
        recent = self.pattern[-5:]
        
        # Zähle Häufigkeit
        counter = Counter(recent)
        
        # Gib häufigsten zurück
        most_common = counter.most_common(1)[0][0]
        return most_common
    
    def _calculate_parasol_chance(self):
        """Berechne Wahrscheinlichkeit dass nächstes Event Parasol ist"""
        if not self.pattern:
            return 33
        
        # Nutze letzte 5 Events
        recent = self.pattern[-5:]
        parasol_count = recent.count("Parasol")
        
        # Prozent berechnen
        chance = int((parasol_count / 5) * 100)
        return chance
    
    def get_pattern_info(self):
        """Gebe Muster-Info zurück"""
        if not self.events:
            return "❌ Noch keine Events aufgezeichnet"
        
        # Letzte 10 Events
        recent = self.events[-10:]
        info = "**Letzte 10 Events:**\n"
        
        for i, event in enumerate(recent, 1):
            info += f"{i}. **{event['type']}** - {event['time_str']}\n"
        
        # Häufigkeitsanalyse
        counter = Counter(self.pattern[-10:])
        info += "\n**Häufigkeit (letzte 10):**\n"
        for boss, count in counter.most_common():
            info += f"• {boss}: {count}x\n"
        
        info += f"\n🎯 **Vorhersage:** {self.predict_next_event()}"
        return info
    
    def get_next_parasol_time(self):
        """Berechne Zeitpunkt des nächsten Parasol"""
        now = datetime.now(BERLIN_TZ)
        
        # Nächste Event-Zeit
        if now.minute < 30:
            next_time = now.replace(minute=30, second=0, microsecond=0)
        else:
            next_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        
        parasol_chance = self._calculate_parasol_chance()
        
        info = f"⏰ **Nächste Event:** `{next_time.strftime('%H:%M')} Berlin Zeit`\n"
        info += f"🎪 **Parasol Chance:** `{parasol_chance}%`\n"
        info += f"📊 **Gelernte Events:** `{len(self.events)}`\n"
        info += f"📈 **Nächster Boss:** `{self.predict_next_event()}`"
        
        return info
