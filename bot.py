import os
import discord
from discord.ext import commands
import openai

# Récupérer les clés via les variables d'environnement
openai.api_key = os.environ.get("OPENAI_API_KEY")

def obtenir_reponse(prompt: str) -> str:
    # Appel optimisé à l'API OpenAI pour obtenir une réponse rapide
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",         # Utilise GPT-3.5-turbo, qui est performant pour ce type de requête
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,                 # Limite le nombre de tokens pour obtenir une réponse concise
        temperature=0.3                # Température basse pour une réponse plus déterministe et rapide
    )
    return response.choices[0].message.content.strip()

# Configuration du bot Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Synchronisation des commandes slash avec Discord
    await bot.tree.sync()
    print(f"Connecté en tant que {bot.user}")

# Commande slash pour poser une question rapide
@bot.tree.command(name="ask", description="Pose une question rapide au bot alimenté par OpenAI")
async def ask(interaction: discord.Interaction, question: str):
    # Indique à Discord que la réponse est en cours pour éviter l'expiration
    await interaction.response.defer()
    # Utilise directement la question comme prompt
    reponse = obtenir_reponse(question)
    await interaction.followup.send(reponse)

# Lancer le bot en utilisant le token récupéré depuis les variables d'environnement
bot.run(os.environ.get("DISCORD_TOKEN"))
