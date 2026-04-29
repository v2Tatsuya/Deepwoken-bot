#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deepwoken Boss Pattern Detector Bot
Hauptdatei - startet den Discord Bot und verwaltet alle Funktionen
"""

import os
import asyncio
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Lade .env Datei mit Secrets
load_dotenv()

# Discord Bot Setup
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
NOTIFICATION_CHANNEL_ID = int(os.getenv("NOTIFICATION_CHANNEL_ID", 0))
NOTIFICATION_ROLE_ID = os.getenv("NOTIFICATION_ROLE_ID")

# Zeitzone Berlin
BERLIN_TZ = pytz.timezone('Europe/Berlin')

# Bot Setup mit Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Globale Variablen für Pattern Tracking
from event_tracker import EventTracker
events = EventTracker()

# Flag um Bot zu stoppen/starten
notification_active = True

@bot.event
async def on_ready():
    """Wird aufgerufen wenn Bot online geht"""
    print(f"✅ Bot eingeloggt als {bot.user}")
    print(f"📊 Starte Pattern Tracking...")
    
    # Starte regelmäßiges Tracking
    check_boss_pattern.start()
    
@bot.command(name="start_tracking")
@commands.is_owner()  # Nur Bot Owner kann das
async def start_tracking(ctx):
    """Discord Befehl: !start_tracking - Aktiviert Benachrichtigungen"""
    global notification_active
    notification_active = True
    await ctx.send("✅ **Parasol Benachrichtigungen AKTIVIERT**")
    print("[TRACKING] Benachrichtigungen aktiviert")

@bot.command(name="stop_tracking")
@commands.is_owner()  # Nur Bot Owner kann das
async def stop_tracking(ctx):
    """Discord Befehl: !stop_tracking - Deaktiviert Benachrichtigungen"""
    global notification_active
    notification_active = False
    await ctx.send("❌ **Parasol Benachrichtigungen DEAKTIVIERT**")
    print("[TRACKING] Benachrichtigungen deaktiviert")

@bot.command(name="show_pattern")
async def show_pattern(ctx):
    """Discord Befehl: !show_pattern - Zeigt erkannte Muster an"""
    pattern_info = events.get_pattern_info()
    
    embed = discord.Embed(
        title="🔍 Erkannte Boss Pattern",
        description=pattern_info if pattern_info else "Noch kein Muster erkannt",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name="boss_status")
async def boss_status(ctx):
    """Discord Befehl: !boss_status - Zeigt aktuellen Status und nächste Events"""
    status = events.get_next_parasol_time()
    
    embed = discord.Embed(
        title="⏰ Nächste Boss Events",
        description=status,
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@tasks.loop(minutes=1)  # Prüfe jede Minute
async def check_boss_pattern():
    """Regelmäßig prüfen ob Parasol Event ansteht und Pattern erkannt wurde"""
    global notification_active
    
    if not notification_active:
        return
    
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if not channel:
        print("❌ Notification Channel nicht gefunden!")
        return
    
    # Hole aktuelle Zeit in Berlin
    now = datetime.now(BERLIN_TZ)
    
    # Prüfe ob Parasol Event ansteht (XX:00 oder XX:30)
    is_event_time, event_type = events.check_event_time(now)
    
    if is_event_time:
        # Prüfe ob Parasol erkannt wurde
        if events.predict_next_event() == "Parasol":
            # Benachrichtigung senden
            mention = f"<@&{NOTIFICATION_ROLE_ID}>" if NOTIFICATION_ROLE_ID else "@everyone"
            
            embed = discord.Embed(
                title="🎪 PARASOL EVENT ERKANNT!",
                description=f"Das nächste Event sollte **PARASOL** sein!\n"
                            f"Zeit: `{now.strftime('%H:%M')} Berlin Zeit`\n"
                            f"Type: {event_type}",
                color=discord.Color.red()
            )
            embed.set_footer(text="Pattern Detector v1.0")
            
            await channel.send(mention, embed=embed)
            print(f"[NOTIFICATION] Parasol erkannt: {now}")

# Error Handler
@bot.event
async def on_command_error(ctx, error):
    """Fehlerbehandlung für Commands"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Falsches Argument!")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("❌ Du hast keine Berechtigung für diesen Befehl!")
    else:
        print(f"Fehler: {error}")

# Bot starten
if __name__ == "__main__":
    print("🚀 Deepwoken Boss Detector startet...")
    bot.run(DISCORD_TOKEN)
