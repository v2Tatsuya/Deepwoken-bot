#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Event Tracker - Verwaltet alle Boss Events und Pattern Recognition
Speichert die Zeiten von Parasol Events und versucht ein Muster zu erkennen
"""

from datetime import datetime, timedelta
import pytz
import json
import os

# Zeitzone Berlin
BERLIN_TZ = pytz.timezone('Europe/Berlin')

class EventTracker:
    """Klasse zum Tracken von Boss Events und Pattern Recognition"""
    
    def __init__(self):
        # Datenfile für persistente Speicherung
        self.data_file = "event_data.json"
        
        # Lade gespeicherte Events oder starte mit leer
        self.events = self._load_events()
        
        # Mögliche Boss Types (alle XX:00 und XX:30 Berlin Zeit)
        self.boss_types = ["Parasol", "Carnival of Heart", "Battle Royale"]
        
        # Pattern der erkannten Events (wird gefüllt durch Machine Learning)
        self.pattern = []
    
    def _load_events(self):
        """Lade alle gespeicherten Events aus JSON Datei"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_events(self):
        """Speichere alle Events in JSON Datei"""
        with open(self.data_file, 'w') as f:
            json.dump(self.events, f, indent=2, default=str)
        print(f"💾 {len(self.events)} Events gespeichert")
    
    def add_event(self, event_type, timestamp):
        """Füge ein erkanntes Event hinzu und speichere es"""
        event = {
            "type": event_type,
            "timestamp": timestamp.isoformat(),
            "time_str": timestamp.strftime("%d.%m.%Y %H:%M Berlin Zeit")
        }
        self.events.append(event)
        self.pattern.append(event_type)
        
        # Begrenze auf letzte 50 Events für Performance
        if len(self.events) > 50:
            self.events = self.events[-50:]
            self.pattern = self.pattern[-50:]
        
        self._save_events()
        print(f"✅ Event hinzugefügt: {event_type} um {timestamp}")
    
    def check_event_time(self, current_time):
        """Prüfe ob gerade ein Event sein sollte (XX:00 oder XX:30)"""
        minute = current_time.minute
        
        # Boss Events sind auf XX:00 oder XX:30 Uhr
        if minute == 0:
            return True, "Volle Stunde (XX:00)"
        elif minute == 30:
            return True, "Halbe Stunde (XX:30)"
        else:
            return False, None
    
    def predict_next_event(self):
        """Vorhersage welcher Boss als nächster kommt basierend auf Pattern"""
        if not self.pattern or len(self.pattern) < 3:
            # Zu wenig Daten - keine sichere Vorhersage möglich
            return "Unbekannt (Zu wenig Daten)"
        
        # Einfaches Pattern Matching: Schaue auf letzte 3 Events
        recent = self.pattern[-3:]
        
        # Zähle Häufigkeit der letzten Events
        from collections import Counter
        counter = Counter(recent)
        
        # Gib den häufigsten Boss zurück
        most_common = counter.most_common(1)[0][0]
        return most_common
    
    def get_pattern_info(self):
        """Gebe Info über erkanntes Pattern"""
        if not self.events:
            return "Noch keine Events aufgezeichnet"
        
        # Zeige letzte 10 Events
        recent_events = self.events[-10:]
        info = "**Letzte 10 Boss Events:**\n"
        
        for i, event in enumerate(recent_events, 1):
            info += f"{i}. {event['type']} - {event['time_str']}\n"
        
        info += f"\n**Nächste Vorhersage:** {self.predict_next_event()}"
        return info
    
    def get_next_parasol_time(self):
        """Berechne die nächste Parasol Event Zeit basierend auf Pattern"""
        now = datetime.now(BERLIN_TZ)
        
        # Nächste mögliche Event Zeit (XX:00 oder XX:30)
        if now.minute < 30:
            # Nächste Event: XX:30 diese Stunde
            next_time = now.replace(minute=30, second=0, microsecond=0)
        else:
            # Nächste Event: nächste volle Stunde (XX+1):00
            next_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        
        # Berechne Parasol Wahrscheinlichkeit basierend auf Pattern
        parasol_chance = self._calculate_parasol_chance()
        
        info = f"⏰ Nächste Event Zeit: `{next_time.strftime('%H:%M')} Berlin Zeit`\n"
        info += f"🎪 Parasol Wahrscheinlichkeit: `{parasol_chance}%`\n"
        info += f"📊 Tracked Events: `{len(self.events)}`"
        
        return info
    
    def _calculate_parasol_chance(self):
        """Berechne die Wahrscheinlichkeit dass nächstes Event Parasol ist"""
        if not self.pattern:
            return 33  # 3 mögliche Events = 33% Chance
        
        # Zähle wie oft Parasol in letzten 5 Events war
        recent_5 = self.pattern[-5:]
        parasol_count = recent_5.count("Parasol")
        
        # Wahrscheinlichkeit = (Vorkommen / 5) * 100
        chance = int((parasol_count / 5) * 100)
        return chance
    
    def record_parasol_spotted(self, timestamp=None):
        """Manuell ein Parasol Event eintragen (für Testing)"""
        if timestamp is None:
            timestamp = datetime.now(BERLIN_TZ)
        
        self.add_event("Parasol", timestamp)
