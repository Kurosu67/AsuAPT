import os
import discord
from discord.ext import commands
import openai

# Récupérer les clés via les variables d'environnement
openai.api_key = os.environ.get("OPENAI_API_KEY")

def obtenir_reponse(prompt: str) -> str:
    # Utilisation de l'API ChatCompletion avec la nouvelle interface
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # ou GPT-4 si tu y as accès
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Mémoire contextuelle : stocke l'historique des conversations par channel
conversation_history = {}

# Configuration du bot Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Synchronise les commandes slash
    await bot.tree.sync()
    print(f"Connecté en tant que {bot.user}")

# Commande slash simple
@bot.tree.command(name="hello", description="Le bot te dit bonjour")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello !")

# Commande slash pour poser une question (sans mémoire)
@bot.tree.command(name="ask", description="Pose une question au bot alimenté par OpenAI")
async def ask(interaction: discord.Interaction, question: str):
    # On peut utiliser defer pour indiquer à Discord qu'on travaille à la réponse
    await interaction.response.defer()
    prompt = f"User: {question}\nBot:"
    reponse = obtenir_reponse(prompt)
    await interaction.followup.send(reponse)

# Commande slash pour discuter avec mémoire contextuelle
@bot.tree.command(name="chat", description="Discute avec le bot en gardant le contexte")
async def chat(interaction: discord.Interaction, message_input: str):
    channel_id = str(interaction.channel_id)
    
    # Initialiser l'historique pour ce channel s'il n'existe pas
    if channel_id not in conversation_history:
        conversation_history[channel_id] = []
    
    # Ajouter le message de l'utilisateur à l'historique
    conversation_history[channel_id].append(f"User: {message_input}")
    
    # Construire le prompt à partir de l'historique
    prompt = "\n".join(conversation_history[channel_id]) + "\nBot:"
    
    # Obtenir la réponse via OpenAI
    reponse = obtenir_reponse(prompt)
    
    # Ajouter la réponse du bot à l'historique
    conversation_history[channel_id].append(f"Bot: {reponse}")
    
    # Limiter l'historique pour éviter de dépasser la limite de tokens (par exemple, 10 derniers échanges)
    if len(conversation_history[channel_id]) > 10:
        conversation_history[channel_id] = conversation_history[channel_id][-10:]
    
    await interaction.response.send_message(reponse)

# Lancement du bot (le token Discord est récupéré via la variable d'environnement DISCORD_TOKEN)
bot.run(os.environ.get("DISCORD_TOKEN"))
