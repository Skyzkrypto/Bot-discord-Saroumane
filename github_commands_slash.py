# Imports

import discord
from discord.ext import commands
import asyncio
import json

# Bot settings

intents = discord.Intents.all()
token = "YOUR TOKEN"

bot = commands.Bot(command_prefix="!", intents=intents)

# Alive command

@bot.tree.command()
async def ping(interaction: discord.Interaction):

    await interaction.response.send_message("Pong !")

# Decompte command : create a countdown with the incoded value

@bot.tree.command()
async def decompte(interaction: discord.Interaction, a: int):
    
    if a > 10:
        await interaction.response.send_message(f"{a} est trop grand pour ce decompte")
        return
    
    await interaction.response.send_message(f"Départ dans :")
    
    while a > 0:
        await interaction.followup.send(a)
        a -= 1
        await asyncio.sleep(0.5)

    if a == 0:
        await interaction.followup.send("C'est parti !")

# Anonyme command : send a anonyme message in the channel

@bot.tree.command()
async def anonyme(interaction: discord.Interaction, *, message: str):

    safe_message = discord.utils.escape_mentions(message)

    if "@everyone" in safe_message or "@here" in safe_message:
        await interaction.response.send_message("Vous ne pouvez pas mentionner `@everyone` ou `@here`.")
        return

    if "<@&" in safe_message or "<@" in safe_message:
        await interaction.response.send_message("Vous ne pouvez pas mentionner des rôles ou utilisateurs.")
        return

    await interaction.response.send_message(f"Message anonyme : {safe_message}")

# Multiplication command : multiply two int value

@bot.tree.command()
async def multiplication(interaction: discord.Interaction, a:int, b:int):

    await interaction.response.send_message(f"{a} x {b} = {a * b}")

# Note command settings

def charger_notes():
    try:
        with open("github_notes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def sauvegarder_notes():
    with open("github_notes.json", "w") as f:
        json.dump(user_notes, f, indent=4)

user_notes = charger_notes()

# Ajouter_note command : add a note in memory so you don't have to remember it. Nobody except you can see the notes.

@bot.tree.command()
async def ajouter_note(interaction: discord.Interaction, note: str):

    user_id = str(interaction.user.id)
    if user_id not in user_notes:
        user_notes[user_id] = []

    user_notes[user_id].append(note)
    sauvegarder_notes()

    await interaction.response.send_message(f"Note ajoutée : {note}", ephemeral=True)

# Voir_note command : see the note that you already add by using the ajouter_note command

@bot.tree.command()
async def voir_notes(interaction: discord.Interaction):

    user_id = str(interaction.user.id)

    if user_id in user_notes and user_notes[user_id]:

        notes = "\n".join(user_notes[user_id])
        await interaction.response.send_message(f"Tes notes :\n{notes}", ephemeral=True)

    else:

        await interaction.response.send_message("Tu n'as pas encore ajouté de notes.", ephemeral=True)

# Effacer_notes command : erease all the notes that you have writed with the ajouter_note command

@bot.tree.command()
async def effacer_notes(interaction: discord.Interaction):

    user_id = str(interaction.user.id)

    if user_id in user_notes:

        user_notes[user_id] = []
        sauvegarder_notes()
        
    await interaction.response.send_message("Toutes tes notes ont été effacées.", ephemeral=True)

# Set the bot and catch errors

@bot.event
async def on_ready():
    try:
        print(f"Connecté en tant que {bot.user}")
        synced = await bot.tree.sync()
        print(f"{len(synced)} commande(s) synchronisée(s) : {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"Erreur lors de la synchronisation : {e}")

def main():
    bot.run(token=token)

if __name__ == "__main__":
    main()
