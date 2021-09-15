""" Error Handler """

# Discord Imports
import discord
from discord.ext import commands

# Other Imports
import traceback
from utils import Utils

class Error_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Handle errors that may be raised
        error_embed = discord.Embed (
            title="An Error has Occurred",
            description=f"**Error Type: {type(error)}** \n\n{error}"
        )
        error_embed.set_author (
            name=self.bot.user.name, 
            icon_url=self.bot.user.avatar_url
        )

        non_critical_errors = [
            discord.ext.commands.errors.CommandNotFound,
            discord.ext.commands.errors.CommandOnCooldown,
            discord.ext.commands.errors.MissingRequiredArgument,
            discord.ext.commands.errors.MissingPermissions
        ]

        if type(error) not in non_critical_errors:
            await self.bot.AUTHOR.send(f"Full Error Message:\n```py\n{traceback.format_exc()}\n```", embed=error_embed)
        
        await ctx.send(embed=error_embed)


def setup(bot):
    bot.add_cog(Error_Handler(bot))