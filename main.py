# Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

# Keep Bot Online
from webserver import keep_alive

# Other imports
from pretty_help import PrettyHelp
from utils import Utils
import json
import os


# Define the bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot (
    command_prefix=Utils.get_server_prefix,
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
    # Get a discord.Member object of the bot's author
    bot.AUTHOR = bot.get_user(bot.AUTHOR)
 
# Load all cogs in the "cogs" subfolder
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# Load all user stats
Utils.refresh_stats(bot)
print(f"Loaded stats for {len(bot.member_stats.keys())} users")


keep_alive()
try:
    # When running locally
    with open("token.txt","r") as f:
        TOKEN = f.read()
except FileNotFoundError:
    # When running on server
    TOKEN = os.environ.get("DISCORD_BOT_SECRET") 

bot.run(TOKEN)