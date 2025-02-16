import os
import time
import discord
from discord.ext import commands
import openai

# Récupère la clé API OpenAI depuis les variables d'environnement
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Fonction asynchrone pour obtenir la réponse de l'API OpenAI
async def obtenir_reponse(prompt: str) -> str:
    start_time = time.time()
    # Utilise l'appel asynchrone de l'API ChatCompletion
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",         # Modèle rapide et performant
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,                 # Limite le nombre de tokens pour une réponse concise
        temperature=0.3                # Température basse pour des réponses plus déterministes
    )
    elapsed_time = time.time() - start_time
    print(f"OpenAI API call took {elapsed_time:.2f} seconds")
    return response.choices[0].message.content.strip()

# Configuration du bot Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Synchronise les commandes slash
    await bot.tree.sync()
    print(f"Connecté en tant que {bot.user}")

# Commande slash pour poser une question rapide
@bot.tree.command(name="ask", description="Pose une question rapide au bot alimenté par OpenAI")
async def ask(interaction: discord.Interaction, question: str):
    # Indique à Discord que la réponse va arriver
    await interaction.response.defer()
    # Appel asynchrone pour obtenir la réponse de l'API OpenAI
    reponse = await obtenir_reponse(question)
    # Envoie la réponse dans un followup pour terminer l'interaction
    await interaction.followup.send(reponse)

# Lancement du bot (le token Discord est récupéré via la variable d'environnement DISCORD_TOKEN)
bot.run(os.environ.get("DISCORD_TOKEN"))
