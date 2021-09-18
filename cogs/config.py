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
        accepted_args = [
            "crit_chance",
            "hit_chance",
            "fight_channel"
        ]

        if kwargs == ("reset",):
            settings[str(ctx.guild.id)] = default_settings
        else:
            for argument in kwargs:
                if argument.lower() in accepted_args:
                    name, value = argument.lower().split("=")
                    settings[str(ctx.guild.id)][name] = int(value)
                
                else:
                    await ctx.send(f"Whoops! Argument `{argument.lower()}` is an accept setting, the list of accepted settings are...")
                    await ctx.send("\n".join(accepted_args))
        
        os.chdir(f"{self.bot.BASE_DIR}/resources")
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=2)
        os.chdir(self.bot.BASE_DIR)
    
    @commands.command()
    @has_permissions(manage_channels=True)
    async def change_prefix(self, ctx, new_prefix):
        os.chdir(f"{self.bot.BASE_DIR}/resources")
        with open("prefixes.json", "f") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = new_prefix
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=2)
        os.chdir(self.bot.BASE_DIR)
    
    # Add/Remove prefixes when joining and leaving a server
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        os.chdir(f"{self.bot.BASE_DIR}/resources")
        with open("prefixes.json", "f") as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = "-"
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=2)
        os.chdir(self.bot.BASE_DIR)
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        os.chdir(f"{self.bot.BASE_DIR}/resources")
        with open("prefixes.json", "f") as f:
            prefixes = json.load(f)
        del prefixes[str(guild.id)]
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=2)
        os.chdir(self.bot.BASE_DIR)


def setup(bot):
    bot.add_cog(Config(bot))