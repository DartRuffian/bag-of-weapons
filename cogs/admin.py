""" Bot Admin Exclusive Commands """

# Discord Imports
import discord
from discord.ext import commands

# Other Libraries
import json
import os

# Utils
from utils import Utils

class Admin_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @Utils.is_owner()
    async def say(self, ctx, channels:commands.Greedy[discord.TextChannel], *, message):
        # Takes any number of channels and sends a message to those channels
        await ctx.message.delete()
        if channels == []:
            channels = [ctx.channel]
        for channel in channels:
            await channel.send(message)
    
    @commands.command (
        hidden=True,
        aliases=["reset", "r"]
    )
    @Utils.is_owner()
    async def reset_stats(self, ctx):
        # Resets stats for all users
        os.chdir(f"{self.bot.BASE_DIR}/resources")
        self.bot.member_stats = {}
        with open("stats.json", "w") as f:
            for user in self.bot.get_all_members():
                self.bot.member_stats[str(user.id)] = [100, None, None]
            json.dump(self.bot.member_stats, f, indent=2)
        os.chdir(self.bot.BASE_DIR)


def setup(bot):
    bot.add_cog(Admin_Commands(bot))