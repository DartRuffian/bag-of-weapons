""" Fighting Commands """

# Discord Imports
from inspect import isroutine
import discord
from discord.ext import commands

# Imports
from datetime import datetime, timedelta
from random import randint
import json
import os

class Fight_Commands(commands.Cog, name="Fight Commands"):
    def __init__(self, bot):
        self.bot = bot

    def check_cooldown(self, member_to_check:discord.Member):
        # Returns a tuple of whether the user is on cooldown and their remaining cooldown (if applicable)
        # (is_on_cooldown, remaining_time)

        current_time = datetime.now()
        # Get the user's remaining cooldown (if dead)
        try:
            self.bot.member_stats[str(member_to_check.id)]
        except KeyError:
            self.bot.member_stats[str(member_to_check.id)] = [100, None, None]
        
        cooldown_end = self.bot.member_stats[str(member_to_check.id)][1]
        
        if cooldown_end is None:
            return (False, None)
        
        # Convert the cooldown's end to a datetime object from string
        cooldown_end = datetime.strptime(cooldown_end, "%Y-%m-%d %H:%M:%S.%f")
        
        # User has a cooldown, but has passed
        if current_time >= cooldown_end: 
            self.bot.member_stats[str(member_to_check.id)] = [100, None, None]

            os.chdir(f"{self.bot.BASE_DIR}/resources")
            with open("stats.json", "w") as f:
                json.dump(self.bot.member_stats, f, indent=2)
            os.chdir(self.bot.BASE_DIR)
            return (False, None)
        
        else:
            return (True, cooldown_end-current_time)

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
        if ctx.channel.id != settings[str(ctx.guild.id)]["fight_channel"]:
            # send message saying improper channel
            return

        if ctx.author == target:
            # "Stop Hitting Yourself"
            await ctx.send(f"While people do say \"The greatest enemy is yourself\", I don't condone hitting yourself with {attack}.")
            return
        
        # Check if the user is unconscious
        is_on_cooldown, time_remaining = self.check_cooldown(ctx.author)
        if is_on_cooldown is True:
            # User is on cooldown
            killed_by, killed_with = self.bot.member_stats[str(ctx.author.id)][2].split("-|-")

            author_cooldown_end = datetime.strptime(self.bot.member_stats[str(ctx.author.id)][1], "%Y-%m-%d %H:%M:%S.%f")
            author_time_remaining, _ = str(author_cooldown_end - datetime.now()).split(".") # Remove miliseconds
            _, author_time_remaining, _ = author_time_remaining.split(':') # Keep only minutes

            await ctx.send(f"You're currently unconscious, please try again in {author_time_remaining} minutes. \nYou were killed by {killed_by} using {killed_with}")
            return

        # Check if the target is unconscious
        if self.bot.member_stats[str(target.id)][0] <= 0:
            target_cooldown_end = datetime.strptime(self.bot.member_stats[str(target.id)][1], "%Y-%m-%d %H:%M:%S.%f")
            target_time_remaining, _ = str(target_cooldown_end - datetime.now()).split(".") # Remove miliseconds
            _, target_time_remaining, _ = target_time_remaining.split(':') # Keep only minutes


            await ctx.send(f"{target.nick or target.name} is currently unconscious. Wait {target_time_remaining} minutes for them to regain consciousness.")
            return
        
        damage_dealt, hit_status = self.calculate_damage(ctx.guild.id, 20, 40) # Get the damage dealt

        # Update user stats
        os.chdir(f"{self.bot.BASE_DIR}/resources")
        with open("stats.json", "r") as f:
            self.bot.member_stats = json.load(f)
        self.bot.member_stats[str(target.id)][0] -= damage_dealt

        # If the target is unconscious, start the cooldown
        kill_message = ""
        if self.bot.member_stats[str(target.id)][0] <= 0:
            self.bot.member_stats[str(target.id)] = [0, str(datetime.now()+timedelta(hours=1)), f"{ctx.author.nick or ctx.author.name}-|-{attack}"]
            kill_message = f"\n\n{target.nick or target.name} was killed by {ctx.author.nick or ctx.author.name} using {attack}"

        with open("stats.json", "w") as f:
            json.dump(self.bot.member_stats, f, indent=2)
        os.chdir(self.bot.BASE_DIR)

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
                value=f":heart: {self.bot.member_stats[str(user.id)][0]}/100",
                inline=False
            )
        
        await ctx.send(hit_messages[hit_status]+kill_message, embed=remaining_health_embed)


def setup(bot):
    bot.add_cog(Fight_Commands(bot))