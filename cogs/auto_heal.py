""" Cog Description """

# Discord Imports
import discord
from discord.ext import commands, tasks

# Utils
from utils import Utils
import json
import os

class Auto_Healing(commands.Cog, name="Auto Healing"):
    def __init__(self, bot):
        self.bot = bot
        self.heal_all_users.start()

    @tasks.loop(minutes=1)
    async def heal_all_users(self):
        print("Healing users")
        Utils.refresh_stats(self.bot)
        for stats in self.bot.member_stats.values():
            if stats[0] != 0 and stats[0] < 100:
                stats[0] += 1
        Utils.save_stats(self.bot)


def setup(bot):
    bot.add_cog(Auto_Healing(bot))