""" Stat Viewer """

# Discord Imports
import discord
from discord.ext import commands

# Other Imports
from utils import Utils

class Stat_Viewer(commands.Cog, name="Stats"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command (
        aliases=["stats","s","health","h"]
    )
    async def view_stats(self, ctx, target:discord.Member=None):
        target = target or ctx.author
        Utils.check_cooldown(self.bot, target)
        stat_embed = Utils.get_stat_embed(self.bot, target=target)
        
        await ctx.send(embed=stat_embed)


def setup(bot):
    bot.add_cog(Stat_Viewer(bot))