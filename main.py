# Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

# Keep Bot Online
from webserver import keep_alive

# Other imports
from pretty_help import PrettyHelp
import os


# Define the bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot (
    command_prefix=".",
    intents=intents,
    case_insensitive=True,
    help_command=PrettyHelp(color=0x784513),
    activity=discord.Game("type .help")
)

# Other attributes
bot.AUTHOR = 400337254989430784
bot.EMBED_COLOR = 0x784513
bot.BASE_DIR = os.getcwd()


@bot.event 
async def on_ready():
    # Called when the bot connects to Discord
    print("Logged in")
    print(f"Username: {bot.user.name}")
    print(f"Userid  : {bot.user.id}")
    bot.AUTHOR = get(bot.get_all_members(), id=bot.AUTHOR)

# Load all cogs in the "cogs" subfolder
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


#keep_alive()
try:
    # When running locally
    with open("token.txt","r") as f:
        TOKEN = f.read()
except FileNotFoundError:
    # When running on server
    TOKEN = os.environ.get("DISCORD_BOT_SECRET") 

bot.run(TOKEN)