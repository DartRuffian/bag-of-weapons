""" Bot Information """

# Discord Imports
import discord
from discord import invite
from discord.ext import commands

class Bot_Info(commands.Cog, name="Bot Info"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def invite(self, ctx):
        inviteEmbed = discord.Embed (
            title="Invite Link",
            description="**You can invite me by using this link!** \nhttps://discord.com/api/oauth2/authorize?client_id=755946685288415312&permissions=2147585024&scope=bot",
            color=self.bot.EMBED_COLOR
        )
        inviteEmbed.set_author (
            name=self.bot.user.name, 
            icon_url=self.bot.user.avatar_url
        )
        await ctx.send(embed=inviteEmbed)


def setup(bot):
    bot.add_cog(Bot_Info(bot))