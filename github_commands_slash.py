import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
token = "YOUR TOKEN"
bot = commands.Bot(command_prefix="!", intents=intents)

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
        interaction.followup.send("C'est parti !")


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


@bot.tree.command()
async def multiplication(interaction: discord.Interaction, a:int, b:int):
    await interaction.response.send_message(f"{a} x {b} = {a * b}")

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
