""" Bot Admin Exclusive Commands """

# Discord Imports
import discord
from discord.ext import commands

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


def setup(bot):
    bot.add_cog(Admin_Commands(bot))