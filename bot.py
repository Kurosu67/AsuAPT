import discord
from discord.ext import commands
import openai

# === Configuration de l'API OpenAI ===
openai.api_key = "TA_CLE_API"  # Remplace par ta clé API OpenAI

def obtenir_reponse(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",  # Ou un autre modèle de ton choix (par exemple GPT-3.5-turbo si disponible)
        prompt=prompt,
        max_tokens=150,             # Ajuste selon tes besoins
        temperature=0.7             # Pour contrôler la créativité des réponses
    )
    return response.choices[0].text.strip()

# === Mémoire contextuelle : un dictionnaire pour stocker l'historique par channel ===
conversation_history = {}

# === Configuration du bot Discord ===
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Synchronisation des commandes slash auprès de Discord
    await bot.tree.sync()
    print(f"Connecté en tant que {bot.user}")

# --- Commande slash simple ---
@bot.tree.command(name="hello", description="Le bot te dit bonjour")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello !")

# --- Commande slash pour poser une question (sans mémoire contextuelle) ---
@bot.tree.command(name="ask", description="Pose une question au bot alimenté par OpenAI")
async def ask(interaction: discord.Interaction, question: str):
    prompt = f"User: {question}\nBot:"
    reponse = obtenir_reponse(prompt)
    await interaction.response.send_message(reponse)

# --- Commande slash pour discuter avec le bot en gardant le contexte ---
@bot.tree.command(name="chat", description="Discute avec le bot en gardant le contexte")
async def chat(interaction: discord.Interaction, message_input: str):
    channel_id = str(interaction.channel_id)
    
    # Initialiser l'historique pour le channel si nécessaire
    if channel_id not in conversation_history:
        conversation_history[channel_id] = []
    
    # Ajouter le message de l'utilisateur à l'historique
    conversation_history[channel_id].append(f"User: {message_input}")
    
    # Construire le prompt à partir de l'historique
    prompt = "\n".join(conversation_history[channel_id]) + "\nBot:"
    
    # Obtenir la réponse d'OpenAI
    reponse = obtenir_reponse(prompt)
    
    # Ajouter la réponse du bot à l'historique
    conversation_history[channel_id].append(f"Bot: {reponse}")
    
    # Optionnel : Limiter l'historique (ici, aux 10 derniers échanges)
    if len(conversation_history[channel_id]) > 10:
        conversation_history[channel_id] = conversation_history[channel_id][-10:]
    
    await interaction.response.send_message(reponse)

# === Démarrer le bot ===
bot.run("TON_TOKEN_DISCORD")  # Remplace par le token de ton bot Discord
