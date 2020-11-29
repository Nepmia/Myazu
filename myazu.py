
import discord
from discord.ext import commands
from secret import BOT_TOKEN

import sys, traceback


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Prefix List
    prefixes = ['spc ', '$']

    # Check if message is from guild or DM
    if not message.guild:
        # Only allow ? to be used in DM
        return '?'

    # Allow user to mention bot or use any of the prefixes in prefix list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

# Cogs list
initial_extensions = ['cogs.spc']

bot = commands.Bot(command_prefix=get_prefix, description='MYAZU')

# Load Cogs in initial_extensions
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="$"))
    print(f'Successfully logged in and booted...!')


bot.run(BOT_TOKEN, bot=True, reconnect=True)