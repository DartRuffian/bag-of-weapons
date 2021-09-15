""" Fighting Commands """

# Discord Imports
from inspect import isroutine
import discord
from discord.ext import commands

# Other Imports
from datetime import datetime, timedelta
from random import randint
from asyncio import sleep as async_sleep
import json
import os

# Utilities
from utils import Utils

class Fight_Commands(commands.Cog, name="Fight Commands"):
    def __init__(self, bot):
        self.bot = bot

    def calculate_damage(self, server_id, min:int, max:int):
        # Returns a tuple of the hit status and the damage dealt

        # Load server specific settings
        os.chdir(f"{self.bot.BASE_DIR}/resources")
        with open("settings.json", "r") as f:
            settings = json.load(f)[str(server_id)]
        os.chdir(self.bot.BASE_DIR)

        damage = randint(min, max) # Calculate initial damage
        
        # Check if the hit is a crit
        if randint(1, 100) <= settings["crit_chance"]:
            return (damage*2, "crit")
        
        elif randint(1, 100) >= settings["hit_chance"]:
            return (0, "miss")
        
        else:
            return (damage, "norm")

    @commands.command (
        brief="Basic fighting",
        description="The most commonly used command, basic text-based combat",
        aliases=["f","a","attack"]
    )
    @commands.cooldown(1, 0, commands.BucketType.user)
    async def fight(self, ctx, target:discord.Member, _, *, attack):
        os.chdir(f"{self.bot.BASE_DIR}/resources")
        with open("settings.json", "r") as f:
            settings = json.load(f)
        os.chdir(self.bot.BASE_DIR)

        try: 
            settings[str(ctx.guild.id)]["fight_channel"]
        except KeyError:
            await ctx.send("This server does not currently have a fight channel set up, ask a server moderator to set one up for you!")
            return
        if ctx.channel.id != settings[str(ctx.guild.id)]["fight_channel"]:
            await ctx.send(f"This is not the proper channel to use the fight command in. This server's set channel is <#{settings[str(ctx.guild.id)]['fight_channel']}>", delete_after=5)
            await async_sleep(5)
            await ctx.message.delete()
            return

        if ctx.author == target:
            # "Stop Hitting Yourself"
            await ctx.send(f"While people do say \"The greatest enemy is yourself\", I don't condone hitting yourself with {attack}.")
            return
        
        # Check if the user is unconscious
        is_on_cooldown, time_remaining = Utils.check_cooldown(self.bot, ctx.author)
        if is_on_cooldown is True:
            # User is on cooldown
            killed_by, killed_with = self.bot.member_stats[str(ctx.author.id)][2].split("-|-")

            time_remaining, _ = str(time_remaining).split(".") # Remove miliseconds
            _, time_remaining, _ = time_remaining.split(':') # Keep only minutes

            await ctx.send(f"You're currently unconscious, please try again in {time_remaining} minutes. \nYou were killed by {killed_by} using {killed_with}")
            return

        # Check if the target is unconscious
        if self.bot.member_stats[str(target.id)][0] <= 0:
            target_cooldown_end = datetime.strptime(self.bot.member_stats[str(target.id)][1], "%Y-%m-%d %H:%M:%S.%f")
            target_time_remaining, _ = str(target_cooldown_end - datetime.now()).split(".") # Remove miliseconds
            _, target_time_remaining, _ = target_time_remaining.split(':') # Keep only minutes

            stat_embed = Utils.get_stat_embed(self.bot, target)
            #os.chdir(f"{self.bot.BASE_DIR}/resources")
            already_dead_image = discord.File(f"{self.bot.BASE_DIR}/resources/already_dead.png")
            await ctx.send(f"{target.nick or target.name} is currently unconscious", file=already_dead_image,embed=stat_embed)
            return
        
        damage_dealt, hit_status = self.calculate_damage(ctx.guild.id, 20, 40) # Get the damage dealt

        # Update user stats
        Utils.refresh_stats(self.bot)
        self.bot.member_stats[str(target.id)][0] -= damage_dealt

        # If the target is unconscious, start the cooldown
        kill_message = ""
        if self.bot.member_stats[str(target.id)][0] <= 0:
            self.bot.member_stats[str(target.id)] = [0, str(datetime.now()+timedelta(hours=1)), f"{ctx.author.nick or ctx.author.name}-|-{attack}"]
            kill_message = f"\n\n{target.nick or target.name} was killed by {ctx.author.nick or ctx.author.name} using {attack}"

        Utils.save_stats(self.bot)

        hit_messages = {
            "crit": f"{ctx.author.nick or ctx.author.name} attacked {target.nick or target.name} with {attack}, scored a critical hit, and dealt {damage_dealt} damage!",
            "miss": f"{ctx.author.nick or ctx.author.name} attacked {target.nick or target.name} with {attack}, but missed and dealt no damage!",
            "norm": f"{ctx.author.nick or ctx.author.name} attacked {target.nick or target.name} with {attack}, and dealt {damage_dealt} damage!"
        }

        remaining_health_embed = discord.Embed (
            title="Remaining Health",
            color=0x7c0a02
        )
        remaining_health_embed.set_author (
            name=self.bot.user.name, 
            icon_url=self.bot.user.avatar_url
        )
        for user in [ctx.author, target]:
            remaining_health_embed.add_field (
                name=user.nick or user.name,
                value=f"**:heart: | {self.bot.member_stats[str(user.id)][0]}/100**",
                inline=False
            )
        
        await ctx.send(hit_messages[hit_status]+kill_message, embed=remaining_health_embed)


def setup(bot):
    bot.add_cog(Fight_Commands(bot))