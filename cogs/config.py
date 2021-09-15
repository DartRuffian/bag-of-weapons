""" Allows server moderators to customize aspects of the bot """

# Discord Imports
import discord
from discord.ext import commands

# Other Imports
import json
import os

from discord.ext.commands.core import has_permissions

# Utils
from utils import Utils

class Config(commands.Cog, name="Configuration"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command (
        aliases=["c"]
    )
    #@has_permissions(manage_channels=True)
    async def config(self, ctx, *kwargs):
        os.chdir(f"{self.bot.BASE_DIR}/resources")
        with open("settings.json", "r") as f:
            settings = json.load(f)
        os.chdir(self.bot.BASE_DIR)

        default_settings = {
            "crit_chance": 6,
            "hit_chance": 80,
        }
        print(kwargs)
        if kwargs == ("reset",):
            settings[str(ctx.guild.id)] = default_settings
        else:
            for argument in kwargs:
                name, value = argument.split("=")
                settings[str(ctx.guild.id)][name] = int(value)
        
        os.chdir(f"{self.bot.BASE_DIR}/resources")
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=2)
        os.chdir(self.bot.BASE_DIR)


def setup(bot):
    bot.add_cog(Config(bot))