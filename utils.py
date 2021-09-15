""" Utilities class for useful functions """

# Imports
import discord
from discord.ext import commands
from datetime import datetime
from json import load, dump
from os import chdir

class Utils:
    def is_owner():
        # Return whether a given user is the bot author
        async def predicate(ctx):
            return ctx.author.id == 400337254989430784
        return commands.check(predicate)
    
    def get_server_prefix(bot, message):
        # Returns a server's prefix
        chdir(f"{bot.BASE_DIR}/resources")

        with open("prefixes.json", "r") as f:
            prefixes = load(f)
        
        chdir(bot.BASE_DIR)
        return prefixes[str(message.guild.id)]

    def get_stat_embed(bot, target:discord.Member):
        # Returns a discord.Embed of the target's stats
        chdir(f"{bot.BASE_DIR}/resources")
        with open("stats.json", "r") as f:
            target_stats = load(f)[str(target.id)]
        chdir(bot.BASE_DIR)

        stat_embed = discord.Embed (
            title="",
            color=0x7c0a02
        )
        stat_embed.set_author (
            name=f"{target.nick or target.name}'s Stats",
            icon_url=target.avatar_url
        )

        if target_stats[0] > 0:
            stat_embed.description=f":heart: **| {target_stats[0]}/100**"
        
        else:
            target_cooldown_end = datetime.strptime(target_stats[1], "%Y-%m-%d %H:%M:%S.%f")
            target_time_remaining, _ = str(target_cooldown_end - datetime.now()).split(".") # Remove miliseconds
            _, target_time_remaining, _ = target_time_remaining.split(':') # Keep only minutes

            stat_embed.description=f":timer: **| {target_time_remaining} Minutes \n:skull: | {target_stats[2].split('-|-')[0]} \n:crossed_swords: | {target_stats[2].split('-|-')[1]}**"
        
        return stat_embed
    
    def refresh_stats(bot):
        # Saves the stats.json file to bot.member_stats
        chdir(f"{bot.BASE_DIR}/resources")
        with open("stats.json", "r") as f:
            bot.member_stats = load(f)
        chdir(bot.BASE_DIR)
    
    def save_stats(bot):
        # Writes the bot.member_stats dictionary to a file
        chdir(f"{bot.BASE_DIR}/resources")
        with open("stats.json", "w") as f:
            dump(bot.member_stats, f, indent=2)
        chdir(bot.BASE_DIR)

    def check_cooldown(bot, member_to_check:discord.Member):
        # Returns a tuple of whether the user is on cooldown and their remaining cooldown (if applicable)
        # (is_on_cooldown, remaining_time)

        current_time = datetime.now()
        # Get the user's remaining cooldown (if dead)
        try:
            bot.member_stats[str(member_to_check.id)]
        except KeyError:
            bot.member_stats[str(member_to_check.id)] = [100, None, None]
        
        cooldown_end = bot.member_stats[str(member_to_check.id)][1]
        
        if cooldown_end is None:
            return (False, None)
        
        # Convert the cooldown's end to a datetime object from string
        cooldown_end = datetime.strptime(cooldown_end, "%Y-%m-%d %H:%M:%S.%f")
        
        # User has a cooldown, but has passed
        if current_time >= cooldown_end: 
            bot.member_stats[str(member_to_check.id)] = [100, None, None]

            Utils.save_stats(bot)
            return (False, None)
        
        else:
            return (True, cooldown_end-current_time)