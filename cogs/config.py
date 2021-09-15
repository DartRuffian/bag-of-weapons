""" Allows server moderators to customize aspects of the bot """

# Discord Imports
import discord
from discord.ext import commands

# Other Imports
import json
import os

# Utils
from utils import Utils

class Config(commands.Cog, name="Configuration"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command (
        aliases=["c%","crit"]
    )
    async def crit_chance(self, ctx, percentage:int):
        os.chdir(f"{self.bot.BASE_DIR}/resources")
        with open("settings.json", "r") as f:
            settings = json.load(f)[str(ctx.guild.id)]


def setup(bot):
    bot.add_cog(Config(bot))