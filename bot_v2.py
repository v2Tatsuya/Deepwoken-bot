#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deepwoken Boss Pattern Detector Bot - Version 2.0
Mit interaktiven Buttons für Event Selection + Auto-Pings!
"""

import os
import asyncio
import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Lade .env mit Secrets
load_dotenv()

# ====== TOKENS & IDS ======
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
NOTIFICATION_CHANNEL_ID = int(os.getenv("NOTIFICATION_CHANNEL_ID", 0))
NOTIFICATION_ROLE_ID = os.getenv("NOTIFICATION_ROLE_ID")
BERLIN_TZ = pytz.timezone('Europe/Berlin')

# ====== BOT SETUP ======
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ====== IMPORTS ======
from event_tracker import EventTracker
events = EventTracker()

# ====== GLOBAL STATES ======
tracking_active = False  # Soll Bot pingen?
pattern_learned = False   # Hat Bot Muster erkannt?
learning_phase = True     # Fragt Bot noch nach Events?
user_responses = {}       # Speichert User Event Inputs

# ====== BUTTON CLASS ====== 
class BossSelectionView(discord.ui.View):
    """
    Interactive Button View - User klickt welcher Boss kam!
    Speichert die Events für Pattern Learning
    """
    
    def __init__(self, user_id: int):
        super().__init__(timeout=300)  # 5 Minuten Timeout
        self.user_id = user_id
        self.selected = None
    
    @discord.ui.button(label="🎪 Parasol", style=discord.ButtonStyle.primary, custom_id="btn_parasol")
    async def parasol_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Button: Parasol Event"""
        await self._handle_selection(interaction, "Parasol")
    
    @discord.ui.button(label="🎠 Carnival of Heart", style=discord.ButtonStyle.blurple, custom_id="btn_carnival")
    async def carnival_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Button: Carnival of Heart Event"""
        await self._handle_selection(interaction, "Carnival of Heart")
    
    @discord.ui.button(label="⚔️ Battle Royale", style=discord.ButtonStyle.danger, custom_id="btn_battleroyal")
    async def battleroyal_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Button: Battle Royale Event"""
        await self._handle_selection(interaction, "Battle Royale")
    
    async def _handle_selection(self, interaction: discord.Interaction, boss_type: str):
        """Verarbeite Boss Selection - speichere und lerne Muster"""
        
        # Nur der Requester kann klicken
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Das ist nicht dein Event!", ephemeral=True)
            return
        
        # Timestamp jetzt
        now = datetime.now(BERLIN_TZ)
        
        # Speichere Event
        events.add_event(boss_type, now)
        self.selected = boss_type
        
        # Feedback
        embed = discord.Embed(
            title="✅ Event gespeichert!",
            description=f"**{boss_type}** um **{now.strftime('%H:%M')}**",
            color=discord.Color.green()
        )
        embed.add_field(name="📊 Events gelernt", value=f"{len(events.events)}/5", inline=False)
        embed.add_field(name="🎯 Ziel", value="Nach 5 Events startet Auto-Ping", inline=False)
        
        await interaction.response.edit_message(embed=embed, view=None)
        
        # Prüfe ob genug Events für Pattern
        global learning_phase, pattern_learned, tracking_active
        if len(events.events) >= 5 and learning_phase:
            pattern_learned = True
            learning_phase = False
            tracking_active = True
            
            # Starte Auto-Tracking
            embed_complete = discord.Embed(
                title="🎉 PATTERN ERKANNT!",
                description=f"Nach 5 Events: Bot hat Muster gelernt!\n"
                            f"**Nächstes Event:** {events.predict_next_event()}\n\n"
                            f"🤖 Bot startet jetzt AUTO-PINGS bei {events.predict_next_event()}!",
                color=discord.Color.gold()
            )
            
            # Sende Notification
            channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
            if channel:
                await channel.send(embed=embed_complete)

@bot.event
async def on_ready():
    """Bot ist online - starte Tracking Loop"""
    print(f"\n✅ Bot online als {bot.user}")
    print(f"🎪 Deepwoken Pattern Detector aktiv\n")
    
    # Synce Slash Commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} Slash Commands synced")
    except Exception as e:
        print(f"❌ Fehler beim Syncing: {e}")
    
    # Starte Auto-Ping Loop
    if not check_event_time.is_running():
        check_event_time.start()

# ====== SLASH COMMANDS ======

@bot.tree.command(name="ask_event", description="🎯 Welcher Boss war es? Klick einen Button")
@app_commands.checks.has_permissions(administrator=False)
async def ask_event(interaction: discord.Interaction):
    """
    Slash Command: /ask_event
    Fragt User welcher Boss gekommen ist
    """
    global learning_phase
    
    if not learning_phase:
        await interaction.response.send_message(
            "✅ Bot kennt das Muster schon! Auto-Pings sind AKTIV!",
            ephemeral=True
        )
        return
    
    # Erstelle Embed mit Buttons
    embed = discord.Embed(
        title="🎪 Welcher Boss war das?",
        description="Klick einen Button um das Event einzutragen!\n"
                    f"Events gelernt: **{len(events.events)}/5**",
        color=discord.Color.blue()
    )
    
    view = BossSelectionView(interaction.user.id)
    await interaction.response.send_message(embed=embed, view=view)
    print(f"[INTERACT] {interaction.user} gefragt: Welcher Boss?")

@bot.tree.command(name="show_pattern", description="📊 Zeige erkannte Muster")
async def show_pattern(interaction: discord.Interaction):
    """
    Slash Command: /show_pattern
    Zeige gelernte Events und Muster
    """
    pattern_info = events.get_pattern_info()
    
    embed = discord.Embed(
        title="🔍 Erkannte Boss Pattern",
        description=pattern_info if pattern_info else "❌ Noch kein Muster erkannt",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="📈 Status",
        value=f"Pattern gelernt: {'✅ JA' if pattern_learned else '❌ NEIN (braucht 5 Events)'}\n"
              f"Auto-Ping: {'✅ AUS' if tracking_active else '❌ AN'}",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="boss_status", description="⏰ Nächste Events & Vorhersagen")
async def boss_status(interaction: discord.Interaction):
    """
    Slash Command: /boss_status
    Zeige Status und nächste Events
    """
    status = events.get_next_parasol_time()
    
    embed = discord.Embed(
        title="⏰ Boss Event Status",
        description=status,
        color=discord.Color.green()
    )
    
    if pattern_learned:
        embed.add_field(
            name="🎯 Nächste Vorhersage",
            value=f"**{events.predict_next_event()}**",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="control_panel", description="⚙️ Starte/Stoppe Auto-Pings")
@app_commands.checks.has_permissions(administrator=True)
async def control_panel(interaction: discord.Interaction):
    """
    Slash Command: /control_panel (nur Admin)
    Kontrolliere Auto-Ping Status
    """
    global tracking_active
    
    class ControlView(discord.ui.View):
        @discord.ui.button(label="▶️ START", style=discord.ButtonStyle.success)
        async def start_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
            global tracking_active
            tracking_active = True
            await interaction.response.send_message("✅ Auto-Pings AKTIVIERT!", ephemeral=True)
        
        @discord.ui.button(label="⏹️ STOP", style=discord.ButtonStyle.danger)
        async def stop_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
            global tracking_active
            tracking_active = False
            await interaction.response.send_message("❌ Auto-Pings DEAKTIVIERT!", ephemeral=True)
    
    embed = discord.Embed(
        title="⚙️ Tracking Control Panel",
        description=f"Auto-Pings: {'✅ AKTIV' if tracking_active else '❌ INAKTIV'}\n"
                    f"Pattern gelernt: {'✅ JA' if pattern_learned else '❌ NEIN'}",
        color=discord.Color.orange()
    )
    
    await interaction.response.send_message(embed=embed, view=ControlView())

# ====== AUTO-PING LOOP ======

@tasks.loop(minutes=1)
async def check_event_time():
    """
    Background Task: Prüfe jede Minute ob Event-Zeit ansteht
    Wenn Pattern gelernt + Event ansteht + Parasol = PING!
    """
    global tracking_active, pattern_learned
    
    if not tracking_active or not pattern_learned:
        return
    
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if not channel:
        print("❌ Notification Channel nicht gefunden!")
        return
    
    # Aktuelle Berlin Zeit
    now = datetime.now(BERLIN_TZ)
    
    # Prüfe ob XX:00 oder XX:30
    is_event_time, event_type = events.check_event_time(now)
    
    if is_event_time:
        # Vorhersage: ist Parasol?
        prediction = events.predict_next_event()
        
        if prediction == "Parasol":
            # PING!!!
            mention = f"<@&{NOTIFICATION_ROLE_ID}>" if NOTIFICATION_ROLE_ID else "@everyone"
            
            embed = discord.Embed(
                title="🎪 PARASOL EVENT JETZT!",
                description=f"{mention}\n"
                            f"Zeit: `{now.strftime('%H:%M')} Berlin`\n"
                            f"Vorhersage Genauigkeit: `{events._calculate_parasol_chance()}%`",
                color=discord.Color.red()
            )
            embed.set_footer(text="Pattern Detector v2.0 - Auto-Ping")
            
            await channel.send(mention, embed=embed)
            print(f"[PING] 🎪 PARASOL DETECTED: {now}")

# ====== ERROR HANDLER ======

@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Error Handler für Slash Commands"""
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Du hast keine Berechtigung!", ephemeral=True)
    elif isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"⏱️ Warte {error.retry_after:.1f}s", ephemeral=True)
    else:
        print(f"❌ Command Error: {error}")

# ====== START BOT ======

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════╗
║ 🎪 DEEPWOKEN BOSS DETECTOR v2.0        ║
║ Mit Buttons & Auto-Pings!              ║
╚════════════════════════════════════════╝
    """)
    
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ FEHLER: {e}")
        print("Prüfe deine .env Datei!")
