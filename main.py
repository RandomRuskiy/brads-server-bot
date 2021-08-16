import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from discord_slash import SlashCommand, SlashContext

from keep_alive import keep_alive

run = True

if run == False:
  exit()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8', mode='w'
)
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
)
logger.addHandler(handler)


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

client = commands.Bot(command_prefix='£')
slash = SlashCommand(client, sync_commands=True)
TOKEN = os.getenv('TOKEN')

extentions = ['cogs.Embeds',
              'cogs.Config',
              'cogs.Help',
              'cogs.Events',
              'cogs.Slash',
              'cogs.Twitch',
              ]


@client.event
async def on_command_error(ctx, error):
    # dump commmand errors to console for debug
    pass

# console status event


@client.event
async def on_ready():
    # await client.change_presence(status = discord.Status.online)
    print('yo the bot is on now\n-----')

client.remove_command('help')

# keep this at bottom

if __name__ == "__main__":
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")

keep_alive()
client.run(TOKEN)
